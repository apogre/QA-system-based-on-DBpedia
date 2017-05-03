#!/usr/bin/python
import csv, os , pprint, sys
from itertools import groupby
from nltk import word_tokenize
from nltk.tag import StanfordNERTagger,StanfordPOSTagger
from nltk.parse.stanford import StanfordDependencyParser

import kb_query

stanford_parser_jar = str(os.environ['HOME'])+'/stanford-parser-full-2015-12-09/stanford-parser.jar'
stanford_model_jar = str(os.environ['HOME'])+'/stanford-parser-full-2015-12-09/stanford-parser-3.6.0-models.jar'

st_ner = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz')
st_pos = StanfordPOSTagger('english-bidirectional-distsim.tagger')
parser = StanfordDependencyParser(path_to_jar=stanford_parser_jar, path_to_models_jar=stanford_model_jar)


def get_entity_nodes(netagged_words):
    ent = []
    for tag, chunk in groupby(netagged_words, lambda x:x[1]):
        if tag != "O":
            tuple1 =(" ".join(w for w, t in chunk),tag)
            ent.append(tuple1)
    return ent

def get_relation_nodes(netagged_words):
    ent = []
    for tag, chunk in groupby(netagged_words, lambda x:x[1]):
        if "NN" in tag:
            tuple1 =(" ".join(w for w, t in chunk),tag)
            ent.append(tuple1)
    return ent


def question_parser(questions_list,id_list):
	print questions_list,id_list
	question_list = [word_tokenize(ques) for ques in questions_list]
	print question_list
	named_entities, pos_tags, dependency_parse = qt_tagger(question_list)
	print pos_tags
	# print named_entities
	# sys.exit(0)
	global answerValue
	for i,enitities in enumerate(named_entities):
		print "Answering question with ID --", i, "--"
		# print enitities
		entity = get_entity_nodes(enitities)
		# print entity
		# print pos_tags
		print question_list[i]
		if entity:
			relation = get_relation_nodes(pos_tags[i])
			# print relation
			try:
				resources = kb_query.resource_extractor(entity)
				print "Dbpedia Resources"
				print "================="
				pprint.pprint(resources)
				q_list, q_list_answers = kb_query.graph_generator(resources,question_list[i][0])
				# print "Entity Graph"
				# print "============"
				# print q_list
				# print q_list_answers
				answer = kb_query.answer_lookup(q_list_answers,relation)
				print "----------$$$$$$$$$$$$$--------------------------------"
				#print answers
				#print answer
				keys = answer.keys()
				with open('Answers_predicted.csv','a') as f:
					f.write(str(id_list[i]) + ",")
					for key in keys:
  						#print(key)
						key1,key = key.split("http://dbpedia.org/resource/")
						#print key
						answerValue = key	
						print answerValue
						answer_data = "\"" + answerValue + "\","
						f.write(answer_data)
					f.write("\n")
				f.close()
				print "----------$$$$$$$$$$$$$--------------------------------"
				print "Answer: "+str(answer)
			except:
				print "sparql query error"
		else:
			print "Entity not Found"



def qt_tagger(question_list):
	ne_s = st_ner.tag_sents(question_list)
	pos_s = st_pos.tag_sents(question_list)
	dep_s = [[list(parse.triples()) for parse in dep_parse] for dep_parse in parser.parse_sents(question_list)]
	return ne_s, pos_s, dep_s

with open('question_testing.csv') as f:
	reader = csv.DictReader(f)
	questions_list = []
	id_list = []
	for i,row in enumerate(reader):
		question = row['question']
		questions_list.append(row['question'])
		id_list.append(row['id'])
	question_parser(questions_list,id_list)
