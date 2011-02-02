#!/usr/bin/env python
from marshal import dumps # for kanwadict2
from zlib import compress
import re

try:
    import anydbm as dbm
    from cPickle import dump # for itaijidict2,kanadict2
except:
    import dbm
    from pickle import dump # for itaijidict2,kanadict2

class mkkanwa(object):

    records = {}

    def run(self, src, dst):
        for line in open(src, "r"):
            self.parsekdict(line)
        self.kanwaout(dst)

# for itaiji and kana/gairai dict

    def mkdict(self, src, dst):
        dic = {}
        for line in open(src, "r"):
            line = line.decode("utf-8").strip()
            if line.startswith(';;'): # skip comment
                continue
            if re.match(r"^$",line):
                continue
            (v, k) = (re.sub(r'\\u([0-9a-fA-F]{4})', lambda x:unichr(int(x.group(1),16)), line)).split(' ')
            dic[k] = v
        dump(dic, open(dst, 'w'), protocol=2) #pickle

# for kanwadict

    def parsekdict(self, line):
        line = line.decode("utf-8").strip()
        if line.startswith(';;'): # skip comment
            return
        (yomi, kanji) = line.split(' ')
        if ord(yomi[-1:]) <= ord('z'): 
            tail = yomi[-1:]
            yomi = yomi[:-1]
        else:
            tail = ''
        self.updaterec(kanji, yomi, tail)

    def updaterec(self, kanji, yomi, tail):
            key = "%04x"%ord(kanji[0]) 
            if key in self.records:
                if kanji in self.records[key]:
                    rec = self.records[key][kanji]
                    rec.append((yomi,tail))
                    self.records[key].update( {kanji: rec} )
                else:
                    self.records[key][kanji]=[(yomi, tail)]
            else:
                self.records[key] = {}
                self.records[key][kanji]=[(yomi, tail)]

    def kanwaout(self, out):
        dic = dbm.open(out, 'c')
        for (k, v) in self.records.iteritems():
            dic[k] = compress(dumps(v))
        dic.close()
