# -*- coding: utf-8 -*-
#  jisyo.py
#
# Copyright 2011 Hiroshi Miura <miurahr@linux.com>
from pkg_resources import resource_filename
try: #python2
    import cPickle as pickle
except: #python3
    import pickle

class jisyo (object):
    _len = None
    _dict = None

    def __init__(self, pklname):
        dict_pkl = open(resource_filename(__name__, pklname), 'rb')
        (self._dict, self._len) = pickle.load(dict_pkl)

    def haskey(self, key):
        return key in self._dict

    def lookup(self,key):
        return self._dict[key]
        
    def maxkeylen(self):
        return self._len
