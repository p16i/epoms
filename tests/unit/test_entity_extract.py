from epoms.entity_extract import EntityExtract
from tests import *
from tests.helpers import *

class BaseTestCase(unittest.TestCase):
    en = EntityExtract()

class TestEntityExtract(BaseTestCase):

    def test_merge_name( self ):
        names = {
            'Obama': 2,
            'John mayer': 3,
            'John Mayer': 2
        }

        new_list = self.en.merge_name( names )

        self.assertEqual( new_list, { 'John Mayer': 5, 'Obama': 2 } )
