#!/bin/sh
#
#

base_addr="http://127.0.0.1:8000"

# Root - Get list of all mosques
addr=$base_addr"/"
echo "===> $addr"
curl -H "Content-Type: application/json" $addr
echo ""

# Mosque details request
addr=$base_addr"/mosque/1/"
echo "===> $addr"
curl -H "Content-Type: application/json" $addr
echo ""

# Mosque details request - mosque doesn't exist
addr=$base_addr"/mosque/1000000/"
echo "===> $addr"
curl -H "Content-Type: application/json" $addr
echo ""

# Search request
addr=$base_addr"/search"
echo "===> $addr"
curl -H "Content-Type: application/json" $addr
echo ""
