# geo

CLI for IP geolocation using local MaxMind, DB-IP and ASN databases.

## Features

- IP geolocation lookup
- Reverse DNS hostname lookup
- ASN and organization lookup
- Network prefix lookup
- Public and non-public IP detection
- Country, flag, region and city
- Coordinates, timezone and postal code
- Local MMDB databases
- JSON output
- Optional JSON file export
- Database population with fallback sources

## Installation

```bash
git clone https://github.com/gd-000019/geo.git
cd geo
pip install -r requirements.txt
chmod +x geo.py
python3 geo.py --populate
```

## Usage

Lookup an IP:

```bash
python3 geo.py --ip 8.8.8.8
```

Save the result:

```bash
python3 geo.py --ip 8.8.8.8 --json result.json
```

Update databases:

```bash
python3 geo.py --populate
```

Force database replacement:

```bash
python3 geo.py --populate --force
```

## Output

```json
{
  "hostname": "69-6-233-11.unifiedlayer.com",
  "asn": {
    "number": 26337,
    "org": "Oso Grande IP Services, LLC"
  },
  "network": {
    "cidr": "69.6.233.0/24",
    "type": "public"
  },
  "country": {
    "name": "Colombia",
    "code": "CO",
    "flag": "🇨🇴"
  },
  "region": "Cundinamarca",
  "city": "Cota",
  "location": {
    "lat": 4.7109,
    "lon": -74.2067,
    "accuracy": 20
  },
  "continent": "SA",
  "timezone": "America/Bogota",
  "postal": "250027",
  "_source": "maxmind",
  "_meta": {
    "ip": "69.6.233.11",
    "sources": [
      "maxmind",
      "dbip",
      "origin-asn",
      "rdns"
    ]
  }
}
```

## Requirements

```text
python 3
maxminddb
```

```markdown
No external API keys are required. GeoIP data is read locally; hostname lookup uses the system DNS resolver.
```

## Data Sources and Licensing

`geo` source code is licensed under the MIT License.

The databases downloaded by `geo --populate` are provided by third parties and remain subject to their respective licenses:

- GeoLite2 City and ASN — MaxMind GeoLite2 License / CC BY-SA 4.0
- DB-IP City Lite — CC BY 4.0
- origin-asn — PDDL

This product includes GeoLite Data created by MaxMind.

IP geolocation data provided in part by DB-IP.com.

Downloaded database files are not part of the `geo` source code license. Users are responsible for complying with the terms of each data provider.