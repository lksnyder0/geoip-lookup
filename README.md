# GeoIP Lookup
## Installation
### Maxmind DB
```bash
./update-geoip.sh all
```

### Clone tool
```bash
git clone git@10.16.251.135:security/geoip-lookup.git
cd geoip-lookup
```
### Install pygeoip
```bash
sudo pip install pygeoip
```
### Link so you can run it anywhere
```bash
sudo ln -s $PWD/lookup.py /usr/bin/lookup
sudo ln -s $PWD/update-geoip.sh /usr/bin/update-geoip
```
## Usage
If you are using python 2.7.x the usage is

```
usage: lookup.py [-h] [-n] [-d <db path>] [-c] [-dc <city db path>] [-a]
                 [-da <asn db path>]
                 ip [ip ...]

positional arguments:
  ip                    ip address/es to lookup

optional arguments:
  -h, --help            show this help message and exit
  -n, --name            Print country names instead of country codes
  -d <db path>, --database <db path>
                        Path to maxmind GeoIP database
  -c, --city            Do city lookup instead of country
  -dc <city db path>, --city-database <city db path>
                        Path to maxmind city lite db
  -a, --asn             Do ASN lookup
  -da <asn db path>, --asn-database <asn db path>
                        Path to maxmind asn lite db
```

Other wise it is 

```
Usage: lookup.py [options] ip [ip ...]

Options:
  -h, --help            show this help message and exit
  -n, --name            Print country name instead of country code
  -d <db path>, --database=<db path>
                        Path to maxmind GeoIP database
  -c, --city            Do city lookup
  --city-database=<city db path>
                        Path to maxmind city lite db
  -a, --asn             Do ASN lookup
  --asn-database=<asn db path>
                        Path to maxmind asn lite db
```
