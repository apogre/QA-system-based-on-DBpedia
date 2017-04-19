import sys
import sparql
import operator
from difflib import SequenceMatcher
from nltk import word_tokenize

# sparql_dbpedia_on = 'https://dbpedia.org/sparql'
sparql_dbpedia_on = 'http://localhost:8890/sparql'
entity_label_threshold = 1.0

question_dict = {'Who':'Person','Where':'Location'}


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


def graph_generator(resource,question_type):
    # print question_type
    for k,v in resource.iteritems():
        for val in v:
            if not 'Category:' in val[0] and not 'wikidata' in val[0]:
                url = val[0]
                q_graph = ('SELECT distinct ?p ?o WHERE { {<' + url + '> ?p ?o} UNION {?o ?p <' + url + '> }  . ?o rdf:type <http://dbpedia.org/ontology/'+question_dict[question_type]+'> .}')
                print q_graph
                # sys.exit(0)
                result = sparql.query(sparql_dbpedia_on, q_graph)
                q_values = [sparql.unpack_row(row_result) for row_result in result]
                q_list = [qv for qv in q_values if 'ontology' in qv[0]]
                list_answers = [qvl[1] for qvl in q_list]
                q_list_answers = list(set(list_answers))
                return q_list, q_list_answers


def answer_lookup(answer_list,relation):
    # print answer_list1
    # answer_list = list(set(answer_list1))
    possible_answer_set = {}
    print relation
    for possible_answer in answer_list:
        # print possible_answer
        count = 0
        q_graph = ('SELECT distinct ?p ?o WHERE { {<' + possible_answer + '> ?p ?o} UNION {?o ?p <' + possible_answer + '> } '
                                                                                                                        'FILTER(STRSTARTS(STR(?p), "http://dbpedia.org/property") || STRSTARTS(STR(?p), "http://dbpedia.org/ontology")) '

                                                                                                              'FILTER(langMatches(lang(?o), "EN")).}')
        result = sparql.query(sparql_dbpedia_on, q_graph)
        q_values = [sparql.unpack_row(row_result) for row_result in result]
        q_list = [qv[1] for qv in q_values]
        # print q_list
        relation_all = [r[0] for r in relation]
        # print relation_all
        for vals in q_list:
            added_keyword = []
            # print vals
            count = 0
            for val in word_tokenize(vals):
                # print val
                # print count, len(relation_all)
                if val in relation_all and val not in added_keyword:
                    # print 'here'
                    count=count+1
                    added_keyword.append(val)

                if count==len(relation_all):
                    # print possible_answer
                    # print 'here'
                    if possible_answer not in possible_answer_set.keys():
                        possible_answer_set[possible_answer] = [vals]
                    else:
                        if vals not in possible_answer_set[possible_answer]:
                            possible_answer_set[possible_answer].append(vals)
    return possible_answer_set


