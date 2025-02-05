import unittest

from ete3 import Tree

from treesumstats import FeatureManager, FeatureRegistry
from treesumstats.resolution_sumstats import FRACTION_RESOLVED, FRACTION_RESOLVED_NON_ZERO, N_RESOLVED, \
    N_RESOLVED_NON_ZERO, ResolutionFeatureCalculator, N_CHILDREN_PREFIX

NWK_W_ZERO = '((A:0.2, B:0.3, A1:0.4)AB:1, (C:0.8, (D:1.2, (E:1.4, F:0.1)EF:1.7)DF:0)CF:0.3)root:0.1;'

FeatureRegistry.register(ResolutionFeatureCalculator())


class ResolutionTest(unittest.TestCase):


    def test_resolution_stats(self):
        tree = Tree(NWK_W_ZERO, format=3)

        features = [N_RESOLVED, N_RESOLVED_NON_ZERO, FRACTION_RESOLVED, FRACTION_RESOLVED_NON_ZERO]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [4, 2, 4 / 6, 2 / 6]):
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')



    def test_nchild_stats(self):
        tree = Tree(NWK_W_ZERO, format=3)

        features = [f'{N_CHILDREN_PREFIX}_min', f'{N_CHILDREN_PREFIX}_max',f'{N_CHILDREN_PREFIX}_mean', f'{N_CHILDREN_PREFIX}_median', f'{N_CHILDREN_PREFIX}_var']
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [2, 3, 11 / 5, 2, 0.16]):
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

