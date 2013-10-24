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
		parser.add_option("-d", "--database", dest="db", metavar="db path",
			help="Path to maxmind GeoIP database", default="/usr/local/share/GeoIP/GeoIP.dat")
		options,args = parser.parse_args()
		if len(args) < 1:
			print "Need to provide ip address"
			parser.print_help()
		ips = args
		name = options.name
		db = options.db
	else:
		parser = argparse.ArgumentParser()
		parser.add_argument('ips', metavar="ip", nargs="+", help="ip address/es to lookup")
		parser.add_argument("-n", "--name", dest="name", action="store_true", default=False,
			help="Print country names instead of country codes")
		parser.add_argument("-d", "--database", dest="db", default="/usr/local/share/GeoIP/GeoIP.dat", 
			metavar="db path", help="Path to maxmind GeoIP database")
		args = parser.parse_args()
		name = args.name
		db = args.db
		ips = args.ips

	## Verify shiz
	## IP addresses
	if not verifyIPs(ips):
		print "Error: Invalid ip provided"
		exit(1)

	## location and permissions of database
	try:
		## will close file descriptor with we leave the with statement or error out
		with open(db) as e:
			pass
	except IOError as e:
		print "Error: %s %s" % (e.strerror, db)
		exit(1)

	gi4 = pygeoip.GeoIP(db, pygeoip.MEMORY_CACHE)
	for ip in ips:
		if name:
			co = gi4.country_name_by_addr(ip)
		else:
			co = gi4.country_code_by_addr(ip)
		print "%s:%s" %(ip, co)


main()
