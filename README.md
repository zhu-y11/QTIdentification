# Question Type Identification(QTI)

This toolkit is used to identify question types, which consists of following types:

- **Who** question: the answer of the question should be a person or a group of people, but not concepts related to people, e.g. team or race.

- **When** question: concept of time, the duration or the moment.

- **What** question: the answer of the question should be intended for entities, objects except those for **who** and **when** questiont.

- **Affirmation**: closed question which can be answered either 'yes' or 'no'.

- **Unkown**: any other questions not falling in previous categories. 


## Settings

The stanford-parser is too big to upload. From [stanford-parser.zip](http://pan.baidu.com/s/1o7h0kRo) you could download zip file for a simpliefied stanford parser.
And the folder *stanford-parser* should be at the same level as *code* and *data* to run successfully.

## Data
The data is part of questions from the following link:

- [Question Classification Training Set 1](http://cogcomp.cs.illinois.edu/Data/QA/QC/train_1000.label) (For who, what, when and unknown question)
- [Question-Answer Dataset v1.2](http://www.cs.cmu.edu/~ark/QA-data/)(For closed question)

data is selected and labelled. There are 600 raw sentences in total in *data/raw/raw_questions/label*.


## Scripts
4 scripts included:

- code/preprocessing.py: preprocess raw data data/raw/raw_questions_label, output /data/questions_lebel which is used for testing, and /data/stats for statistics of the types of sentences. Every time questions_label will be shuffled.
- code/solutions.py: 4 solutions to the QTI problem
	1. Random Guess: random assign a label to a test sentence, and get average result of 20% (obviously).
	2. Majority Prediction: assign all data with the major type, which is **what**, get baseline of 45.8% (also obviously, 275 **what** questions).
	3. Regular expression without disambiguation: find the first token word in the sentence, and assign the sentence to the corresponding type label. For example, we would find the token word **how** for '*How old are you?*' and assign it to type **Unkown**, and find **what** for '*what time is it and how did you get here?*' and assign it to type **what**. We could get 93.17% accuracy. Any reasonable implementation should be higher than this baseline.
	4. Regular expression + syntactic analysis: we could notice that there are almost no disambiguations for **who** and **when**, and the disambiguations lie in the word *what* and *which*, which could also represent the concept of people and time. The methods could be described as follows:
	
````
0. Use stanford PCFG parser to parse all senteces;
1. For every sentence:
2. 		Use Regular Expression to identify head token word;
3. 		if token_word == wh_word #(i.e. what, who, how .....):
4. 			if foken_word = what or token_word = which:
5.    			if token_word is a deteminer and modify a noun in dependency tree:
6.    				#what actor, keyword = actor
7.    				keyword = the word token_word modify
8.    			if token_word is not a determiner but sentence is a BE-clause:
9.					#what is date today, keyword = date    
10.					keyword = the subject of the sentence
11.				if LeastCommonSynset(keyword.most_common_sense, synset(time_period.n.01)) = synset(time_period.n.01):    
12.      			return when type
13.	        	if LeastCommonSynset(keyword.most_common_sense, synset(measure.n.02)) = synset(measure.n.02):
14.             	return when type
15.         	if LeastCommonSynset(keyword.most_common_sense, synset(person.n.01)) = synset(person.n.01):
16.					return who type
17.         	if LeastCommonSynset(keyword.most_common_sense, synset(people.n.01)) = synset(people.n.01): 
18.             	return who type
19.         	return what type
20. 		return corresponding type according to method 3
21. return affirmation type	            
````
And we would get 97.17% accuracy for this method.

- code/evaluation.py: evaluate different solutions, and print out wrong cases.
- code/run.py: script to run preprocessing and evaluation in serial mode.

## Selected Wrong Cases
g for gold result and p for predicted result.
	
- g:1 p:2 What famous model was married to Billy Joel
- g:1 p:2 What 1920s cowboy star rode Tony the Wonder Horse
- g:2 p:1 Which Japanese car maker had its biggest percentage of sale in the domestic market

the word *model* and *star* for the most common sense are object rather than person, and maker vice versa.	

- g:2 p:3 What is the highest peak in Africa
- g:2 p:3 What is the quantity of American soldiers still unaccounted for from the Vietnam war

This is due to the synset of time, because some time concept has measure for the least common sense, other mearsure concept words could be considered as time.

- g:2 p:1 What relative of the racoon is sometimes known as the cat-bear
- g:2 p:1 What predators exist on Antarctica

This is due to the most common sense we use, which is misleading and need help of context. 

- g:2 p:3 What is Australia Day

This one is difficult, it is stating a concept rather than time, we also need help of context.

## Further Improvement

- Based on the errors, we should further check the modifers of the keyword. The modifier of relative is racoon, which is **what** type, conforming with the right answer. We leave it to the future work.
- Some wh words may be part of words using our regular expression such as however, somewhat, but since the sentence we use is a question, and we could always find the first and more proper wh word representing the question sentence.
- Here we decide to model **Unknown** type instead of **Affirmation** type, because we think it is easier and the auxilary words for **Affirmation** could be a lot. But logicaaly we ought to form tha latter first.
- We delete some impliacating questions in original corpus, like '*Name 10 of you favorite people.*' We think it is not a question because it will be deleted in preprocessing step if we hadle large corpus. But we could still model this type by investigating the object of the sentence.
- If we could get large amount of data, machine learning methods are to be taken using SVM or neural network for multi-classification with the context being a vector, and more features should be explored.

	
 





