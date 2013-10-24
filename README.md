# GeoIP Lookup
## Installation
### Maxmind DB
```bash
wget -N http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz
gunzip GeoIP.dat.gz
sudo mkdir -p /usr/local/share/GeoIP
sudo mv GeoIP.dat /usr/local/share/GeoIP
```
### Clone tool
```bash
git clone git@10.16.251.135:security/geoip-lookup.git
cd geoip-lookup
```
## Usage
If you are using python >=2.7 the usage is:
```
usage: lookup [-h] [-n] [-d db path] ip [ip ...]

positional arguments:
  ip                    ip address/es to lookup

optional arguments:
  -h, --help            show this help message and exit
  -n, --name            Print country names instead of country codes
  -d db path, --database db path
                        Path to maxmind GeoIP database
```
Other wise it is 
```
Usage: lookup [options] ip [ip ...]

Options:
  -h, --help            show this help message and exit
  -n, --name            Print country name instead of country code
  -d db path, --database=db path
                        Path to maxmind GeoIP database
```
