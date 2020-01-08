'''Alice Dini - 830931'''
'''5 May 2019 - Assignment'''

def PowerSet(mainset):
    '''This function returns all the subset of a set: at every
    iteration excludes the last element of the set, and computes
    the power set of the remaining items; then this latter is
    concatenated to all the subsets everytime obtained.
    Since at every recursive iteration it considers decreasing
    prefixes of a mainset, the recursion will stop as soon as
    the original set contains only 1 element.'''
    
    if not mainset: return [[]]
    elif len(mainset) == 1: return [mainset, []]
    else:
        reduced = PowerSet(mainset[:-1])
        rest = []
        for i in reduced:
            rest += [i + [mainset[-1]]]
        return reduced + rest

def ExhaustiveSearch(m, n, S, U):
    '''Given m and n integers, and S, U two lists of length m, it computes the most valuable
    set that fits size n exhaustively exploring the search space.'''
    
    subsets = PowerSet([i for i in range(m)])
    candidate, maxUtility = (set(),0)
    for D in subsets: 
        currentUtility, currentSize = (0, 0)
        for i in D:
            currentUtility += U[i]
            currentSize += S[i]
        if currentSize <= n and currentUtility >= maxUtility:       #It is important to check as first condition the size requirement.  
            maxUtility = currentUtility
            candidate = D
    return set(candidate)

def Skip(node, k):
    '''Skips the subtree rooted at (node).
    i is set to the index of the last position in the node, and if the
    value at that position is less than k, it gets updated;
    otherwise, the penultimate value is updated, and
    the node up to that penultimate value will be the next one to
    be checked.'''
    
    i = len(node) - 1                                        
    if node[i] < k:
        node[i] += 1
        return node
    else:
        node[i-1] += 1
        if node[:i] == []:
        return node[:i]

def Continue(node, k):
    '''Takes a node and returns the next node to be checked in the tree.
    i takes as value the index of the last position in the node: if the node
    has not yet reached k, appends to the node the last value incremented by 1,
    going down by 1 level in the tree, and hence incrementing also the
    length (size) of the subset considered; otherwise, the penultimate
    value is increased by 1, an the next node to be checked will be the one
    ending with that penultimate value, meaning that it goes upward in the tree
    to lead a new possible subtree, from a new node. '''
    
    i = len(node) - 1
    if node[i] < k:
        node += [node[i] + 1] 
        return node
    else:
        node[i-1] += 1
        if node[:i] == []:
        return node[:i]

def BranchAndBoundSearch(m, n, S, U):
    '''Given m and n integers, and S, U two lists of length m, it computes the most valuable
    set that fits size n. The first node from which the tree describing the search space
    is rooted corresponds to the first element in the m items, and we initialize it.'''
    
    if m == 0: return []
    else:
        k = m-1                                         #In Python, ranges start at 0, so the maximum element of an indexed list with m elements would be m-1.            
        maxUtility, bestSet = (0, set())
        node = [0]                     
        while len(node) != 0:
            print(node)
            currentSize, currentUtility = (0, 0)
            for i in node:
                currentSize += S[i]
                currentUtility += U[i]
            if currentSize <= n:
                if currentUtility > maxUtility:
                    maxUtility = currentUtility
                    bestSet = node[:]                   #This avoids the assignment of bestSet to node itself, providing a new object.
                node = Continue(node, k)
            else: node = Skip(node, k)
        return set(bestSet)

import random, cProfile
'''These routines test the results provided by both the solutions, and their
    equivalence. If two or more datasets have the same utility,
    the result may vary. Since the returned values of ExhaustiveSearch
    and BranchAndBoundSearch have been converted to sets, the comparison
    will not take care about the order in which the integers are found.'''

def test3():
    m = random.choice((5, 10, 15, 20, 25))
    S = [random.randint(1, 10) for i in range(m)]
    U = [random.randint(1, 10) for i in range(m)]
    n = 3*m
    A = ExhaustiveSearch(m, n, S, U,)
    print(A)
    B = BranchAndBoundSearch(m, n, S, U)
    print(B)
    return A == B

def test7():
    m = random.choice((5, 10, 15, 20, 25))
    S = [random.randint(1, 10) for i in range(m)]
    U = [random.randint(1, 10) for i in range(m)]
    n = 7*m
    A = ExhaustiveSearch(m, n, S, U,)
    B = BranchAndBoundSearch(m, n, S, U)
    return A == B

def tester():
    true = 0
    for i in range(50):
        if test3():
            true +=1
        if test7():
            true +=1     
    return true
   

m = 10
S = [random.randint(1, 10) for i in range(m)]
U = [random.randint(1, 10) for i in range(m)]
n = 7*m
print(BranchAndBoundSearch(m, n, S, U))
                
    
