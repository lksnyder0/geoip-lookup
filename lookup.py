#!/usr/bin/env python2
import os
import sys
from os.path import isfile
try:
	import argparse
	opt = False
except ImportError:
	from optparse import OptionParser
	opt = True
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
try:
	import pygeoip
except ImportError:
	print "Please install pygeoip library"
	exit(1)

def checkFile(location):
	## location and permissions of database
	try:
		## will close file descriptor when we leave the with statement or error out
		with open(location) as e:
			pass
	except IOError as e:
		print "Error: %s %s" % (e.strerror, location)
		exit(1)
	return True

def verifyIPs(ips):
	import socket
	if type(ips) == list:
		for ip in ips:
			try:
				socket.inet_pton(socket.AF_INET, ip)
			except socket.error:
				return False
		return True
	elif type(ips) == type(""):
		try:
			socket.inet_pton(socket.AF_INET, ip)
		except socket.error:
			return False
		return True
	else:
		return False

def main():
	country = False
	city = False
	asn = False
	if opt or True:
		from optparse import OptionParser
		usage = "usage: %prog [options] ip [ip ...]"
		parser = OptionParser(usage=usage)
		parser.add_option("-n", "--name", action="store_true", dest="name", default=False,
			help="Print country name instead of country code")
		parser.add_option("-t", "--country", dest="country", action="store_true", default=False,
			help="Do country lookup")
		parser.add_option("-d", "--database", dest="db", metavar="<db path>",
			help="Path to maxmind GeoIP database", default="/usr/local/share/GeoIP/GeoIP.dat")
		#City database
		parser.add_option("-c", "--city", dest="city", action="store_true", default=False,
			help="Do city lookup")
		parser.add_option("--city-database", dest="citydb", default="/usr/local/share/GeoIP/GeoLiteCity.dat",
			metavar="<city db path>", help="Path to maxmind city lite db")
		#ASN database
		parser.add_option("-a", "--asn", dest="asn", action="store_true", default=False,
			help="Do ASN lookup")
		parser.add_option("--asn-database", dest="asndb", default="/usr/local/share/GeoIP/GeoIPASNum.dat",
			metavar="<asn db path>", help="Path to maxmind asn lite db")
		options,args = parser.parse_args()
		if len(args) < 1:
			print "Need to provide ip address"
			parser.print_help()
		ips = args
		if options.city:
			city = True
			if checkFile(options.citydb):
				citydb = options.citydb
		if options.asn:
			asn = True
			if checkFile(options.asndb):
				asndb = options.asndb
		if options.country:
			country = True
			if checkFile(options.db):
				db = options.db
		if not city and not country and not asn:
			country = True
			if checkFile(options.db):
				db = options.db
		name = options.name
	else:
		parser = argparse.ArgumentParser()
		parser.add_argument('ips', metavar="ip", nargs="+", help="ip address/es to lookup")
		parser.add_argument("-co", "--country", dest="country", action="store_true", default=False,
			help="Do country lookup")
		parser.add_argument("-n", "--name", dest="name", action="store_true", default=False,
			help="Print country names instead of country codes")
		parser.add_argument("-d", "--database", dest="db", default="/usr/local/share/GeoIP/GeoIP.dat", 
			metavar="<db path>", help="Path to maxmind GeoIP database")
		parser.add_argument("-c", "--city", dest="city", action="store_true", default=False,
			help="Do city lookup")
		parser.add_argument("-dc", "--city-database", dest="citydb", default="/usr/local/share/GeoIP/GeoLiteCity.dat",
			metavar="<city db path>", help="Path to maxmind city lite db")
		parser.add_argument("-a", "--asn", dest="asn", action="store_true", default=False,
			help="Do ASN lookup")
		parser.add_argument("-da", "--asn-database", dest="asndb", default="/usr/local/share/GeoIP/GeoIPASNum.dat",
			metavar="<asn db path>", help="Path to maxmind asn lite db")
		args = parser.parse_args()
		name = args.name
		ips = args.ips
		if args.city:
			city = True
			if checkFile(args.citydb):
				citydb = args.citydb
		if args.asn:
			asn = True
			if checkFile(args.asndb):
				asndb = args.asndb
		if args.country:
			country = True
			if checkFile(args.db):
				db = args.db
		if not city and not country and not asn:
			country = True
			if checkFile(args.db):
				db = args.db

	## Verify shiz
	## IP addresses
	if not verifyIPs(ips):
		print "Error: Invalid ip provided"
		exit(1)

	for ip in ips:
		co = ""
		if country:
			country = pygeoip.GeoIP(db, pygeoip.MEMORY_CACHE)
			if name:
				co += ":" + country.country_name_by_addr(ip) 
			else:
				co += ":" + country.country_code_by_addr(ip)
		if asn:
			asn = pygeoip.GeoIP(asndb, pygeoip.MEMORY_CACHE)
			co += ":" + asn.org_by_name(ip)
		if city:
			city = pygeoip.GeoIP(citydb, pygeoip.MEMORY_CACHE)
			r = city.record_by_addr(ip)
			co += ":%s, %s" % (r["city"], r["region_code"])
		print "%s%s" %(ip, co)


main()
