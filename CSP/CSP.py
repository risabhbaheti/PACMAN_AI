import time
import Queue
'''q = Queue.Queue()
q._put(5)'''
allDifs = set()     #global list of shared diffs between node(should be unique)
count = 0

#checks diff b/w 2 values to see if they exist in allDIfs
def checkConstraintVals(x,y):
    global allDifs
    if x==y:
        return False
    if abs(x-y) in allDifs:
        return False
    return True
#checks one value in tail(x) against head node. Returns true if value found
def checkConstraint(x,headDomain):
    result = False
    for y in headDomain:
        result = checkConstraintVals(x,y)
        if(result == True):
            return True
    return False

#Removes nodes in tail node corresponding to which inconsistencies found in the head
def removeInconsistentalues(tail,head,domains):
    removed = False
    headDomain = domains[head]
    tailDomain = domains[tail]
    for x in tailDomain.copy():
        result = checkConstraint(x,headDomain)
        if result == False:
            tailDomain.remove(x)
            removed = True
    return removed, tailDomain

'''AC3 algorithm to reduce domain values'''
def AC3(assignments,domains,m,l):
    
    queue = Queue.Queue()
    #print domains
    assignedIndex = len(assignments) - 1
    for i in xrange(m):
        for j in xrange(m):
            if i!=j:
                if(j>assignedIndex):
                    queue.put((i,j))
    while not queue.empty():
        head, tail = queue._get()
        removed, newTailNode =  removeInconsistentalues(tail,head,domains)
        if removed:
            domains[tail] = newTailNode
            for i in xrange(m):
                if i > assignedIndex and i != tail:
                    queue.put((tail, i))
    #print domains
    return domains


def backTrackUsingAC3(assignments,domains,m,l):
    global allDifs
    global count
    if len(assignments) == m:
        return True, assignments
    domain_copy = domains[:]
    domains_new = AC3(assignments[:],domain_copy,m,l)
    for i in xrange(m):
        if len(domains_new[i]) == 0:
            return False, assignments
    
    currentIndex = len(assignments)
    #print assignments
    oldDomainValue = domains_new[currentIndex]
    domain_new_copy = []
    maxi = -1
    if(len(assignments) >0):
        maxi = assignments[len(assignments)-1]
    for indSet in domains_new:
        domain_new_copy.append(indSet.copy())
    for i in oldDomainValue.copy():
        if(i>maxi):
            newDomainValue = set()
            newDomainValue.add(i)
            domains_new[currentIndex] = newDomainValue
            newDiffs = []
            for assignment in assignments:
                newDiffs.append(abs(i - assignment))
            for k in newDiffs:
                allDifs.add(k)
            count+=1
            assignments.append(i)
            result,newAssignment = backTrackUsingAC3(assignments[:],domains_new,m,l)
            #print domain_new_copy
            if result == True:
                return True, newAssignment
            else:
                domains_new = []
                for i in domain_new_copy:
                    domains_new.append(i.copy())
                #print assignments
                assignments = assignments[0:len(assignments)-1]
                for k in newDiffs:
                    allDifs.remove(k)
    return False, None

    
def CP(l,m):
    if m==0:
        return -1,[]
    global count
    global allDifs
    assignments = []
    domain = set()
    for i in xrange(l+1):
        domain.add(i)
    domains = []
    for i in xrange(m):
        domains.append(domain)
    count =0
    result, assignment = backTrackUsingAC3(assignments,domains,m,l)
    #print "Count",count
    if(result):
        llimit = m*(m-1)/2
        for i in range(llimit,l,1):
            assignments = []
            domain = set()
            for j in xrange(i+1):
                domain.add(j)
            domains = []
            for k in xrange(m):
                domains.append(domain)
            allDifs = set()
            result, aval = backTrackUsingAC3(assignments,domains,m,i)
            if result:
                #print "Optimal Count", count
                #print aval
                #print i
                return i,aval
        return l,assignment
    else:
        print "No result"
        return -1,[]




'''
Pair wise computes and checks values in the assignments list for all values of differences
and checks their uniqueness. The newVal variable is the next assignment
'''
def checkConsistency(assignments, newVal):
    if(len(assignments)==0):  #if all markers assigned, return True
        return True
    i = 0
    while(i<len(assignments)):
        if(newVal == assignments[i]):
            return False
        i+=1
    else:
        diffsTaken = set()
        i = 0;
        #Pair-wise constraint check of assignment
        while(i<len(assignments)-1):
            j=i+1
            while(j<len(assignments)):
                vali = assignments[i]
                valj = assignments[j]
                diff = abs(valj - vali)
                if diff in diffsTaken:
                    return False
                else:
                    #HashSet of stored differences
                    diffsTaken.add(diff)
                j+=1
            i+=1
        i = 0
        #comparing stored vals with newVal
        while(i<len(assignments)):
            diff = abs(newVal - assignments[i])
            if diff in diffsTaken:
                return False
            diffsTaken.add(diff)
            i+=1
    return True


def recursiveBtSearch(assignments,domain,m,l, lastVal):
    global count
    if len(assignments) == m:
        return True, assignments
    else:
        i = lastVal+1
        while(i<=l):
            count = count +1
            allowed = checkConsistency(assignments, i)              #Checking for consisiteny of i
            if(allowed):
                leng = len(assignments)                             #If i is consistent add it to assignment list
                assignments.append(i)
                #print assignments
                result, retAssignments = recursiveBtSearch(assignments, domain, m, l,i)         #Recursive call to the function
                if(result == True):
                    return result, retAssignments
                else:
                    assignments = assignments[0:leng]
            i+=1
    return False, None

def BT(l,m):
    if m==0:
        return -1,[]
    global count
    assignments = []
    domain = []
    t1=time.time()
    count =0
    for i in xrange(l+1):
        domain.append(i)
    result, assignment = recursiveBtSearch(assignments,domain,m,l,-1)
    #print "count",count
    if(result):
        llimit = m*(m-1)/2
        for i in range(llimit,l,1):
            assignments = []
            domain = []
            for j in xrange(i+1):
                domain.append(j)
            result, aval = recursiveBtSearch(assignments,domain,m,i,-1)
            if result:
                #print "Optimal Count", count
                #t2 = time.time()
                #print "Bt time"
                #print t2-t1
                #print aval
                #print i
                return i,aval
        return l,assignment
    else:
        print "No result"
        return -1,[]
    
def checkFCConsisiteny(assignments, domain, difDict,lenDifDict,i,m):
    domainTemp = [val for val in domain]                            #Copy of domain
    if(len(assignments)==0):                                        #For case of empty assignment
        varList =[0]
        difDict[i]= varList
        lenDifDict[i]=varList
        domain.remove(i)
        return True,domain
    difInt =[]                                                      #List to store all unique edges 
    valList =[]                                                     #List that will store values removed from domain because of this value of assignment
    lenDifList=set()                                                #Set of edges generated by this assignment                      
    for key in lenDifDict.keys():                                   
        difInt = difInt + list(lenDifDict[key])
    
    for assgn in assignments:
        lenDifList.add(abs(i-assgn))
    difInt = difInt + list(lenDifList)                              
    for val in difInt:                                              #Removing the values whose edge length are +,- to the new assignment value
        addVal = i+val
        subVal = i-val
        if addVal in domain:
            domain.remove(addVal)
            valList.append(addVal)
        if subVal in domain:
            domain.remove(subVal)
            valList.append(subVal)
    
    if 2*i in domain:
        domain.remove(2*i)
        valList.append(2*i)
        
    if(len(domain)==0):
        if(len(assignments)==(m-1)):
            difDict[i]=valList
            lenDifDict[i] = lenDifList
            return True,domain
        domain = domainTemp
        return False,domain
    
    lenDifDict[i] = lenDifList                                          #Updating the dictionary with the respective values for the assignment i
    difDict[i]=valList
    return True,domain

        
def recursiveBtFCSearch(assignments,domain,difDict,lenDifDict,m,l,lastVal):
    global count
    if len(assignments) == m:
        return True, assignments
    else:
        i = lastVal + 1
        #Domain to be used when i >l
        recoveredDomain =[]
        
        while(i<=l):
            if i in domain:
                count = count +1
                allowed,recoveredDomain = checkFCConsisiteny(assignments, domain, difDict,lenDifDict,i,m)  #Checking consistency for i
                if(allowed):
                    leng = len(assignments)                                 #If consisitent we add i to assignment list and call the recursive function
                    assignments.append(i)

                    result, retAssignments = recursiveBtFCSearch(assignments, domain[:],difDict,lenDifDict, m, l,i)     #Recursive call
                    if(result == True):
                        return result, retAssignments
                    else:
                        domainVal = difDict[i]
                        domain= list(set(domain + domainVal +  recoveredDomain))            #Updating the domain so that it contains the value for the level
                        lenDifDict.pop(i,None)                                              #Popping the value of i to be removed so that we can go back one level
                        difDict.pop(i,None)                                                 #Popping the value of i to be removed so that we can go back one level
                        assignments = assignments[0:leng]                                   #Removing the last value from assignment list                                   
                else:
                    domain = recoveredDomain
            i = i+1
    return False, None

def FC(l,m):
    if m==0:
        return -1,[]
    global count
    assignments = []
    domain = []
    t1 = time.time()
    #Initializng domain
    for i in xrange(l+1):
        domain.append(i)
    difDict = {}
    lenDifDict = {}
    count =0
    result, assignment = recursiveBtFCSearch(assignments,domain,difDict,lenDifDict,m,l,-1)
    #print "count",count
    if(result):
        llimit = m*(m-1)/2                                                              #If a solution exists looping through to get least L
        for i in range(llimit,l,1):
            assignments = []
            domain = []
            for j in xrange(i+1):
                domain.append(j)
            difDict = {}
            lenDifDict = {}
            result, aval = recursiveBtFCSearch(assignments,domain,difDict,lenDifDict,m,i,-1)
            if result:
                #print "Optimal Count", count
                #t2 = time.time()
                #print "FC time",t2-t1
                #print i,aval
                return i,aval
        return l,assignment
    else:
        print "No result"
        return -1,[]

count =0



