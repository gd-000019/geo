#!/usr/bin/env python3

import argparse
import gzip
import ipaddress
import json
import shutil
import socket
import sys
import urllib.request
from pathlib import Path

import maxminddb


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CONFIG_FILE = BASE_DIR / "databases.json"


def load_config():
    with CONFIG_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)["databases"]


def populate(force=False):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for name, db in load_config().items():
        target = DATA_DIR / db["filename"]

        if target.exists() and not force:
            print(f"[skip] {target.name}")
            continue

        tmp = target.with_suffix(target.suffix + ".tmp")

        for url in (db["url"], db.get("fallback_url")):
            if not url:
                continue

            try:
                print(f"[download] {name}: {url}")
                urllib.request.urlretrieve(url, tmp)
                break
            except Exception as exc:
                print(f"[failed] {url}: {exc}", file=sys.stderr)
        else:
            print(f"[error] could not download {name}", file=sys.stderr)
            continue

        try:
            with tmp.open("rb") as f:
                gzipped = f.read(2) == b"\x1f\x8b"

            if gzipped:
                with gzip.open(tmp, "rb") as src, target.open("wb") as dst:
                    shutil.copyfileobj(src, dst)
                tmp.unlink()
            else:
                shutil.move(tmp, target)

            print(f"[ok] {target}")

        except Exception as exc:
            print(f"[error] {name}: {exc}", file=sys.stderr)
            tmp.unlink(missing_ok=True)


def get_record(db_name, ip):
    db = load_config().get(db_name)

    if not db:
        return {}, None

    path = DATA_DIR / db["filename"]

    if not path.exists():
        return {}, None

    try:
        with maxminddb.open_database(str(path)) as reader:
            record, prefix = reader.get_with_prefix_len(ip)
            return record or {}, prefix
    except Exception:
        return {}, None


def country_flag(code):
    if not code or len(code) != 2:
        return None

    return "".join(
        chr(127397 + ord(char))
        for char in code.upper()
    )


def reverse_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror, OSError):
        return None


def address_type(address):
    if address.is_private:
        return "private"
    if address.is_loopback:
        return "loopback"
    if address.is_link_local:
        return "link-local"
    if address.is_multicast:
        return "multicast"
    if address.is_reserved:
        return "reserved"
    if address.is_unspecified:
        return "unspecified"

    return "public" if address.is_global else "non-public"


def empty_result(ip, network_type):
    return {
        "hostname": None,
        "asn": {
            "number": None,
            "org": None,
        },
        "network": {
            "cidr": None,
            "type": network_type,
        },
        "country": {
            "name": None,
            "code": None,
            "flag": None,
        },
        "region": None,
        "city": None,
        "location": {
            "lat": None,
            "lon": None,
            "accuracy": None,
        },
        "continent": None,
        "timezone": None,
        "postal": None,
        "_source": None,
        "_meta": {
            "ip": ip,
            "sources": [],
        },
    }


def lookup(ip):
    try:
        address = ipaddress.ip_address(ip)
    except ValueError:
        raise SystemExit(f"Invalid IP address: {ip}")

    network_type = address_type(address)

    if not address.is_global:
        return empty_result(ip, network_type)

    maxmind, maxmind_prefix = get_record("geolite2", ip)
    dbip, dbip_prefix = get_record("dbip", ip)
    asn, asn_prefix = get_record("asn", ip)
    origin_asn, origin_prefix = get_record("origin_asn", ip)

    city = maxmind or dbip

    sources = []

    if maxmind:
        sources.append("maxmind")

    if dbip:
        sources.append("dbip")

    if asn:
        sources.append("asn")

    if origin_asn:
        sources.append("origin-asn")

    hostname = reverse_hostname(ip)

    if hostname:
        sources.append("rdns")

    country = city.get("country", {})
    location = city.get("location", {})
    subdivisions = city.get("subdivisions", [])

    country_code = country.get("iso_code")

    asn_number = (
        asn.get("autonomous_system_number")
        or origin_asn.get("autonomous_system_number")
    )

    asn_org = (
        asn.get("autonomous_system_organization")
        or origin_asn.get("autonomous_system_organization")
    )

    # Prefer routing/ASN prefixes.
    # GeoIP prefixes are only used as a final fallback.
    prefix = (
        origin_prefix
        or asn_prefix
        or maxmind_prefix
        or dbip_prefix
    )

    cidr = None

    if prefix is not None:
        cidr = str(
            ipaddress.ip_network(
                f"{ip}/{prefix}",
                strict=False,
            )
        )

    region = (
        subdivisions[0].get("names", {}).get("en")
        if subdivisions
        else None
    )

    return {
        "hostname": hostname,
        "asn": {
            "number": asn_number,
            "org": asn_org,
        },
        "network": {
            "cidr": cidr,
            "type": network_type,
        },
        "country": {
            "name": country.get("names", {}).get("en"),
            "code": country_code,
            "flag": country_flag(country_code),
        },
        "region": region,
        "city": city.get("city", {}).get("names", {}).get("en"),
        "location": {
            "lat": location.get("latitude"),
            "lon": location.get("longitude"),
            "accuracy": location.get("accuracy_radius"),
        },
        "continent": city.get("continent", {}).get("code"),
        "timezone": location.get("time_zone"),
        "postal": city.get("postal", {}).get("code"),
        "_source": sources[0] if sources else None,
        "_meta": {
            "ip": ip,
            "sources": sources,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Static GeoIP lookup")

    parser.add_argument(
        "--ip",
        help="IP address to lookup",
    )

    parser.add_argument(
        "--json",
        metavar="OUTPUT",
        nargs="?",
        const="-",
        help="Print JSON or save it to OUTPUT",
    )

    parser.add_argument(
        "--populate",
        action="store_true",
        help="Download databases",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace existing databases",
    )

    args = parser.parse_args()

    if args.populate:
        populate(args.force)
        return

    if not args.ip:
        parser.error("use --ip IP or --populate")

    output = json.dumps(
        lookup(args.ip),
        indent=2,
        ensure_ascii=False,
    )

    if args.json and args.json != "-":
        Path(args.json).write_text(
            output + "\n",
            encoding="utf-8",
        )
    else:
        print(output)


if __name__ == "__main__":
    main()