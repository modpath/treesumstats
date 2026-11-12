import unittest

from ete3 import Tree

from treesumstats.balance_sumstats import WIDTH_DEPTH_RATIO, WIDTH_DELTA, IMBALANCE_AVG, BalanceFeatureCalculator, COLLESS, SACKIN, WIDTH_MAX, \
    DEPTH_MAX
from treesumstats import FeatureManager, FeatureRegistry, NORMALIZED

NWK_CONF = '(((A1:1, A2:1, A3:1)A:1, (B:1, (C:1, (D1:1, D2:1)D:1)CD:1)BD:1)AD:1,' \
           '((E1:1, E2:1, E3:1, E4:1)E:1, X:1)EX:1, ((F1:1, F2:1, F3:1)F:1, G:1)FG:1, (((H1:1, H2:1)H:1, I:1)HI:1, J:1)HJ:1, ' \
           '((K1:1, K2:1)K:1, (L1:1, L2:1)L:1)KL:1, ((M1:1, M2:1)M:1, N:1, O:1)MO:1);'

NWK = '((A:0.2, B:0.3, A1:0.4)AB:1, (C:0.8, (D:1.2, (E:1.4, F:0.1)EF:1.7)DF:1.5)CF:0.3)root:0.1;'

FeatureRegistry.register(BalanceFeatureCalculator())


class BalanceTest(unittest.TestCase):

    def test_balance_stats(self):
        tree = Tree(NWK, format=3)

        features = [COLLESS, SACKIN]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [4, 12]):
            self.assertEqual(real_value, value, msg=f'Wrong {feature_name} value')

        features = [f'{f}_{NORMALIZED}' for f in features]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [4 / (5 * 6 / 2), 12 / (6 * 7 / 2 - 1)]):
            self.assertEqual(real_value, value, msg=f'Wrong {feature_name} value')

    def test_width_stats(self):
        tree = Tree(NWK, format=3)

        features = [WIDTH_MAX, DEPTH_MAX, WIDTH_DEPTH_RATIO, WIDTH_DELTA]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [5, 4, 5 / 4, 3]):
            self.assertEqual(real_value, value, msg=f'Wrong {feature_name} value')

        features = [f'{f}_{NORMALIZED}' for f in features]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [5 / 6, 4 / 6, (5 / 4) / (6 / 3), 3 / 2]):
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

    def test_imbalance_stats(self):
        tree = Tree(NWK_CONF, format=3)
        features = ['n_inodes_imbalanced', 'frac_inodes_imbalanced', IMBALANCE_AVG]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [9, 9 / 18, (4/7 + 1/2 + 1 + 2/2 + 1 + 1 + 1/3 + 1/2 + 1 + 1/3 + 1 + 1/4 + 1 + 3/4 + 1 + 1/3 + 1/2 + 1) / 18]):
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')


