import copy

def simplex_algo():
   
    def drop_rows_and_columns(matrix):
        matrix = [row[1:] for row in matrix]
        matrix = matrix[2:]
        return matrix

    def print_matrix(matrix):
        for row in matrix:
            print("    ".join(map(str, row)))
        print('\n\n')

    def roundmatrix(m):
        for row in range(len(m)):
            for col in range(len(m[0])):
                m[row][col] = round(m[row][col],3)
        return m

    def sumColumn(A,col_index):
        sum = 0
        for i in range(len(A)):
            sum += A[i][col_index]
        return sum

    def phase2firstrow(A,col_index,c):    
        sum=0
        for i in range(len(A)):
            sum += A[i][col_index]*c[A[i][0]]
        return c[col_index-2]-sum
    
    def performOperations(T,pivotRow, pivotCol):
        pivotElement = T[pivotRow][pivotCol]
        for i in range(1,len(T)):
            if(i==pivotRow):
                continue
            u=(T[i][pivotCol]/pivotElement)
            for j in range(1,len(T[0])):
                T[i][j]-=u*T[pivotRow][j]
        for j in range(1,len(T[0])):
            T[pivotRow][j] = ((T[pivotRow][j])/(pivotElement))
            T[pivotRow][j] = T[pivotRow][j]
        T[pivotRow][0] = T[0][pivotCol]
        return T

    def read_input(filename):    
        with open(filename, 'r') as f:
            lines = f.readlines()
        objective = None 
        # 1 -> minimize 
        # -1 -> maximize
        A = []
        b = []
        c = []
        constraint_types = []
        neg_row = []
        cons_row = []
        num_constraints = 0
        decision_vars = 0
        slack_vars = 0
        myDict = {}
        mode = "objective"
        for line in lines:
            line = line.strip()
            if not line :
                continue
            if line == "[objective]" :
                mode = "objective"
                continue
            elif (line == "[A]"):
                mode = "A"
                continue
            elif line == "[b]":
                mode = "b"
                continue
            elif line == '[c]':
                mode = 'c'
                continue
            elif line == '[constraint_types]':
                mode = 'constraint_types'
                continue
            elif mode == "objective":
                if(line.lower() == "maximize"):
                    objective = -1
                else:
                    objective = 1
            elif mode == "A":
                row_entries = line.split(',')
                decision_vars = len(row_entries)

                row_entries = [float(x) for x in row_entries]
               
                A.append(row_entries)
            elif mode == "b":
                b.append(float(line))
                if (float(line) < 0):
                    neg_row.append(1)
                else:
                    neg_row.append(0)
            elif mode == "c":
                row_entries = line.split(',')
                c = [float(x) for x in row_entries]
            elif mode == "constraint_types":
                if (line == ">="):
                    cons_row.append(-1)
                elif (line == "="):
                    cons_row.append(0)
                else:
                    cons_row.append(1)
        

        decision_vars = len(A[0])
        num_constraints = len(neg_row)

        for i in range(len(neg_row)):
            if neg_row[i]:
                A[i] = [-x for x in A[i]]
                b[i] = - b[i]
                cons_row[i] = -cons_row[i]
        
        c = [x*objective for x in c]

        for i in range(num_constraints):
            if (cons_row[i] != 0):

                slack_vars += 1
                for j in range (num_constraints):
                    if j == i:
                        A[j].append(cons_row[i])
                    else:
                        A[j].append(0)
        

        for i in range(slack_vars):
            c.append(0)
        
        for i in range(decision_vars):
            myDict[i] = "decision_vars"
        
        for i in range(decision_vars,decision_vars + slack_vars):
            myDict[i] = "slack_vars"
        
        return A,b,c,myDict,objective

    def phase_I(A, b, myDict):

        valid = 0 # valid = 1, if LP is infesaible, valid = 0 otherwise;
        num_vars = len(A[0])
        num_constraint = len(b)
        aux_vars = num_constraint

        c = [0 for i in range(num_vars)]

        for i in range(aux_vars):
            c.append(1)
        
        for i in range(num_vars, aux_vars + num_vars):
            myDict[i] = "auxillary_vars"

        for i in range(num_constraint):
            for j in range(num_constraint):
                if (i == j):
                    A[j].append(1)
                else:
                    A[j].append(0)


        row1 = [0, 0] 
        for i in range(aux_vars + num_vars):
            row1.append(i)
        
        ctx = 0
        for value in b:
            ctx += value

        row2 = [0,-ctx]
        

        for i in range(num_vars):
            row2.append(-sumColumn(A,i))

        for i in range(num_vars, num_vars + aux_vars):
            row2.append(0)
        
        T = [[(f'x_{i}_{j}') for i in range(aux_vars + num_vars + 2)] for j in range(num_constraint + 2)]
        T[0] = row1
        T[1] = row2

        for i in range(2,num_constraint + 2):
            T[i][0] = num_vars + i - 2
            T[i][1] = b[i-2]
                

        for j in range(2, num_vars + aux_vars + 2):
            for i in range(2, num_constraint+2):
                T[i][j] = A[i-2][j-2]



        iteration_max = 100000
        i = 0
        # 0 --> fes  1 --> unfes 
        status = 0

        while(True and i < iteration_max):
            i+=1

            pivotColList = []
            for col in range(2, num_vars + aux_vars + 2):
                if(T[1][col] < 0):
                    pivotColList.append(col)
            
            if(len(pivotColList) == 0):
                #all reduced costs were postive:
                break
            
            pivotCol = -1
            postiveFound = False
            
            for colIndex in pivotColList:
               
                for i in range(2,num_constraint+2):
                    if(T[i][colIndex]>0):
                        pivotCol = colIndex
                        postiveFound = True
            
            
            if(postiveFound == False):
                status =1 
                break
        
            minValue = 1e10
            minIndex = -1

            for row in range(2,num_constraint + 2):

                if(T[row][pivotCol] <= 0):
                    continue
                
                ratio = ((T[row][1])/(T[row][pivotCol]))
                ratio = ratio
                if(ratio < minValue):
                    minValue = ratio
                    minIndex = row


            if(minIndex == -1):
                # all were non postive, and infes
                status = 1
                break
            
            pivotRow = minIndex
            
            T = performOperations(T,pivotRow,pivotCol)

        if(status == 1):
            pass
            # print("LP is infeasible status 1")

        elif(status == 0 and T[1][1] == 0):
            valid=1
            pass
            # print("basic feasible solution found , drive out aux vars")

        elif(status == 0 and T[1][1] < 0):
            pass
            # print("LP is infeasible status 0 cost > 0")

        else:
            pass


        #driving out auxillary vairables:
        i=2
        while(i<num_constraint+2):
            # print("we reached i = ",i)
            if(myDict[T[i][0]]=="auxillary_vars"):
                operation_performed=False
                for j in range(2,num_vars+2):
                    if(T[i][j]!=0):
                        performOperations(T,i,j)
                        operation_performed=True
                        break
                if(operation_performed==False):
                    T.pop(i)
                    i-=1
                    num_constraint-=1
            i+=1
        result = [row[:num_vars+2] for row in T[2:]]

        return result,valid

    #//PHASE2 

    A,b,c,myDict,objective = read_input("input.txt")
    base_matrix,valid = phase_I(A,b,myDict)
    
    first_row=[0]
    for  i in range(1,len(base_matrix[0])):
        first_row.append(phase2firstrow(base_matrix, i, c))
    base_matrix.insert(0,first_row)

    second_row=[0,0]
    for i in range(2, len(base_matrix[0])):
        second_row.append(i-2)
    base_matrix.insert(0,second_row)

    initial_matrix = copy.deepcopy(base_matrix)

    ansDict = {}
    ansDict["initial_tableau"] = drop_rows_and_columns(roundmatrix(initial_matrix))


    if(valid==1):
    
        iteration_max = 100000
        i = 0
        # 0 --> fes  1 --> unfes 
        status = 0

        while(True and i < iteration_max):

            i+=1

            pivotColList = []
    
            
            for col in range(2, len(base_matrix[0])):
                if(base_matrix[1][col] < 0):
                    pivotColList.append(col)
            

            if(len(pivotColList) == 0):
                #all ci >=0, optimal solution found!
                break
            
            pivotCol = -1
            positiveFound = False

            for colIndex in pivotColList:
                for i in range(2,len(base_matrix)):
                    if(base_matrix[i][colIndex]>0):
                        pivotCol = colIndex
                        positiveFound=True
                
            if(positiveFound == False):
                status = 1
                break


            minValue = 1e10
            minIndex = -1

            for row in range(2,len(base_matrix)):
                    
                if(base_matrix[row][pivotCol] <= 0):
                    continue
                    
                ratio = ((base_matrix[row][1])/(base_matrix[row][pivotCol]))
                if(ratio < minValue):
                    minValue = ratio
                    minIndex = row


            if(minIndex == -1):
                # all were non postive, and unbded
                status = 1
                break
            
            pivotRow = minIndex
            
            base_matrix = performOperations(base_matrix,pivotRow,pivotCol)
         

        if(status == 1):
            ansDict["final_tableau"]= drop_rows_and_columns(roundmatrix(base_matrix))
            ansDict["solution_status"] = "unbounded"
            ansDict["optimal_solution"]= None
            ansDict["optimal_value"] = None
            
        

        elif(status == 0):

            ansDict["final_tableau"]= drop_rows_and_columns(roundmatrix(base_matrix))
            ansDict["solution_status"] = "optimal"

            solution = [0] * (len (base_matrix[0]) - 2)

            for i in range (len(base_matrix) - 2):
                solution[base_matrix[i + 2][0]] = base_matrix[i+2][1]
            
            final_values = []
            for i in range(len(solution)):
                if(myDict[i]=="decision_vars"):
                    final_values.append(solution[i])
            
            ansDict["optimal_solution"] = final_values
            ansDict["optimal_value"] =  -objective*base_matrix[1][1]

        else:
            pass



    elif(valid == 0):
        ansDict["final_tableau"]= drop_rows_and_columns(roundmatrix(base_matrix))
        ansDict["solution_status"] = "infeasible"
        ansDict["optimal_solution"]= None
        ansDict["optimal_value"] = None

    return ansDict
