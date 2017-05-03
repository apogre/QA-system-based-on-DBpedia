#!/usr/bin/python
import sys
correct_ans=0
empty_ans=0
incorrect_ans=0

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
			if answers[0][-1] == '\r':
                                answers[0] = answers[0][:-1]
			if answers[0][-2:-1] == '\r\n':
				print "RN found"
				answers[0] = answers[0].replace(' ', '')[:-2]
			count = 0
			print "Corrected answers ***********", answers
			#print answers_dict_pred[id]
			if not answers_dict_pred[id]:
				print "The answer is empty"
				empty_ans = empty_ans + 1
				print "Missing ID: ",id
				print ""
			else:
				for values in answers_dict_pred[id]:
					print "Values in answers predicted are: ", values
					print answers
					if values in answers:
						print "The answer --", values, "-- is present in our local DB"
						count = count + 1
						#print "Correct ID: ",id
						break	
					#count = count + 1
				if count == 0:
					incorrect_ans = incorrect_ans + 1
					print "Incorrect ID: ",id
				else:
					correct_ans = correct_ans + 1
					print "Correct ID: ",id
				predict = ""
				if count > 1:
					predict = "1/" + str(count)
				else:
					predict = count
				#incorrect_ans = incorrect_ans + 1
				print "The prediction for this answer is: " , predict
print "Number of Correct Answers: ", correct_ans
print "Number of No Answers: ", empty_ans
print "Number of Incorrect Answers: ", incorrect_ans
