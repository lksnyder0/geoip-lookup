#!/usr/bin/env python2
import os
import sys
try:
	import argparse
	opt = False
except ImportError:
	from optparse import OptionParser
	opt = True
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import pygeoip

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
	if opt:
		usage = "usage: %prog [options] ip [ip ...]"
		parser = OptionParser(usage=usage)
		parser.add_option("-n", "--name", action="store_true", dest="name", default=False,
			help="Print country name instead of country code")
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
			lType = "city"
			db = options.citydb
		elif options.asn:
			lType = "asn"
			db = options.asndb
		else:
			ltype = "country"
			db = options.db
		name = options.name
	else:
		parser = argparse.ArgumentParser()
		parser.add_argument('ips', metavar="ip", nargs="+", help="ip address/es to lookup")
		parser.add_argument("-n", "--name", dest="name", action="store_true", default=False,
			help="Print country names instead of country codes")
		parser.add_argument("-d", "--database", dest="db", default="/usr/local/share/GeoIP/GeoIP.dat", 
			metavar="<db path>", help="Path to maxmind GeoIP database")
		parser.add_argument("-c", "--city", dest="city", action="store_true", default=False,
			help="Do city lookup instead of country")
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
			lType = "city"
			db = args.citydb
		elif args.asn:
			lType = "asn"
			db = args.asndb
		else:
			ltype = "country"
			db = args.db

	## Verify shiz
	## IP addresses
	if not verifyIPs(ips):
		print "Error: Invalid ip provided"
		exit(1)

	## location and permissions of database
	try:
		## will close file descriptor when we leave the with statement or error out
		with open(db) as e:
			pass
	except IOError as e:
		print "Error: %s %s" % (e.strerror, db)
		exit(1)

	gi4 = pygeoip.GeoIP(db, pygeoip.MEMORY_CACHE)
	for ip in ips:
		if lType == "country":
			if name:
				co = gi4.country_name_by_addr(ip)
			else:
				co = gi4.country_code_by_addr(ip)
		elif lType == "asn":
			co = gi4.asn_by_name(ip)
		elif lType == "city":
			r = gi4.record_by_addr(ip)
			co = "%s, %s" % (r["city"], r["region_code"])
		print "%s:%s" %(ip, co)


main()
