import os
import re
import nltk
import string
import random

filenames = ['s08_question_answer_pairs.txt', 
              's09_question_answer_pairs.txt',
              's10_question_answer_pairs.txt']
patterns = [ r'what\s?', r'which\s?', r'where\s?', r'when\s?', r'who\s?', r'how\s?', r'why\s?' ]
puncts = list(string.punctuation)
puncts.extend( ["``","''"] )
part_patterns = [ r'what\s?', r'which\s?' ]

outfilename = 'affirm_questions'
datafile = 'raw_questions_label'
outdatafile = 'questions_label'
stats = 'stats'

def AQExtraction():
    outfile = open( os.path.join( './raw/', outfilename ), 'w' ) 
    sentvec = set()
    for filename in filenames:
        infile = open( os.path.join( './raw/', filename ), 'r' )
        for line in infile:
            linevec = line.strip().split( '\t' )
            sent = linevec[1]

            if not sent.strip():
                continue

            if sent in sentvec:
                continue

            is_affirm = True
            #Eliminate all sentences containing tokens in patterns
            #Reserve other questions(possibly affimitive)
            for pattern in patterns:
                regex = re.compile( pattern, re.I )
                match = regex.search( sent )
                if match:
                    sentvec.add( sent )
                    is_affirm = False
                    break

            if not is_affirm:
                continue

            sentvec.add( sent )
            outfile.write( 'p' + '\t' + '4' + '\t' + sent + '\n' )

        infile.close()
    outfile.close()

def ProcData():
    infile = open( os.path.join( './raw/', datafile ), 'r' )
    outfile = open( outdatafile, 'w' )
    outstats = open( stats, 'w' )
    remark = infile.readline()
    outfile.write( remark )
    questions = []
    qtype = {}
    for line in infile:
        #Space 2 tab among tokens, but not among sentences
        linevec = line.strip().split( '\t' )
        #Conversion
        if len( linevec ) == 1:
            space1 = linevec[0].find( ' ' ) 
            space2 = linevec[0].find( ' ', space1 + 1 )
            linevec = [  linevec[0][0: space1],
                      linevec[0][space1 + 1: space2],
                      linevec[0][space2 + 1:] ]
        sent = linevec[-1]
        
        #Remove punctuations
        sentvec = [i for i in nltk.word_tokenize( sent ) if i not in puncts] 
        linevec[-1] = ' '.join( sentvec )
        
        if linevec[1] in qtype:
            qtype[linevec[1]] += 1
        else:
            qtype[linevec[1]] = 1

        line = '\t'.join( [linevec[1], linevec[2]] )
        questions.append( line )
    infile.close()
    
    #shuffle the questions
    random.shuffle( questions ) 
    for question in questions:
        outfile.write( question + '\n' )
    outfile.close()

    #output statistics
    outstats.write( 'Total' + '\t' + str( len( questions ) ) + '\n' )
    outstats.write( 'Unknown' + '\t' + str( qtype['0'] ) + '\n' )
    outstats.write( 'Who' + '\t' + str( qtype['1'] ) + '\n' )
    outstats.write( 'What' + '\t' + str( qtype['2'] ) + '\n' )
    outstats.write( 'When' + '\t' + str( qtype['3'] ) + '\n' )
    outstats.write( 'Affirmation' + '\t' + str( qtype['4'] ) + '\n' )
    outstats.close()

        
if __name__ == '__main__':
    os.chdir( '../data/' )         
    #AQExtraction()
    ProcData()

