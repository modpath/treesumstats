import unittest

import numpy as np
from ete3 import Tree

from treesumstats.tree_manager import TIME
from treesumstats import FeatureManager, FeatureRegistry, BASIC_ARRAY_METRICS, NORMALIZED
from treesumstats.event_time_sumstats import EventTimeFeatureCalculator

NWK_W_ZERO = '((A:0.2, B:0.3, A1:0.4)AB:1, (C:0.8, (D:1.2, (E:1.4, F:0.1)EF:1.7)DF:0)CF:0.3)root:0.1;'

FeatureRegistry.register(EventTimeFeatureCalculator())


class EventTimeTest(unittest.TestCase):


    def test_tip_stats(self):
        tree = Tree(NWK_W_ZERO, format=3)

        features = [f'{TIME}_tip_{flavour}' for flavour in BASIC_ARRAY_METRICS]
        heights = [0.4 + 1 + 0.1, 0.3 + 1 + 0.1, 0.2 + 1 + 0.1,
                   0.8 + 0.3 + 0.1, 1.2 + 0.3 + 0.1,
                   0.1 + 1.7 + 0.3 + 0.1, 1.4 + 1.7 + 0.3 + 0.1]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [np.mean(heights), np.min(heights), np.max(heights), np.var(heights),
                                                    np.median(heights)]):
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

        features = [f'{TIME}_tip_{NORMALIZED}_{flavour}' for flavour in BASIC_ARRAY_METRICS]
        heights = np.array(heights) / np.max(heights)
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [np.mean(heights), np.min(heights), np.max(heights), np.var(heights),
                                                    np.median(heights)]):
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

    def test_inode_stats(self):
        tree = Tree(NWK_W_ZERO, format=3)

        features = [f'{TIME}_inode_{flavour}' for flavour in BASIC_ARRAY_METRICS]
        heights = [1 + 0.1, 1.7 + 0.3 + 0.1, 0 + 0.3 + 0.1, 0.3 + 0.1, 0.1]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [np.mean(heights), np.min(heights), np.max(heights), np.var(heights),
                                                    np.median(heights)]):
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

        features = [f'{TIME}_inode_{NORMALIZED}_{flavour}' for flavour in BASIC_ARRAY_METRICS]
        heights = np.array(heights) / (1.4 + 1.7 + 0.3 + 0.1)
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [np.mean(heights), np.min(heights), np.max(heights), np.var(heights),
                                                    np.median(heights)]):
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')
