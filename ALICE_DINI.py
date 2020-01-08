'''Alice Dini - 830931'''
'''27 May 2019 - Assignment'''

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
        return node[:i]

def BranchAndBoundSetCover(m, n, S, P):
    '''Given m and n integers, and S, U two lists of length n where S
    contains subsets of {1, ..., m} and P contains positive integers,
    it computes the optimal set D of subsets in S which entirely
    covers {1,...,m} elements and whose overall cost is minimal.
    The size of D is at most n. 
    The first node from which the tree describing the search space
    is rooted corresponds to the first element in S,
    and we initialize it.'''
    
    A = set(range(1, m+1))
    S = [set(i) for i in S]
    if m == 0 or n == 0 or len(S) == 0 or len(P) == 0:
        return 'Error.'
    if len(S) != n or len(P) != n: return 'Error.'
    if set(e for s in S for e in s) != A: return 'Error.'
    D, bestPrice = [], sum(P)                               #By convention, since we have to minimize the overall price, we initialize the sum of all the subsets' prices.
    for i in range(n):                                      #Until we arrive at the end of S and P.
        k = n - 1                                           #In Python, ranges start at 0, so the maximum element of an indexed list with m elements would be m-1.
        node, price, covered = [i], P[i], S[i]              #Initialize the first node.

        '''Python rule: indexes start at 0, so even if A contains elements starting from 1,
        P and S mainain the mapping of the sets and correspondent prices with indexes pertaining
        to the set {0, ..., m-1}, hence since in nodes we find integers referring to subsets in S
        and prices in P, the first element will be denoted by 0 for example. Nevertheless,
        the program will output the sets as such and not the integers associated to them.
        Since the subsets in D can be at most n, we stop whenever the last element in the node is n-1
        otherwise, whenever we reach a node [i, n-1] it means a new branch, starting with a new
        integer, has to be initialized, since a leaf has been reached for that subtree.
        Nevertheless, whenever i == n - 1 the execution will end because
        the for loop traversed the whole possible set of subsets in S and prices in P.'''
        
        while node != [i, n-1] and node != [n - 1]:         #Lists, being mutable objects, are used for nodes.
            print(node)
            if price > bestPrice:                           #Bound: if the price is greater than the minimum found so far, skip that branch.
                node = Skip(node, k)  
                price = sum([P[i] for i in node])
                covered = set(k for i in node for k in S[i])
            else:
                if covered == A:
                    bestPrice = price
                    D = node[:]
                node = Continue(node, k)
                price = sum([P[i] for i in node])
                covered = set(k for i in node for k in S[i])
                
    '''Since indexes have been used to produce the result,
    Each set gets now fetched from S to be reported.'''
    
    return [set(S[i]) for i in D], bestPrice
                    
def GreedySetCover(m, n, S, P):
    '''Given m and n integers, and S, U two lists of length n where S
    contains subsets of {1, ..., m} and P contains positive integers,
    it computes the approximate set D of subsets in S which entirely
    covers {1,...,m} elements and whose overall cost is minimal.
    The size of D is at most n. '''

    A = set(range(1,m+1))
    if m == 0 or n == 0 or len(S) == 0 or len(P) == 0:
        return 'Error.'
    S = [set(i) for i in S]
    if len(S) != n or len(P) != n: return 'Error.'
    if set(e for s in S for e in s) != A: return 'Error.'
    D, bestPrice = [], 0
    covered = set()
    while covered != A:
        alpha = [Cost(P[i], S[i], covered) for i in range(len(S))]
        subset = alpha.index(min(alpha))
        #subset is a position, used to maintain the mapping between with S and P.
        covered = covered.union(S[subset])
        D.append(S[subset])
        bestPrice += P[subset]
        #The sets already considered get removed from S, and their price as well.
        S = S[:subset] + S[subset+1:]
        P = P[:subset] + P[subset+1:]
    return D, bestPrice


import math
def Cost(price, subset, covered):
    '''Cost computes the cost effectiveness of
    a subset, namely the distribution of its price
    among the uncovered elements.'''
    
    if len(subset.difference(covered)) > 0:
        return price / len(subset.difference(covered))
    else: return math.inf

'''Instances'''
'''Results:'''
'''
I) Branch-And-Bound ([{1, 2, 5}, {4}, {2, 3}], 23)
I) Greedy Algorithm ([{1, 2, 5}, {4}, {2, 3}], 23)
II) Branch-And-Bound ([{1, 3, 5, 8, 10, 11, 12, 15}, {1, 2, 4, 5, 6, 7, 9, 11, 13, 14, 15}], 20)
II)Greedy Algorithm ([{1, 2, 4, 6, 7, 11, 13, 14, 15}, {1, 3, 5, 8, 10, 11, 12, 15}, {3, 5, 6, 7, 8, 9, 12, 13, 14}], 21)
III) Branch-And-Bound([{1, 3, 4}, {2}, {1, 3, 5}], 16)
III) Greedy Algorithm([{1, 3, 4}, {2}, {1, 3, 5}], 16)
IV) Branch-And-Bound ([{2, 4, 5, 7, 13, 14, 15, 17, 20, 23, 24, 25, 27, 28, 29, 30, 34, 35}, {3, 5, 6, 10, 12, 14, 16, 17, 18, 19, 20, 22, 23, 24, 26, 28, 29, 30, 31, 32, 33, 34, 37, 39}, {1, 2, 5, 6, 8, 9, 10, 11, 12, 13, 14, 16, 20, 21, 26, 29, 30, 32, 33, 35, 36, 38, 39, 40}], 106)
IV) Greedy Algorithm ([{1, 2, 5, 6, 8, 9, 10, 11, 12, 13, 14, 16, 20, 21, 26, 29, 30, 32, 33, 35, 36, 38, 39, 40}, {3, 5, 6, 10, 12, 14, 16, 17, 18, 19, 20, 22, 23, 24, 26, 28, 29, 30, 31, 32, 33, 34, 37, 39}, {1, 2, 35, 37, 7, 39, 40, 12, 15, 17, 21, 24, 25, 27, 28, 30}, {3, 4, 9, 10, 14, 15, 17, 18, 19, 23, 24, 26, 28, 29, 30, 32, 34, 35, 38, 39, 40}], 122)
V) Branch-And-Bound ([{2, 5, 6, 7, 8, 9, 10, 13, 17, 19, 20, 21, 23, 24, 25, 27, 28, 29, 30}, {4, 7, 8, 9, 11, 12, 13, 14, 15, 16, 19, 20, 25, 26, 27, 28, 29, 30}, {1, 3, 5, 7, 8, 9, 18, 19, 20, 21, 22, 23, 26, 28, 29}], 138)
V) Greedy Algorithm([{4, 7, 8, 9, 11, 12, 13, 14, 15, 16, 19, 20, 25, 26, 27, 28, 29, 30}, {2, 5, 6, 7, 8, 9, 10, 13, 17, 19, 20, 21, 23, 24, 25, 27, 28, 29, 30}, {1, 3, 5, 7, 8, 9, 18, 19, 20, 21, 22, 23, 26, 28, 29}], 138)
'''

import cProfile
# First instance

m1 = 5
n1 = 10
S1 = [[1,3],[2],[1,2,5],[3,5],[4],[5],[1,3],[2,4,5],[1,2],[2,3]]
P1 = [11,4,9,12,5,4,13,12,8,9]
print(BranchAndBoundSetCover(m1, n1, S1, P1))
##print(GreedySetCover(m1, n1, S1, P1))
##cProfile.run('BranchAndBoundSetCover(m1, n1, S1, P1)')
##cProfile.run('GreedySetCover(m1, n1, S1, P1)')

# Second instance

m2 = 15
n2 = 45
S2 = [[2, 7, 8, 10, 12, 13], [1, 3, 5, 8, 10, 11, 12, 15], [1, 2, 3, 4, 5, 6, 7, 12, 13], [2, 6, 7, 11, 12, 13], [9, 10, 12, 13], [1, 3, 7, 9, 11, 12, 13], [1, 3, 5, 6, 8, 9, 10, 11, 12, 13], [1, 3, 4, 5, 6, 7, 12, 14, 15], [1, 2, 3, 6, 11, 12], [1, 2, 4, 5, 7, 8], [5, 9, 10, 11, 15], [3, 5, 6, 7, 8, 9, 12, 13, 14], [1, 3, 4, 5, 6, 7, 9, 11, 13, 14, 15], [1, 3, 5, 6, 8, 12, 14], [2, 4, 7, 9, 10, 12, 14], [1, 3, 5, 6, 11, 15], [2, 3, 4, 5, 6, 8, 10, 11, 12, 13, 14, 15], [1, 2, 4, 6, 7, 11, 13, 14, 15], [1, 2, 8, 12, 13, 14], [1, 2, 6, 7, 8, 13], [1, 2, 3, 5, 7, 8, 10, 12, 14, 15], [4, 5, 7, 12, 15], [1, 2, 3, 5, 11, 14], [1, 6, 8, 11, 13], [1, 6, 7, 8, 9, 10, 13], [1, 2, 3, 4, 5, 9, 11, 15], [2, 3, 4, 7, 9, 11, 12], [1, 3, 4, 5, 8, 10, 11, 12, 13], [2, 8, 9, 10], [6, 11, 13], [2, 5, 6, 8, 9, 11, 12, 13, 15], [2, 4, 6, 7, 8, 9, 10, 11, 13, 15], [1, 2, 3, 4, 5, 7, 8, 10, 11], [1, 2, 6, 9, 11, 13, 14, 15], [1, 4, 9, 10, 11, 13, 15], [1, 2, 3, 4, 6, 8, 12, 14, 15], [4, 5, 7, 8, 10, 13, 14], [2, 4, 8, 9, 11, 14], [2, 3, 4, 5, 6, 7, 10, 11, 14], [1, 2, 4, 5, 6, 7, 9, 11, 13, 14, 15], [1, 2, 6, 7, 9, 10, 12, 15], [1, 3, 6, 9, 10, 15], [2, 3, 5, 7, 8, 9, 11], [2, 3, 4, 5, 8, 10, 11, 12, 15], [1, 3, 4, 5, 6, 7, 9, 10, 12, 15]]
P2 = [16, 7, 16, 39, 29, 35, 19, 27, 27, 33, 38, 8, 41, 16, 12, 7, 41, 6, 34, 48, 23, 16, 31, 18, 35, 31, 41, 21, 50, 21, 12, 37, 35, 44, 48, 18, 14, 26, 22, 13, 29, 34, 28, 45, 50]
##print(BranchAndBoundSetCover(m2, n2, S2, P2))
##print(GreedySetCover(m2, n2, S2, P2))
##cProfile.run('BranchAndBoundSetCover(m2, n2, S2, P2)')
##cProfile.run('GreedySetCover(m2, n2, S2, P2)')

# Third instance

m3 = 5
n3 = 21
S3 = [[1], [1, 2, 3, 4, 5], [2, 3], [2, 3, 4, 5], [1, 3, 4], [5], [1, 2, 4], [1, 3, 4, 5], [3, 5], [4, 5], [3], [2, 5], [4], [1, 5], [2], [1, 2, 4], [1, 3], [1, 3, 5], [2, 4, 5], [2], [1, 2, 5]]
P3 = [44, 44, 39, 24, 5, 30, 26, 42, 28, 12, 6, 45, 37, 33, 5, 42, 26, 6, 38, 11, 28]
##print(BranchAndBoundSetCover(m3, n3, S3, P3))
##print(GreedySetCover(m3, n3, S3, P3))
##cProfile.run('BranchAndBoundSetCover(m3, n3, S3, P3)')
##cProfile.run('GreedySetCover(m3, n3, S3, P3)')

#Fourth instance

m4 = 40
n4 = 23
S4 = [[1, 3, 4, 6, 7, 9, 10, 15, 16, 18, 26, 31, 32, 35, 36, 38, 39, 40], [1, 2, 3, 4, 5, 7, 9, 11, 13, 15, 17, 18, 19, 20, 23, 24, 25, 27, 31, 32, 37, 39, 40], [4, 7, 8, 10, 11, 14, 16, 17, 18, 20, 23, 24, 27, 28, 29, 34, 36, 37, 39, 40], [2, 3, 4, 7, 9, 11, 17, 20, 22, 25, 26, 27, 28, 32, 34, 35, 36, 37, 39, 40], [1, 2, 4, 6, 7, 10, 12, 13, 22, 23, 24, 26, 28, 30, 32, 33, 35, 36, 39], [1, 3, 4, 5, 6, 8, 9, 10, 12, 13, 16, 24, 25, 30, 34, 35, 36, 37, 38, 39], [2, 3, 5, 10, 11, 12, 14, 18, 20, 22, 24, 25, 27, 28, 30, 31, 33, 34, 40], [1, 3, 11, 12, 18, 19, 21, 22, 24, 25, 26, 30, 33, 35], [1, 2, 7, 9, 10, 11, 14, 16, 18, 20, 22, 25, 28, 33, 35, 38], [3, 4, 9, 10, 14, 15, 17, 18, 19, 23, 24, 26, 28, 29, 30, 32, 34, 35, 38, 39, 40], [1, 2, 3, 4, 5, 6, 7, 9, 10, 13, 14, 15, 16, 19, 20, 22, 23, 29, 30, 31, 36, 38, 39], [2, 4, 5, 7, 13, 14, 15, 17, 20, 23, 24, 25, 27, 28, 29, 30, 34, 35], [1, 2, 4, 8, 9, 11, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 26, 27, 31, 32, 33, 34, 35, 36, 37, 39, 40], [1, 4, 5, 6, 8, 10, 14, 17, 20, 21, 23, 24, 25, 29, 30, 40], [3, 5, 6, 10, 12, 14, 16, 17, 18, 19, 20, 22, 23, 24, 26, 28, 29, 30, 31, 32, 33, 34, 37, 39], [2, 3, 5, 6, 7, 9, 14, 15, 16, 17, 20, 21, 23, 27, 28, 29, 31, 32, 34, 35, 39, 40], [2, 5, 7, 10, 11, 13, 14, 18, 20, 22, 23, 29, 32, 33, 34, 35, 38, 39], [1, 3, 6, 7, 8, 9, 10, 12, 13, 24, 29, 30, 33, 34, 35, 36, 37, 39, 40], [1, 2, 5, 6, 8, 9, 10, 11, 12, 13, 14, 16, 20, 21, 26, 29, 30, 32, 33, 35, 36, 38, 39, 40], [3, 4, 7, 8, 11, 14, 16, 17, 19, 20, 21, 22, 23, 24, 25, 26, 29, 30, 31, 33, 34, 36, 38, 39], [2, 3, 4, 6, 7, 9, 11, 13, 14, 15, 16, 19, 21, 24, 25, 26, 27, 28, 29, 30, 31, 33, 36, 39], [1, 2, 3, 6, 8, 10, 11, 13, 15, 16, 17, 19, 20, 21, 22, 25, 26, 34, 35, 36, 39, 40], [1, 2, 7, 12, 15, 17, 21, 24, 25, 27, 28, 30, 35, 37, 39, 40]]
P4 = [59, 68, 56, 50, 75, 95, 71, 66, 30, 28, 42, 50, 68, 34, 29, 52, 70, 85, 27, 40, 76, 82, 38]
##print(BranchAndBoundSetCover(m4, n4, S4, P4))
##print(GreedySetCover(m4, n4, S4, P4))
##cProfile.run('BranchAndBoundSetCover(m4, n4, S4, P4)')
##cProfile.run('GreedySetCover(m4, n4, S4, P4)')

# Fifth instance

m5 = 30
n5 = 23
S5 = [[2, 3, 4, 8, 9, 10, 11, 12, 15, 16, 18, 19, 22, 23, 24, 26, 27, 28, 29], [1, 2, 4, 5, 7, 8, 10, 11, 13, 16, 17, 19, 20, 21, 22, 23, 25, 27, 30], [1, 3, 9, 10, 16, 17, 18, 23, 24, 25, 26, 29, 30], [2, 4, 5, 6, 7, 10, 11, 12, 13, 14, 17, 20, 21, 22, 26, 27, 29, 30], [1, 6, 7, 11, 14, 17, 18, 23, 25, 26, 28, 29], [3, 5, 6, 7, 9, 10, 12, 13, 15, 16, 17, 18, 19, 21, 22, 24, 25, 26, 29], [2, 5, 6, 7, 8, 9, 10, 13, 17, 19, 20, 21, 23, 24, 25, 27, 28, 29, 30], [1, 5, 6, 8, 10, 19, 21, 24], [1, 3, 7, 8, 9, 10, 15, 19, 25, 26, 27, 30], [4, 5, 10, 11, 12, 13, 14, 16, 18, 20, 21, 22, 27, 28, 29], [1, 6, 7, 9, 17, 23, 26, 29, 30], [3, 4, 7, 8, 12, 13, 14, 15, 19, 21, 22, 24, 25, 27, 28, 29, 30], [1, 5, 6, 7, 8, 10, 15, 19, 21, 22, 27, 28, 29, 30], [1, 2, 4, 5, 6, 7, 8, 9, 11, 13, 14, 17, 19, 20, 23, 25, 26, 28, 30], [2, 3, 4, 9, 12, 15, 17, 20, 23, 26, 27, 28, 29], [4, 7, 8, 9, 11, 12, 13, 14, 15, 16, 19, 20, 25, 26, 27, 28, 29, 30], [1, 3, 5, 7, 8, 9, 18, 19, 20, 21, 22, 23, 26, 28, 29], [1, 3, 6, 7, 8, 10, 12, 13, 14, 16, 21, 23, 24, 25, 26, 27], [3, 5, 8, 9, 12, 13, 15, 18, 20, 21, 23, 24, 29], [1, 3, 4, 5, 8, 9, 10, 14, 15, 16, 18, 19, 20, 21, 22, 24, 26, 27], [2, 5, 8, 9, 12, 13, 14, 15, 17, 19, 20, 21, 24, 27, 28, 30], [2, 4, 8, 9, 12, 15, 16, 23, 24, 27, 28], [4, 5, 9, 10, 11, 12, 14, 15, 19, 22, 23, 27, 30]]
P5 = [60, 79, 49, 65, 88, 83, 38, 44, 54, 100, 65, 53, 43, 73, 63, 35, 65, 92, 74, 79, 67, 34, 95]
##print(BranchAndBoundSetCover(m5, n5, S5, P5))
##print(GreedySetCover(m5, n5, S5, P5))
##cProfile.run('BranchAndBoundSetCover(m5, n5, S5, P5)')
##cProfile.run('GreedySetCover(m5, n5, S5, P5)')

