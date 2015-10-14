from epoms.linguistic_utility import LinguisticUtility
from tests import *
from tests.helpers import *

class BaseTestCase(unittest.TestCase):
    ling = LinguisticUtility()

class TestLinguisticUtility(BaseTestCase):

    def test_clean_up_space( self ):
        text = self.ling.clean_up_space( ' xxxx     b ')
        self.assertEqual( text, 'xxxx b' )
