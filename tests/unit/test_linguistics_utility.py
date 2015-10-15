from epoms.linguistic_utility import LinguisticUtility
from tests import *
from tests.helpers import *

class BaseTestCase(unittest.TestCase):
    ling = LinguisticUtility()

class TestLinguisticUtility(BaseTestCase):

    def test_clean_up_space( self ):
        text = self.ling.clean_up_space( ' xxxx     b ')
        self.assertEqual( text, 'xxxx b' )

    def test_clean_up_tweet( self ):
        text = self.ling.clean_up_tweet( 'RT @heytitle YOYOYO http://t.com bb')
        self.assertEqual( text, '[RT] [MENTION] YOYOYO [URL] bb' )

        text = self.ling.clean_up_tweet( 'RT @heytitle @title ok!')
        self.assertEqual( text, '[RT] [MENTION] [MENTION] ok!' )

    def test_choose_fartest_term( self ):
        term =self.ling.choose_furthest_term( 'john mayer', 'John mayer', 'John Mayer' )
        self.assertEqual( term, 'John Mayer' )
