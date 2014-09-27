#!/bin/sh

osmconvert $1 -o=$1.o5m
osmfilter $1.o5m --keep="railway=station =halt" -o=filtered_$1.osm