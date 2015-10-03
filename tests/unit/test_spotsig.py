from epoms.spotsig import SpotSig
from tests import *
from tests.helpers import *

class BaseTestCase(unittest.TestCase):
    spotsig  = SpotSig()

class TestSpotSig(BaseTestCase):

    def test_signature(self):
        doc = """
            At a rally to kick off a weeklong campaign for the South
            Carolina primary,  Obama tried to set the record straight
            from an attack circulating widely on the Internet that is
            designed to play into prejudices against Muslims and fears
            of terrorism
        """
        signature = self.spotsig.signature(doc).keys()
        signature.sort()

        self.assertEqual( signature,
            [
                'a:rally:kick',
                'a:weeklong:campaign',
                'an:attack:circulating',
                'is:designed:play',
                'the:internet:designed',
                'the:record:straight',
                'the:south:carolina'
            ]
        )

    def test_is_stopword(self):
        self.assertEqual( self.spotsig.is_stopword("that"), True )
        self.assertEqual( self.spotsig.is_stopword("foo"), False )

    # def test_tokenisation(self):
    #     self.assertEqual(
    #         self.spotsig.tokenise("This is the rock!\t Am Hungy"),
    #         [ 'this', 'is', 'the', 'rock', 'am', 'hungy' ]
    #     )

