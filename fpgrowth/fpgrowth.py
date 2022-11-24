import csv
import collections
import itertools

class Node:
    def __init__(self, num, freq, f):
        self.num = num
        self.freq = freq
        self.f = f
        self.child = {}
        self.nxt = None
    def increment(self, freq):
        self.freq += freq
    def display(self, idx = 1):
        print(' ' * idx, self.num, ' ', self.freq)
        for child in list(self.child.values()):
            child.display(idx + 1)

def getFromFile(name):
    itemSetList = []
    freq = []
    with open(name, 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            line = list(filter(None, line))
            itemSetList.append(line)
            freq.append(1)
    return itemSetList, freq

def constructTree(itemSetList, freq, minSup):
    headertb = collections.defaultdict(int)
    for idx, itemSet in enumerate(itemSetList):
        for item in itemSet:
            headertb[item] += freq[idx]
    headertb = dict((item, cnt) for item, cnt in headertb.items() if cnt >= minSup)
    if (len(headertb) == 0):
        return None, None
    for item in headertb:
        headertb[item] = [headertb[item], None]
    fpTree = Node('Null', 1, None)
    for idx, itemSet in enumerate(itemSetList):
        itemSet = [item for item in itemSet if item in headertb]
        itemSet.sort(key = lambda item:headertb[item][0], reverse = True)
        curr = fpTree
        for item in itemSet:
            curr = updateTree(item, curr, headertb, freq[idx])
    return fpTree, headertb

def updateHeadertb(item, node, headertb):
    if headertb[item][1] == None:
        headertb[item][1] = node
    else:
        curr = headertb[item][1]
        while curr.nxt != None:
            curr = curr.nxt
        curr.nxt = node

def updateTree(item, node, headertb, freq):
    if item in node.child:
        node.child[item].increment(freq)
    else:
        newnode = Node(item, freq, node)
        node.child[item] = newnode
        updateHeadertb(item, newnode, headertb)
    return node.child[item]

'''
f,a,c,d,g,i,m,p
a,b,c,f,l,m,o
b,f,h,j,o
b,c,k,s,p
a,f,c,e,l,p,m,n
'''
