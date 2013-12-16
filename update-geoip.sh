#!/bin/bash

GEOLITE_COUNTRY="http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz"
GEOLITE_COUNTRY_NAME="GeoIP.dat.gz"
GEOLITE_CITY="http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz"
GEOLITE_CITY_NAME="GeoLiteCity.dat.gz"
GEOLITE_ASN="http://download.maxmind.com/download/geoip/database/asnum/GeoIPASNum.dat.gz"
GEOLITE_ASN_NAME="GeoIPASNum.dat.gz"
LOCATION="/usr/local/share/GeoIP/"

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

function update {
	mkdir -p /tmp/GeoIP
	cd /tmp/GeoIP
	curl --silent -o $2 $1
	gzip -d $2
	mv `ls -1 | cut -d "." -f -2` $LOCATION
}

mkdir $LOCATION

case $1 in
	country) 	echo "Updating country database"
				update $GEOLITE_COUNTRY $GEOLITE_COUNTRY_NAME
				;;
	city)		echo "Updating city database"
				update $GEOLITE_CITY $GEOLITE_CITY_NAME
				;;
	asn)		echo "Updating ASN database"
				update $GEOLITE_ASN $GEOLITE_ASN_NAME
				;;
	*)			echo "$0 [country|city|asn|help]"
				;;
esac
