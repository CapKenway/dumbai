import sys
from pprint import pprint
import os
#--------------------------------------------------------------------------#
class CsPP():
    def __init__(self, domains):
        self.domains = domains
        self.maindict = {}
        self.keyitems = []
        pass

    def check_if(self):
        emptylist = []
        for domainkey in list(self.domains.keys()):
            if not domainkey in list(self.maindict.keys()):
                emptylist.append(domainkey)
        for listitem in emptylist:
            self.maindict[listitem] = list(self.domains.values())[1]
        pass

    def not_belonging(self, key, lister):
        templist = []
        maindomain = self.domains[key]
        for item in maindomain:
            if not item in lister:
                templist.append(item)
        self.maindict[key] = templist
        pass
    
    def belonging(self, key, lister):
        self.maindict.__setitem__(key, lister)
        pass
    
    def get_one_up(self, values):
        self.keyitems.insert(self.keyitems.index(values[0]), values[1])

    def get_one_down(self, values):
        self.keyitems.reverse()
        self.keyitems.insert(self.keyitems.index(values[1]), values[0])
        self.keyitems.reverse()

    def not_working_together(self, first, second):
        firstlist = self.maindict[first]
        secondlist = self.maindict[second]
        for item in firstlist:
            if item in secondlist:
                firstlist.remove(item)
        self.maindict[first] = firstlist
    
    def backtrack(self, maindict, what_want = '', conditions = [], starter = ''):
        csp_back = CsPP_Backend(domains = maindict, what_want = what_want, conditions = conditions, starter = starter)
        return csp_back._backtrack()
        pass
    
    def left_to_right(self, maindict, path):
        to_do = []
        pathkeys = list(path.keys())
        pathvalues = list(path.values())
        mainkeys = list(maindict.keys())
        mainvalues = list(maindict.values())
        keylist = []
        for key, values in zip(pathkeys, pathvalues):
            keylist.append(key)
            if len(values) > 1:
                to_do.append(values[1:])
            if len(to_do) != 0:
                for i in range(0, len(to_do)):
                    popped = to_do.pop(i)
                keylist.append(popped)
        for item in keylist:
            if keylist.count(item) > 1:
                keylist.remove(item)
            if type(item) == list:
                keylist.remove(item)
        valuestodict = []
        for key in keylist:
            if type(key) != list:
                valuestodict.append(maindict[key])
            else:
                keylist.remove(key)
        returndict = dict((key, values) for key, values in zip(keylist, valuestodict))
        forprune = CsPP_Backend()
        pruned = forprune._prune(returndict)
        return pruned
    
    def right_to_left(self, maindict, path):
        tempkeys = list(path.keys())
        tempvalues = list(path.values())
        tempvalues.reverse()
        tempkeys.reverse()
        i = 0
        flag = False
        templist = []
        removeditems = []
        indexes = []
        i = 0
        templist.append(tempkeys[0])
        for key in tempkeys:
            for n in range(i, len(tempvalues)):
                flag = False
                for u in range(0, len(tempvalues[n])):
                    if len(tempvalues)!= 0 and key == tempvalues[n][u]:
                        i = n
                        templist.append(tempkeys[n])
                        flag = True
                        break
                if flag:
                    break
        for item in templist:
            if templist.count(item) > 1:
                templist.remove(item)
        dictvalues = []
        for tempval in templist:
            dictvalues.append(maindict[tempval])
        availdict = dict((key, val) for key, val in zip(templist, dictvalues))

        removedvalues = []
        for key in list(maindict.keys()):
            if not key in list(availdict.keys()):
                removeditems.append(key)
                removedvalues.append(maindict[key])
        removeddict = dict((key, val) for key, val in zip(removeditems, removedvalues))
        forprune = CsPP_Backend()
        pruned = forprune._prune(availdict)
        for key in list(removeddict.keys()):
            pruned[key] = []
        return pruned
        pass
    
#--------------------------------------------------------------------------#

class CsPP_Backend():
    def __init__(self, *args, **kwargs):
        self.domains = kwargs.get('domains')
        self.conditions = kwargs.get('conditions')
        self.what_want = kwargs.get('what_want')
        self.starter = kwargs.get('starter')
        pass
    
    def _backtrack(self):
        if self.what_want == 'mrv':
            return self._highest_constraint(self.domains, self.starter)
        elif self.what_want == 'lcv':
            return self._minimum_constraint(self.domains, self.starter)
        else:
            return self.domains

    def _minimum_constraint(self, domains, starter = ''):
        low_constraint = None
        if starter != '':
            yet_lowest = len(domains[starter])
        else:
            yet_lowest = len(domains[list(domains.keys())[0]])
        for key, val in zip(list(domains.keys()), list(domains.values())):
            if yet_lowest > len(val):
                yet_lowest = len(val)
                low_constraint = key
        return low_constraint
        pass

    def _highest_constraint(self, domains, starter = ''):
        high_constraint = None
        if starter != '':
            yet_highest = len(domains[starter])
        else:
            yet_highest = len(domains[list(domains.keys())[0]])
        for key, val in zip(list(domains.keys()), list(domains.values())):
            if yet_highest < len(val):
                yet_highest = len(val)
                high_constraint = key
        return high_constraint
        pass

    def _prune(self, domains):
        emptydict = {}
        pruneditems = []
        for key, value in zip(list(domains.keys()), list(domains.values())):
            for val in value:
                if val in pruneditems:
                    continue
                emptydict.__setitem__(key, val)
                pruneditems.append(val)
                break
        for key in list(domains.keys()):
            if not key in list(emptydict.keys()):
                emptydict.__setitem__(key, [])
        return emptydict
#--------------------------------------------------------------------------#