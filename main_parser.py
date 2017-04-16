import csv, os , pprint
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

def question_parser(questions_list,id_list):
	print questions_list,id_list
	question_list = [word_tokenize(ques) for ques in questions_list]
	print question_list
	named_entities, pos_tags, dependency_parse = qt_tagger(question_list)
	for enitities in named_entities:
		entity = get_entity_nodes(enitities)
	resources = kb_query.resource_extractor(entity)
	print "Dbpedia Resources"
	print "================="
	pprint.pprint(resources)


def qt_tagger(question_list):
	ne_s = st_ner.tag_sents(question_list)
	pos_s = st_pos.tag_sents(question_list)
	dep_s = [[list(parse.triples()) for parse in dep_parse] for dep_parse in parser.parse_sents(question_list)]
	return ne_s, pos_s, dep_s

with open('question.csv') as f:
	reader = csv.DictReader(f)
	questions_list = []
	id_list = []
	for i,row in enumerate(reader):
		question = row['question']
		questions_list.append(row['question'])
		id_list.append(row['id'])
	question_parser(questions_list,id_list)