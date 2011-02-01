#!/usr/bin/python
# derivered from unidecode setup.py

from setuptools import Command,setup

import unittest
import os,threading
import gencodemap
import genkanwadict

UNITTESTS = [
        "tests", 
    ]

class TestCommand(Command):
    user_options = [ ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        suite = unittest.TestSuite()

        suite.addTests( 
            unittest.defaultTestLoader.loadTestsFromNames( 
                                UNITTESTS ) )

        result = unittest.TextTestRunner(verbosity=2).run(suite)

class GenKanwa(Command):
    user_options = [ ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        src = os.path.join('data','kakasidict.utf8')        
        dst = os.path.join('unihandecode','pykakasi','kanwadict2.db')
        try:
            os.unlink(dst)
        except:
            pass
        kanwa = genkanwadict.mkkanwa()
        kanwa.run(src, dst)

        src = os.path.join('data','itaijidict.utf8')
        dst = os.path.join('unihandecode','pykakasi','itaijidict2.pickle')
        try:
            os.unlink(dst)
        except:
            pass
        kanwa.mkitaiji(src, dst)

        src = os.path.join('data','kanadict.utf8')
        dst = os.path.join('unihandecode','pykakasi','kanadict2.pickle')
        try:
            os.unlink(dst)
        except:
            pass
        kanwa.mkkanadict(src, dst)



class GenMap(Command):
    user_options = [ ]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        k= genmap_t('kr')
        j= genmap_t('ja')
        c= genmap_t('zh')
        v= genmap_t('vn')
        k.start()
        j.start()
        c.start()
        v.start()
        k.join()
        j.join()
        c.join()
        v.join()

class genmap_t(threading.Thread):
    l = None
    def __init__(self, lang):
        threading.Thread.__init__(self)
        self.l = lang

    def run(self):
        unihan_source = os.path.join('data','Unihan_Readings.txt')        
        dest = os.path.join('unihandecode',self.l+'codepoints.py')
        u = gencodemap.UnihanConv(self.l)
        u.run(source = unihan_source, dest=dest)


setup(name='Unihandecode',
      version='0.20',
      description='US-ASCII transliterations of Unicode text',
      url='http://launchpad.net/unihandecode/',
      license='GPLv3/Perl',
      long_description="""
It often happens that you have non-Roman text data in Unicode, but
you can't display it -- usually because you're trying to show it
to a user via an application that doesn't support Unicode, or
because the fonts you need aren't accessible. You could represent
the Unicode characters as "???????" or "\15BA\15A0\1610...", but
that's nearly useless to the user who actually wants to read what
the text says.

What Unihandecode provides is a function, 'decode(...)' that
takes Unihancode data and tries to represent it in ASCII characters 
(i.e., the universally displayable characters between 0x00 and 0x7F). 
The representation is almost always an attempt at transliteration 
-- i.e., conveying, in Roman letters, the pronunciation expressed by 
the text in some other writing system.

For example;
>>>d = Unidecoder()
>>>d.decode(u"\u5317\u4EB0")
'Bei Jing'.
d = Unidecoder(lang='ja')
>>>d.decode(u"\u5317\u4EB0")
'Pe King'
      """,
      author='Hioshi Miura',
      author_email='miurahr@linux.com',

      packages = [ 'unihandecode', 'unihandecode.pykakasi' ],

      package_data = { 'unihandecode.pykakasi': ['kanwadict2.db','itaijidict2.pickle', 'gairaidict2.pickle', 'kanadict2.pickle']},

      provides = [ 'unihandecode' ],

      cmdclass = { 'test': TestCommand,  'genmap':GenMap, 'genkanwa':GenKanwa }

)
