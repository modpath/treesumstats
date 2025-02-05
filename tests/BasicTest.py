import unittest

from ete3 import Tree

from treesumstats import FeatureManager, FeatureRegistry
from treesumstats.basic_sumstats import BasicFeatureCalculator

NWK_W_ZERO = '((A:0.2, B:0.3, A1:0.4)AB:1, (C:0.8, (D:1.2, (E:1.4, F:0.1)EF:1.7)DF:0)CF:0.3)root:0.1;'

FeatureRegistry.register(BasicFeatureCalculator())


class BasicTest(unittest.TestCase):


    def test_basic_stats(self):
        tree = Tree(NWK_W_ZERO, format=3)

        features = ['n_trees', 'n_tips', 'n_inodes', 'len_forest']
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree, tree], *features),
                                                   [2, 7 * 2, 5 * 2,
                                                    (0.2 + 0.3 + 0.4 + 1 + 0.8 + 1.2 + 1.4 + 0.1 + 1.7 + 0.3 + 0.1) * 2]):
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')
