from epoms.linguistic_utility import LinguisticUtility
from tests import *
from tests.helpers import *

class BaseTestCase(unittest.TestCase):
    ling = LinguisticUtility()

class TestLinguisticUtility(BaseTestCase):

    def remove_diacritics( self ):
        # -*- coding: utf-8 -*-
        text = self.ling.remove_diacritics(u'RØDE')
        self.assertEqual( text, 'RODE' );
