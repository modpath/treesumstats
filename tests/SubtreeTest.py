import unittest

from ete3 import Tree

from treesumstats import FeatureManager, FeatureRegistry
from treesumstats.subtree_sumstats import SubtreeFeatureCalculator, TOPOLOGY_LABELS

NWK_CONF = '(((A1:1, A2:1, A3:1)A:1, (B:1, (C:1, (D1:1, D2:1)D:1)CD:1)BD:1)AD:1,' \
           '((E1:1, E2:1, E3:1, E4:1)E:1, X:1)EX:1, ((F1:1, F2:1, F3:1)F:1, G:1)FG:1, (((H1:1, H2:1)H:1, I:1)HI:1, J:1)HJ:1, ' \
           '((K1:1, K2:1)K:1, (L1:1, L2:1)L:1)KL:1, ((M1:1, M2:1)M:1, N:1, O:1)MO:1);'

NWK = '((A:0.2, B:0.3, A1:0.4)AB:1, (C:0.8, (D:1.2, (E:1.4, F:0.1)EF:1.7)DF:1.5)CF:0.3)root:0.1;'

FeatureRegistry.register(SubtreeFeatureCalculator())


class TopologyTest(unittest.TestCase):


    def test_configs(self):
        tree = Tree(NWK_CONF, format=3)



        features = [f'n_tips_in_{conf}' for conf in TOPOLOGY_LABELS]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [5 * 2, 2 * 3, 2 * 3, 1 * 4, 1 * 4, 1 * 4, 2 * 4, 1 * 4, 1 * 1]):
            self.assertEqual(real_value, value, msg=f'Wrong {feature_name} value')

        features = [f'frac_tips_in_{conf}' for conf in TOPOLOGY_LABELS]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [5 * 2 / 28,
                                                    2 * 3 / 28, 2 * 3 / 28,
                                                    1 * 4 / 28, 1 * 4 / 28, 1 * 4 / 28, 2 * 4 / 28, 1 * 4 / 28,
                                                    1 * 1 / 28]):
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')




