import os
import re
import random
import preprocessing
import subprocess
from nltk.corpus import wordnet as wn

os.chdir('../data/')
filename = 'questions_label' 
out_filename = 'pred_questions_label'
patmap = { r'what\s?': '2', r'which\s?': '2', r'when\s?': '3', r'who\s?': '1', r'where\s?': '0', r'how\s?': '0', r'why\s?':'0' }

#Random Guess
def Sol1():
    infile = open( filename, 'r')
    outfile = open( out_filename + '_1', 'w' )
    remark = infile.readline()
    outfile.write( remark )
    rd = random.Random()
    #seed could be fiexed to reimplement the accuracy
    rd.seed()
    for line in infile:
        sent = line.strip().split('\t')[-1]
        outfile.write( str( rd.randint( 0, 4 ) ) + '\t' + sent + '\n' )

    infile.close()
    outfile.close()

#Majorith Prediction
def Sol2():
    infile = open( filename, 'r')
    outfile = open( out_filename + '_2', 'w' )
    remark = infile.readline()
    outfile.write( remark )
    for line in infile:
        sent = line.strip().split('\t')[-1]
        outfile.write( '2' + '\t' + sent + '\n' )

    infile.close()
    outfile.close()

#Without Disambiguation
def Sol3():
    infile = open( filename, 'r')
    outfile = open( out_filename + '_3', 'w' )
    remark = infile.readline()
    outfile.write( remark )
    patterns = preprocessing.patterns

    for line in infile:
        sent = line.strip().split('\t')[-1]

        is_affirm = True
        matches = {}
        for pattern in patterns:
            regex = re.compile( pattern, re.I )
            match = regex.search( sent )
            if match:
                matches[match.start()] = pattern
                is_affirm = False

        if is_affirm:
            outfile.write( '4' + '\t' + sent + '\n' )
        else:
            #Find the first pattern in the sentence
            min_key = min( matches.keys() )
            outfile.write( patmap[matches[min_key]] + '\t' + sent + '\n' ) 

    infile.close()
    outfile.close()


def Disamb( sent, parselist ):
    patterns = preprocessing.patterns
    part_patterns = preprocessing.part_patterns

    #Find the very first wh word
    is_affirm = True
    matches = {}
    for pattern in patterns: 
        regex = re.compile( pattern, re.I )
        match = regex.search( sent )
        if match:
            matches[match.start()] = ( pattern, match.group().strip() )
            is_affirm = False
    
    #Found wh word
    if not is_affirm:
        min_key = min( matches.keys() )
        min_pattern = matches[min_key][0]
        #Not which or what, but some other word: how, who, when ...
        if min_pattern not in part_patterns:
            return patmap[matches[min_key][0]] 
    
        #Found a what or which
        keywh = matches[min_key][1]
        #if keywh modifies someword, that word is the keyword
        # e.g. What actor
        modregex = re.compile( 'det\(\S+\s%s'%keywh )
        modmatch = modregex.search( parselist[1] )
        #not a modifier, a be-clause, subject is concept
        subjregex = re.compile( 'nsubj\(%s\S+\s\S+'%keywh )
        subjmatch = subjregex.search( parselist[1] ) 

        #modmatch has priority
        if modmatch or subjmatch:
            keyword = None
            if modmatch:
                keyword = modmatch.group()[4:modmatch.group().rfind('-')]
            elif subjmatch:
                keyword = subjmatch.group()[subjmatch.group().find(', ') + 2: subjmatch.group().rfind('-')]

            #Concetp of time
            if keyword == 'time':
                return '3'
            keyword_synset = wn.synsets( keyword )
            if keyword_synset:
                time_synset = wn.synsets( keyword )[0].lowest_common_hypernyms(
                            wn.synset('time_period.n.01'))[0].name()
                if 'time' in time_synset or 'measure' in time_synset:
                    return '3'

                #Concept of people
                per_synset = wn.synsets( keyword )[0].lowest_common_hypernyms(
                           wn.synset('person.n.01'))[0].name()
                if 'person' in per_synset:
                    return '1'
                peo_synset = wn.synsets( keyword )[0].lowest_common_hypernyms(
                           wn.synset('people.n.01'))[0].name()
                if 'people' in peo_synset:
                    return '1'
            
        #no modifier, no subject,assign what
        return '2'
            
    else:
        return '4'

#Disambiguation
def Sol4():
    infile = open( filename, 'r')
    temp1 = open( 'temp1', 'w' )
    outfile = open( out_filename + '_4', 'w' )
    remark = infile.readline()
    outfile.write( remark )
    for line in infile:
        sent = line.strip().split('\t')[-1]
        temp1.write( sent + '?\n\n' )

    infile.close()
    temp1.close()

    #Call stanford parser 
    call_bash = subprocess.Popen(['../stanford-parser/lexparser.sh', './temp1'], shell = False,
                            stdout=subprocess.PIPE)
    output = call_bash.communicate()[0]
    temp2 = open( 'temp2', 'w' )
    temp2.write( output )
    temp2.close()


    temp2 = open( 'temp2', 'r' )
    infile = open( filename, 'r' )
    infile.readline()
    for sentline in infile:
        sent = sentline.strip().split( '\t' )[-1]
        spnum = 0
        parselist = ['', '']
        for parseline in temp2:
            if not parseline.strip():
                spnum += 1
                if spnum == 2:
                    break
                else:
                    continue

            parselist[spnum] += parseline
        label = Disamb( sent, parselist )
        outfile.write( label + '\t' + sent + '\n' )

    infile.close()
    temp2.close()
    outfile.close()
    os.remove( './temp1' )
    os.remove( './temp2' )


if __name__ == '__main__': 
    #Random Guess
    #Sol1()
    
    #Majority Prediction
    #Sol2() 
    
    #Without Disambiguation
    #Sol3()
    
    #Disambiguation
    Sol4()
