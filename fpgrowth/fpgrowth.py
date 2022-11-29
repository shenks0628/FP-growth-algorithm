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
    itemSetList = {}
    with open(name, 'r') as file:
        reader = csv.reader(file)
        tmp = []
        for line in reader:
            line = list(filter(None, line))
            tmp.append(line)
        for item in tmp:
            itemSetList[frozenset(item)] = 1
    return itemSetList

def constructTree(itemSetList, minSup):
    headertb = {}
    for idx, itemSet in enumerate(itemSetList):
        for item in itemSet:
            headertb[item] = headertb.get(item, 0) + itemSetList[itemSet]
    for i in list(headertb.keys()):
        if headertb[i] < minSup:
            del(headertb[i])
    if (len(headertb) == 0):
        return None, None
    freqItemSet = set(headertb.keys())
    for item in headertb:
        headertb[item] = [headertb[item], None]
    fpTree = Node('Null', 1, None)
    for itemSet, cnt in itemSetList.items():
        itemx = {}
        for item in itemSet:
            if item in freqItemSet:
                itemx.update({item: headertb[item][0]})
        if len(itemx) > 0:
            items = [i[0] for i in sorted(itemx.items(), key = lambda p:(p[1], str(p[0])), reverse = True)]
            updateTree(items, fpTree, headertb, cnt)
    return fpTree, headertb

def updateHeadertb(item, node):
    while item.nxt != None:
        item = item.nxt
    item.nxt = node

def updateTree(items, node, headertb, freq):
    if items[0] in node.child:
        node.child[items[0]].increment(freq)
    else:
        node.child[items[0]] = Node(items[0], freq, node)
        if headertb[items[0]][1] == None:
            headertb[items[0]][1] = node.child[items[0]]
        else:
            updateHeadertb(headertb[items[0]][1], node.child[items[0]])
    if len(items) > 1:
        updateTree(items[1::], node.child[items[0]], headertb, freq)

def pull(node, prefix):
    if node.fa != None:
        prefix.append(node.num)
        pull(node.fa, prefix)

def findprefix(base, headertb):
    node = headertb[base][1]
    res = {}
    freq = []
    while node != None:
        prefix = []
        pull(node, prefix)
        if len(prefix) >= 1:
            res.update({frozenset(prefix[1:]): node.freq})
            freq.append(node.freq)
        node = node.nxt
    return res, freq

def mine(headertb, minSup, prefix, freqItemList, mp):
    sortedItemList = [item[0] for item in sorted(headertb.items(), key = lambda p : str(p[1]))] # sort by frequency
    for item in sortedItemList:
        newfreq = prefix.copy()
        newfreq.add(item)
        if len(newfreq) <= 5:
            newfreq = set(sorted(list(newfreq)))
            freqItemList.append(newfreq)
            [conditionalBase, freq] = findprefix(item, headertb)
            sum = 0
            for i in conditionalBase.values():
                sum += i
            mp.update({frozenset(newfreq): sum})
            [conditionalTree, newheadertb] = constructTree(conditionalBase, minSup)
            if newheadertb != None:
                mine(newheadertb, minSup, newfreq, freqItemList, mp)
                
# def powerset(s):
#     return itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(1, len(s)))

# def support(testSet, itemSetList):
#     cnt = 0
#     for itemSet in itemSetList:
#         if (set(testSet).issubset(itemSet)):
#             cnt += 1
#     return cnt

# def associationRule(freqItemSet, itemSetList, minConf):
#     rules = []
#     for itemSet in freqItemSet:
#         subsets = powerset(itemSet)
#         supp = support(itemSet, itemSetList)
#         for s in subsets:
#             conf = float(supp / support(s, itemSetList))
#             if conf >= minConf:
#                 rules.append([set(s), set(itemSet.difference(s)), conf])
#     return rules

def associationRule(freqItems, mp, minConf):
    rules = 0
    for items in mp:
        subsets = [i for n in range(1, len(items)) for i in itertools.combinations(items, n)]
        for subset in subsets:
            conf = mp[frozenset(items)] / mp[frozenset(subset)]
            if conf >= minConf:
                rules += 1
    return rules

def getFreqfromList(itemSetList):
    freq = [1 for i in range(len(itemSetList))]
    return freq

def fpgrowth(name, minSup, minConf):
    itemSetList = getFromFile(name)
    minSup = len(itemSetList) * minSup
    fpTree, headertb = constructTree(itemSetList, minSup)
    if fpTree == None:
        print("No frequent item set!")
    else:
        freqitems = []
        mp = {}
        mine(headertb, minSup, set(), freqitems, mp)
        rules = associationRule(freqitems, mp, minConf)
        return freqitems, rules

if __name__ == "__main__":
    # parser = optparse.OptionParser()
    # parser.add_option('-f', '--inputFile', dest = 'inputFile', help = 'CSV filename', default = None)
    # parser.add_option('-s', '--minSupport', dest = 'minSup', help = 'Min support (float)', default = 0.5, type = 'float')
    # parser.add_option('-c', '--minConfidence', dest = 'minConf', help = 'Min confidence (float)', default = 0.5, type = 'float')
    # [test, args] = parser.parse_args()
    # freqitems, rules = fpgrowth(test.inputFile, test.minSup, test.minConf)
    # freqitems, rules = fpgrowth("test.csv", 0.5, 0.5)
    freqitems, rules = fpgrowth("mushroom.csv", 0.1, 0.8)
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
    for i in range(0, 5):
        print("|L^" + str(i + 1) + "|=" + str(cnt[i]))
    print(rules)

# '''
# f,a,c,d,g,i,m,p
# a,b,c,f,l,m,o
# b,f,h,j,o
# b,c,k,s,p
# a,f,c,e,l,p,m,n
# '''
