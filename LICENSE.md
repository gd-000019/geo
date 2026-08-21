# License

## Source Code

Copyright (c) 2026 geo contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

## Third-Party Data

The `geo` source code is licensed under the MIT License above.

GeoIP and ASN databases downloaded by `geo --populate` are third-party data
and are not covered by the MIT License of this project. Each database remains
subject to its own license and terms of use.

### MaxMind GeoLite2

Used for GeoLite2 City and GeoLite2 ASN data.

- Provider: MaxMind
- License: GeoLite2 License / CC BY-SA 4.0
- Attribution: This product includes GeoLite Data created by MaxMind.

Users must comply with the applicable MaxMind GeoLite2 license and terms.

### DB-IP City Lite

Used as a city geolocation data source.

- Provider: DB-IP
- License: CC BY 4.0
- Attribution: IP geolocation data provided in part by DB-IP.com.

Users must comply with the applicable DB-IP Lite license and attribution
requirements.

### origin-asn

Used for BGP origin ASN and routed network prefix data.

- Provider: sapics/ip-location-db
- License: PDDL

Users must comply with the applicable license and upstream data terms.

## Database Distribution

Database files downloaded at runtime are not distributed as part of the
project source code unless explicitly included by a distributor.

Users and redistributors are responsible for reviewing and complying with
the licenses, attribution requirements, and terms of the respective data
providers.
