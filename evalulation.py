#!/usr/bin/python
import sys

answers_dict_pred = {}
with open('Answers_predicted.csv','r') as f:
	for line in f:
		if line != "\n":
			answers = []
			answers = line.split(',')
			id = answers[0]
			if answers:
				answers.pop(0)
			if answers:
				answers.pop(-1)
			print "ID: ",id
			print "Answers: ", answers
			answers_dict_pred[id] = answers
print "Answers!!!"
print answers_dict_pred
print "All the answers!!!"
with open('answers_act.csv','r') as f:
        for line in f:
                if line.split(',')[0] in answers_dict_pred.keys():
			print "***Key found***"
                        answers = []
                        answers = line.split(',')
                       	id = answers[0]
                        if answers:
                                answers.pop(0)
			if answers[0][-1] == '\n':
				answers[0] = answers[0][:-1]
			count = 0
			
			print answers_dict_pred[id]
			for values in answers_dict_pred[id]:
				print "Values in answers predicted are: ", values
				print answers
				if values in answers:
					print "The answer --", values, "-- is present in our local DB"
					count = count + 1
					break	
				count = count + 1
			predict = ""
			if count > 1:
				predict = "1/" + str(count)
			else:
				predict = count
			print "The prediction for this answer is: " , predict
