import sys
import difflib
import pprint
import codecs

from imposm.parser import OSMParser

class ParseAggregator(object):
	names = []

	def nodes(self, nodes):
		for element in nodes:
			if "name" in element[1]:
				self.names.append(element[1]['name'])

	def ways(self, ways):
		for element in ways:
			if "name" in element[1]:
				self.names.append(element[1]['name'])

	def relations(self, relations):
		for element in relations:
			if "name" in element[1]:
				self.names.append(element[1]['name'])


def read_osm_file(osm_filepath):
	aggr = ParseAggregator()
	p = OSMParser(concurrency=4, nodes_callback=aggr.nodes, ways_callback=aggr.ways, relations_callback=aggr.relations)
	p.parse(osm_filepath)
	return aggr.names


def read_bahn_file(bahn_filepath):
	bahn_names = []
	with codecs.open("planb_2.tsv", "r", encoding="utf-8") as f:
		for line in iter(f.readline, ''):
			line = line.split("	")
			bahn_names.append(line[3].strip())

	return bahn_names


def compare(osm_names, bahn_filepath):
	ratio_calc = difflib.SequenceMatcher()
	match_ratio = 0.8
	exact_matches = []
	close_matches = []
	results = {}

	bahn_names = read_bahn_file(bahn_filepath)
	results["number_of_elements"] = {"bahn": len(bahn_names), "osm": len(osm_names)}

	for bahn_station in bahn_names:
		if bahn_station in osm_names:
			exact_matches.append(bahn_station)
		else:
			if len(difflib.get_close_matches(bahn_station, osm_names, 1, match_ratio)) > 0:
				close_matches.append(bahn_station)

	results["in_both"] = len(exact_matches)
	results["close_matches"] = len(close_matches)

	return results


if __name__ == "__main__":
	if(len(sys.argv) < 3):
		print("usage: bash_osm_comparator.py $osm_file_name $bahn_file_name")
		sys.exit(-1)

	osm_names = read_osm_file(sys.argv[1])
	results = compare(osm_names, sys.argv[2])
	pp = pprint.PrettyPrinter(indent=4)
	pp.pprint(results)