import csv
import collections
import itertools
import optparse

class Node:
    def __init__(self, num, freq, fa):
        self.num = num
        self.freq = freq
        self.fa = fa
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

def pull(node, prefix):
    if node.fa != None:
        prefix.append(node.num)
        pull(node.fa, prefix)

def findprefix(base, headertb):
    node = headertb[base][1]
    res = []
    freq = []
    while node != None:
        prefix = []
        pull(node, prefix)
        if len(prefix) > 1:
            res.append(prefix[1:])
            freq.append(node.freq)
        node = node.nxt
    return res, freq

def mine(headertb, minSup, prefix, freqItemList):
    sortedItemList = [item[0] for item in sorted(list(headertb.items()), key = lambda p : p[1][0])] # sort by frequency
    for item in sortedItemList:
        newfreq = prefix.copy()
        newfreq.add(item)
        freqItemList.append(newfreq)
        [conditionalBase, freq] = findprefix(item, headertb)
        [conditionalTree, newheadertb] = constructTree(conditionalBase, freq, minSup)
        if newheadertb != None:
            mine(newheadertb, minSup, newfreq, freqItemList)

def powerset(s):
    return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(1, len(s)))

def support(testSet, itemSetList):
    cnt = 0
    for itemSet in itemSetList:
        if (set(testSet).issubset(itemSet)):
            cnt += 1
    return cnt

def associationRule(freqItemSet, itemSetList, minConf):
    rules = []
    for itemSet in freqItemSet:
        subsets = powerset(itemSet)
        supp = support(itemSet, itemSetList)
        for s in subsets:
            conf = float(supp / support(s, itemSetList))
            if conf >= minConf:
                rules.append([set(s), set(itemSet.difference(s)), conf])
    return rules

def getFreqfromList(itemSetList):
    freq = [1 for i in range(len(itemSetList))]
    return freq

def fpgrowth(name, minSup, minConf):
    itemSetList, freq = getFromFile(name)
    minSup = len(itemSetList) * minSup
    fpTree, headertb = constructTree(itemSetList, freq, minSup)
    if fpTree == None:
        print("No frequent item set!")
    else:
        freqitems = []
        mine(headertb, minSup, set(), freqitems)
        rules = associationRule(freqitems, itemSetList, minConf)
        return freqitems, rules

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-f', '--inputFile', dest = 'inputFile', help = 'CSV filename', default = None)
    parser.add_option('-s', '--minSupport', dest = 'minSup', help = 'Min support (float)', default = 0.5, type = 'float')
    parser.add_option('-c', '--minConfidence', dest = 'minConf', help = 'Min confidence (float)', default = 0.5, type = 'float')
    [test, args] = parser.parse_args()
    freqitems, rules = fpgrowth(test.inputFile, test.minSup, test.minConf)
    # print(freqitems)
    cnt = [0, 0, 0, 0, 0]
    for i in freqitems:
        if len(i) == 1:
            cnt[0] += 1
        elif len(i) == 2:
            cnt[1] += 1
        elif len(i) == 3:
            cnt[2] += 1
        elif len(i) == 4:
            cnt[3] += 1
        elif len(i) == 5:
            cnt[4] += 1
    for i in cnt:
        print(i)
    print(len(rules))
    # for i in rules:
    #     print(i)

# [a, b] = getFromFile("test.csv")
# [c, d] = constructTree(a, b, 0.5)
# c.display()
# for i in d:
#     print(i)
#     for j in d[i]:
#         print(j)

'''
f,a,c,d,g,i,m,p
a,b,c,f,l,m,o
b,f,h,j,o
b,c,k,s,p
a,f,c,e,l,p,m,n
'''
