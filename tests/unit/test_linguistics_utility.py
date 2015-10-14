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
        text = self.ling.clean_up_tweet( 'RE @heytitle YOYOYO http://t.com bb')
        self.assertEqual( text, '[RE] [MENTION] YOYOYO [URL] bb' )

        text = self.ling.clean_up_tweet( 'RE @heytitle @title ok!')
        self.assertEqual( text, '[RE] [MENTION] [MENTION] ok!' )
