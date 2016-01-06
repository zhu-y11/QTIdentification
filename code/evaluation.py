import os
import solutions

sol_filename = None
gold_list = []
total = 0


def EvalSol( sol_num ):
    if sol_num == 1:
        solutions.Sol1()
    elif sol_num == 2:
        solutions.Sol2()
    elif sol_num == 3:
        solutions.Sol3()
    elif sol_num == 4:
        solutions.Sol4()

    idx = 0
    rt = 0
    wrong_list = [] 
    if os.path.isfile( sol_filename ):
        infile = open( sol_filename, 'r')
        for line in infile:
            if line.startswith( '#' ):
                continue

            linevec = line.strip().split( '\t' )
            if linevec[1] != gold_list[idx][1]:
                print 'Sentence not aligned!'
                break

            if linevec[0] == gold_list[idx][0]:
                rt += 1
            else:
                print ( 'g:' + gold_list[idx][0] + ' p:' + linevec[0] + ' ' + linevec[1] )
                wrong_list.append( idx + 2 )
            idx += 1

        print ( 'Solution ' + str( sol_num ) + ': Accuracy = ' + str( rt / total ) )
        #print wrong_list
    else:
        print sol_filename + ' not exists!!'


if __name__ == '__main__':
    os.chdir( '../data/' )
    #Read gold setences into list
    infile_gold = open( 'questions_label', 'r' ) 
    for line in infile_gold:
        if line.startswith( '#' ):
            continue
        linevec = line.strip().split( '\t' )
        gold_list.append( ( linevec[0], linevec[1] ) )
    infile_gold.close()
    total = len( gold_list ) * 1.0

    #Solution 1: Random Guess   
    sol_filename = solutions.out_filename + '_1' 
    EvalSol( 1 )

    #Solution 2: Majority Prediction   
    sol_filename = solutions.out_filename + '_2' 
    EvalSol( 2 )

    #Solution 3: Without Disambiguation  
    sol_filename = solutions.out_filename + '_3' 
    EvalSol( 3 )  
    
    sol_filename = solutions.out_filename + '_4' 
    EvalSol( 4 )
