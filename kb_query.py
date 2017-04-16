import sys
import sparql
import operator
from difflib import SequenceMatcher

sparql_dbpedia_on = 'https://dbpedia.org/sparql'
entity_label_threshold = 1.0

def similarity_score(a,b):
    return SequenceMatcher(None,a,b).ratio()

def resource_extractor(labels):
    print labels
    resources = {}
    for i,label in enumerate(labels):
        my_labels = label[0].split()
        if len(my_labels) == 1:
            q_u = ('SELECT distinct ?uri ?label WHERE { ?uri rdfs:label ?label . FILTER langMatches( lang(?label), "EN" ). ?label bif:contains "' +str(my_labels[0]) +'" . }')
        else:
            q_u = ('SELECT distinct ?uri ?label WHERE { ?uri rdfs:label ?label .  FILTER langMatches( lang(?label), "EN" ). ?label bif:contains "' +str(my_labels[1]) +'" . FILTER (CONTAINS(?label, "'+str(my_labels[0])+'"))}')

        print "sparql query: "+q_u
        result = sparql.query(sparql_dbpedia_on, q_u)
        values = [sparql.unpack_row(row) for row in result]
        add_score = [similarity_score(label[0], val[1]) for val in values]
        for s, score in enumerate(add_score):
            values[s].append(score)
        sorted_values = sorted(values, key=operator.itemgetter(2), reverse=True)
        threshold_sorted = [vals for vals in sorted_values if vals[2] >= entity_label_threshold]
        resources[label[0]] = threshold_sorted
    return resources