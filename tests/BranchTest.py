import unittest

import numpy as np
from ete3 import Tree

from treesumstats import FeatureManager, FeatureRegistry, MEAN, MED, VAR, EPSILON
from treesumstats.branch_sumstats import BranchFeatureCalculator, BRLEN

NWK_W_ZERO = '((A:0.2, B:0.3, A1:0.4)AB:1, (C:0.5, (D:1.2, (E:1.4, F:0.1)EF:1.7)DF:0)CF:0.3)root:0.1;'

FeatureRegistry.register(BranchFeatureCalculator())


class BranchTest(unittest.TestCase):


    def test_inode_stats(self):
        tree = Tree(NWK_W_ZERO, format=3)

        features = [f'{BRLEN}_inode_{flavour}' for flavour in [MEAN, MED, VAR]]
        brlens = [1, 1.7, 0, 0.3, 0.1]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [np.mean(brlens), np.median(brlens), np.var(brlens)]):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

    def test_inode_stats_top(self):
        tree = Tree(NWK_W_ZERO, format=3)

        features = [f'{BRLEN}_inode_top_{flavour}' for flavour in [MEAN, MED, VAR]]
        brlens = [1, 0, 0.3, 0.1]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [np.mean(brlens), np.median(brlens), np.var(brlens)]):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

    def test_inode_stats_middle(self):
        tree = Tree(NWK_W_ZERO, format=3)

        features = [f'{BRLEN}_inode_middle_{flavour}' for flavour in [MEAN, MED, VAR]]
        brlens = [0.4 + 1.7 - 3.5 / 3]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [np.mean(brlens), np.median(brlens), np.var(brlens)]):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

    def test_inode_stats_bottom(self):
        tree = Tree(NWK_W_ZERO, format=3)

        features = [f'{BRLEN}_inode_bottom_{flavour}' for flavour in [MEAN, MED, VAR]]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [0, 0, 0]):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

    def test_tip_stats(self):
        tree = Tree(NWK_W_ZERO, format=3)

        features = [f'{BRLEN}_tip_{flavour}' for flavour in [MEAN, MED, VAR]]
        brlens = [0.2, 0.3, 0.4, 0.5, 1.2, 0.1, 1.4]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [np.mean(brlens), np.median(brlens), np.var(brlens)]):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

    def test_tip_stats_top(self):
        tree = Tree(NWK_W_ZERO, format=3)

        features = [f'{BRLEN}_tip_top_{flavour}' for flavour in [MEAN, MED, VAR]]
        brlens = [0.5]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [np.mean(brlens), np.median(brlens), np.var(brlens)]):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

    def test_tip_stats_middle(self):
        tree = Tree(NWK_W_ZERO, format=3)

        features = [f'{BRLEN}_tip_middle_{flavour}' for flavour in [MEAN, MED, VAR]]
        brlens = list(np.array([0.1 + 1 + 0.4, 0.1 + 1 + 0.3, 0.1 + 1 + 0.2, 0.1 + 0.3 + 1.2]) - 3.5 / 3) + [0.1]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [np.mean(brlens), np.median(brlens), np.var(brlens)]):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

    def test_tip_stats_bottom(self):
        tree = Tree(NWK_W_ZERO, format=3)

        features = [f'{BRLEN}_tip_bottom_{flavour}' for flavour in [MEAN, MED, VAR]]
        brlens = [0.1 + 0.3 + 1.7 + 1.4 - 2 * 3.5 / 3]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [np.mean(brlens), np.median(brlens), np.var(brlens)]):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')


    def test_ratio_stats(self):
        tree = Tree(NWK_W_ZERO, format=3)

        features = [f'frac_{BRLEN}_inode_{flavour}_by_{BRLEN}_tip_{flavour}' for flavour in [MEAN, MED, VAR]]
        ibrlens = [1, 1.7, 0, 0.3, 0.1]
        ebrlens = [0.2, 0.3, 0.4, 0.5, 1.2, 0.1, 1.4]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [np.mean(ibrlens) / np.mean(ebrlens), np.median(ibrlens) / np.median(ebrlens),
                                                    np.var(ibrlens) / np.var(ebrlens)]):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

    def test_ratio_stats_top(self):
        tree = Tree(NWK_W_ZERO, format=3)

        features = [f'frac_{BRLEN}_inode_top_{flavour}_by_{BRLEN}_tip_top_{flavour}' for flavour in [MEAN, MED, VAR]]
        ibrlens = [1, 0, 0.3, 0.1]
        ebrlens = [0.5]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [np.mean(ibrlens) / np.mean(ebrlens), np.median(ibrlens) / np.median(ebrlens),
                                                    np.var(ibrlens) / max(np.var(ebrlens), EPSILON)]):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

    def test_ratio_stats_middle(self):
        tree = Tree(NWK_W_ZERO, format=3)

        ibrlens = [0.4 + 1.7 - 3.5 / 3]
        ebrlens = list(np.array([0.1 + 1 + 0.4, 0.1 + 1 + 0.3, 0.1 + 1 + 0.2, 0.1 + 0.3 + 1.2]) - 3.5 / 3) + [0.1]
        features = [f'frac_{BRLEN}_inode_middle_{flavour}_by_{BRLEN}_tip_middle_{flavour}' for flavour in [MEAN, MED, VAR]]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [np.mean(ibrlens) / np.mean(ebrlens),
                                                    np.median(ibrlens) / np.median(ebrlens),
                                                    np.var(ibrlens) / max(np.var(ebrlens), EPSILON)]):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

    def test_ratio_stats_bottom(self):
        tree = Tree(NWK_W_ZERO, format=3)

        ebrlens = [0.1 + 0.3 + 1.7 + 1.4 - 2 * 3.5 / 3]

        features = [f'frac_{BRLEN}_inode_bottom_{flavour}_by_{BRLEN}_tip_bottom_{flavour}' for flavour in [MEAN, MED, VAR]]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [0 / np.mean(ebrlens),
                                                    0 / np.median(ebrlens),
                                                    0 / max(np.var(ebrlens), EPSILON)]):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')
