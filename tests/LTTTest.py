import unittest

import numpy as np
from ete3 import Tree

from treesumstats import FeatureManager, FeatureRegistry, MEAN, MED, VAR, EPSILON, NORMALIZED
from treesumstats.branch_sumstats import BranchFeatureCalculator, BRLEN
from treesumstats.ltt_sumstats import LTTFeatureCalculator, get_ltt_plot, get_ltt_coordinates, TREE_PARTS
from treesumstats.tree_manager import annotate_forest_with_time

NWK = '((A:0.2, B:0.3, A1:0.4)AB:1, (C:0.8, (D:1.2, (E:1.4, F:0.1)EF:1.7)DF:1.5)CF:0.3)root:0.1;'
NWK_WO_ROOT_BR = '((A:0.2, B:0.3, A1:0.4)AB:1, (C:0.8, (D:1.2, (E:1.4, F:0.1)EF:1.7)DF:1.5)CF:0.3);'
FeatureRegistry.register(LTTFeatureCalculator(n_coordinates=5))


class BranchTest(unittest.TestCase):


    def test_lineage_stats(self):
        tree = Tree(NWK, format=3)

        features = ['time_trees_max'] + [f'time_trees_max_{part}' for part in TREE_PARTS]
        expected_values = 5 - np.array([0, 0, 5 / 3, 2 * 5 / 3])
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   expected_values):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

        features = ['trees_max'] + [f'trees_max_{part}' for part in TREE_PARTS]
        expected_values = [1, 1, 1, 1]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   expected_values):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

        features = ['time_lineages_max'] + [f'time_lineages_max_{part}' for part in TREE_PARTS]
        expected_values = 5 - np.array([1.1, 1.1, 1.9, 3.6])
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   expected_values):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

        features = ['lineages_max'] + [f'lineages_max_{part}' for part in TREE_PARTS]
        expected_values = [5, 5, 2, 2]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   expected_values):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

        features = [f'lineages_max_{NORMALIZED}'] + [f'lineages_max_{part}_{NORMALIZED}' for part in TREE_PARTS]
        expected_values = np.array([5, 5, 2, 2]) / len(tree)
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   expected_values):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

        features = ['lineage_start_to_max_slope', 'lineage_stop_to_max_slope', 'lineage_slope_ratio']
        expected_values = [(5 - 1) / (1.1 - 0), (5 - 0) / (5 - 1.1), ((5 - 1) / (1.1 - 0)) / ((5 - 0) / (5 - 1.1))]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   expected_values):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

        features = [f'lineage_start_to_max_slope_{part}' for part in TREE_PARTS]
        expected_values = [4 / (1.1 - 0), 1 / (1.9 - 5 / 3), 1 / (3.6 - 2 * 5 / 3)]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   expected_values):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

        features = [f'lineage_stop_to_max_slope_{part}' for part in TREE_PARTS]
        expected_values = [4 / (5 / 3 - 1.1), 1 / (2 * 5 / 3 - 1.9), 2 / (5 - 3.6)]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   expected_values):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

        features = [f'lineage_slope_ratio_{part}' for part in TREE_PARTS]
        expected_values = [(5 / 3 - 1.1) / (1.1 - 0), (2 * 5 / 3 - 1.9) / (1.9 - 5 / 3), 1 / 2 * (5 - 3.6) / (3.6 - 2 * 5 / 3)]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   expected_values):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

        features = [f'lineage_start_to_max_slope_{NORMALIZED}', f'lineage_stop_to_max_slope_{NORMALIZED}']
        expected_values = np.array([(5 - 1) / (1.1 - 0), (5 - 0) / (5 - 1.1)]) / len(tree)
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   expected_values):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

        features = [f'lineage_start_to_max_slope_{part}_{NORMALIZED}' for part in TREE_PARTS]
        expected_values = np.array([4 / (1.1 - 0), 1 / (1.9 - 5 / 3), 1 / (3.6 - 2 * 5 / 3)]) / len(tree)
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   expected_values):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

        features = [f'lineage_stop_to_max_slope_{part}_{NORMALIZED}' for part in TREE_PARTS]
        expected_values = np.array([4 / (5 / 3 - 1.1), 1 / (2 * 5 / 3 - 1.9), 2 / (5 - 3.6)]) / len(tree)
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   expected_values):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')


    def test_ltt_stats_tree(self):
        tree = Tree(NWK, format=3)

        features = [f'ltt_time{i}' for i in range(5)]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [5 - t for t in range(5)]):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

        features = [f'ltt_trees{i}' for i in range(5)]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [1] * 5):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')


        features = [f'ltt_lineages{i}' for i in range(5)]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [1, 3, 2, 2, 1]):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

        features = [f'ltt_lineages{i}_{NORMALIZED}' for i in range(5)]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   np.array([1, 3, 2, 2, 1]) / len(tree)):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')


    def test_ltt_stats_forest(self):
        tree = Tree(NWK, format=3)

        features = [f'ltt_time{i}' for i in range(5)]
        forest = [tree, tree]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features(forest, *features),
                                                   [5 - t for t in range(5)]):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

        features = [f'ltt_trees{i}' for i in range(5)]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features(forest, *features),
                                                   [2] * 5):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')


        features = [f'ltt_lineages{i}' for i in range(5)]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features(forest, *features),
                                                   np.array([1, 3, 2, 2, 1]) * 2):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

        features = [f'ltt_lineages{i}_{NORMALIZED}' for i in range(5)]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features(forest, *features),
                                                   np.array([1, 3, 2, 2, 1]) / len(tree)):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')



    def test_ltt_coordinates_forest(self):
        tree = Tree(NWK, format=3)
        annotate_forest_with_time([tree])
        ltt = get_ltt_plot([tree, tree])

        ltt = get_ltt_coordinates(ltt, n_coordinates=5)

        # ltt_times =    [0, 0.1, 0.4, 1.1, 1.2, 1.3, 1.4, 1.5, 1.9, 3.1, 3.6, 3.7, 5]
        # ltt_lineages = [1,   2,   3,   5,   4,   3,   2,   1,   2,   1,   2,   1, 0]

        expected_lineages = np.array([1, 3, 2, 2, 1]) * 2

        for i in range(5):
            self.assertEqual(i, ltt.times[i])
            self.assertEqual(expected_lineages[i], ltt.lineages[i])
            self.assertEqual(2, ltt.trees[i])

    def test_ltt_coordinates(self):
        tree = Tree(NWK, format=3)
        annotate_forest_with_time([tree])
        ltt = get_ltt_plot([tree])

        ltt = get_ltt_coordinates(ltt, n_coordinates=5)

        # ltt_times =    [0, 0.1, 0.4, 1.1, 1.2, 1.3, 1.4, 1.5, 1.9, 3.1, 3.6, 3.7, 5]
        # ltt_lineages = [1,   2,   3,   5,   4,   3,   2,   1,   2,   1,   2,   1, 0]

        expected_lineages = np.array([1, 3, 2, 2, 1])

        for i in range(5):
            self.assertEqual(i, ltt.times[i])
            self.assertEqual(expected_lineages[i], ltt.lineages[i])
            self.assertEqual(1, ltt.trees[i])


    def test_ltt_tree_w_root_br(self):
        tree = Tree(NWK, format=3)
        annotate_forest_with_time([tree])
        ltt = get_ltt_plot([tree])
        expected_times =             [0, 0.1, 0.4, 1.1, 1.2, 1.3, 1.4, 1.5, 1.9, 3.1, 3.6, 3.7, 5]
        expected_lineages = np.array([1,   2,   3,   5,   4,   3,   2,   1,   2,   1,   2,   1, 0])
        n = len(expected_times)
        expected_trees = np.ones(n, dtype=int)
        expected_trees[-1] = 0

        self.assertEqual(n, len(ltt.times))
        self.assertEqual(n, len(ltt.lineages))
        self.assertEqual(n, len(ltt.trees))
        for (t, et, l, el, tr, etr) in zip(ltt.times, expected_times,
                                           ltt.lineages, expected_lineages,
                                           ltt.trees, expected_trees):
            self.assertAlmostEqual(t, et, places=6)
            self.assertEqual(l, el)
            self.assertEqual(tr, etr)

    def test_ltt_tree_wo_root_br(self):
        tree = Tree(NWK_WO_ROOT_BR, format=3)
        annotate_forest_with_time([tree])
        ltt = get_ltt_plot([tree])

        expected_times =        [0.0,  0.3, 1.0, 1.1, 1.2, 1.3, 1.4, 1.8, 3.0, 3.5, 3.6, 4.9]
        expected_lineages  =    [  2,    3,   5,   4,   3,   2,   1,   2,   1,   2,   1,   0]
        n = len(expected_times)
        expected_trees = np.ones(n, dtype=int)
        expected_trees[-1] = 0

        self.assertEqual(n, len(ltt.times))
        self.assertEqual(n, len(ltt.lineages))
        self.assertEqual(n, len(ltt.trees))
        for (t, et, l, el, tr, etr) in zip(ltt.times, expected_times,
                                           ltt.lineages, expected_lineages,
                                           ltt.trees, expected_trees):
            self.assertAlmostEqual(t, et, places=6)
            self.assertEqual(l, el)
            self.assertEqual(tr, etr)

    def test_ltt_forest_same_start(self):
        forest = [Tree(NWK, format=3), Tree(NWK_WO_ROOT_BR, format=3)]
        annotate_forest_with_time(forest)
        ltt = get_ltt_plot(forest)
        expected_times_1 =             [0.0, 0.1,      0.4,      1.1, 1.2, 1.3, 1.4, 1.5,      1.9,      3.1,      3.6, 3.7,      5.0]
        expected_lineages_1_delta =    [ +1,  +1,       +1,       +2,  -1,  -1,  -1,  -1,       +1,       -1,       +1,  -1,       -1]
        expected_times_2 =             [0.0,      0.3,      1.0, 1.1, 1.2, 1.3, 1.4,      1.8,      3.0,      3.5, 3.6,      4.9]
        expected_lineages_2_delta =    [ +2,       +1,       +2,  -1,  -1,  -1,  -1,       +1,       -1,       +1,  -1,       -1]
        expected_times =               [0.0, 0.1, 0.3, 0.4, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.8, 1.9, 3.0, 3.1, 3.5, 3.6, 3.7, 4.9, 5.0]
        expected_lineages =            [  3,   4,   5,   6,   8,   9,   7,   5,   3,   2,   3,   4,   3,   2,   3,   3,   2,   1,   0]
        expected_trees =               [  2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   2,   1,   0]
        n = len(expected_times)


        print(ltt)
        self.assertEqual(n, len(ltt.times))
        self.assertEqual(n, len(ltt.lineages))
        self.assertEqual(n, len(ltt.trees))
        for (t, et, l, el, tr, etr) in zip(ltt.times, expected_times,
                                           ltt.lineages, expected_lineages,
                                           ltt.trees, expected_trees):
            self.assertAlmostEqual(t, et, places=6)
            self.assertEqual(l, el)
            self.assertEqual(tr, etr)

    def test_ltt_forest_diff_start(self):
        forest = [Tree(NWK, format=3), Tree(NWK_WO_ROOT_BR, format=3)]
        annotate_forest_with_time(forest, start_times=[0, 0.1])
        ltt = get_ltt_plot(forest)

        expected_times =             [0, 0.1, 0.4, 1.1, 1.2, 1.3, 1.4, 1.5, 1.9, 3.1, 3.6, 3.7, 5]
        expected_lineages = np.array([1,   2,   3,   5,   4,   3,   2,   1,   2,   1,   2,   1, 0]) * 2
        expected_lineages[0] = 1
        n = len(expected_times)
        expected_trees = np.ones(n, dtype=int) * 2
        expected_trees[0] = 1
        expected_trees[-1] = 0

        print(ltt)
        self.assertEqual(n, len(ltt.times))
        self.assertEqual(n, len(ltt.lineages))
        self.assertEqual(n, len(ltt.trees))
        for (t, et, l, el, tr, etr) in zip(ltt.times, expected_times,
                                           ltt.lineages, expected_lineages,
                                           ltt.trees, expected_trees):
            self.assertAlmostEqual(t, et, places=6)
            self.assertEqual(l, el)
            self.assertEqual(tr, etr)

