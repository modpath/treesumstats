import unittest
from collections import Counter

import numpy as np
from ete3 import Tree

from treesumstats import FeatureManager, FeatureRegistry, BASIC_ARRAY_METRICS
from treesumstats.subtree_sumstats import SubtreeFeatureCalculator, TIP_TOPOLOGY_LABELS, get_reshuffled_configs, \
    get_config2tips, CHERRY, TRIPLET_LADDER, TRIPLET_UNRESOLVED, QUARTET_LADDER, OTHER, CONFIG_ORDER, \
    QUARTET_UNRESOLVED, QUARTET_TRIPLET_UNRESOLVED_TIP, QUARTET_CHERRY_TIP_TIP, TIP_TIME_PERCENTILES, TOPOLOGY_LABEL2N, \
    KEY2TOPOLOGY_LABEL, pick_siblings
from treesumstats.tree_manager import annotate_forest_with_time, TIME

NWK = '((A1:1, A2:1, A3:1)A:1, (B:1, (C:1, (D1:1, D2:1)D:1)CD:1)BD:1);'
NWK_CONF = '(((A1:4.6, A2:3.3, A3:0.4)A:1.5, (B:2.3, (C:1.6, (D1:1.6, D2:0.1)D:4.9)CD:2.6)BD:0.8)AD:4.0,((E1:3.8, E2:0.5, E3:0.9, E4:1.8)E:2.4, X:1.7)EX:5.0, ((F1:4.7, F2:2.2, F3:4.2)F:2.9, G:4.6)FG:4.9, (((H1:1.8, H2:0.1)H:0.5, I:0.1)HI:0.3, J:3.3)HJ:0.3, ((K1:1.7, K2:3.1)K:3.5, (L1:3.1, L2:2.5)L:3.4)KL:0.5, ((M1:1.4, M2:0.2)M:1.2, N:0.4, O:4.8)MO:4.9);'

FeatureRegistry.register(SubtreeFeatureCalculator())


class TopologyTest(unittest.TestCase):


    def test_configuration_finder(self):
        tree = Tree(NWK, format=3)
        conf2tips = get_config2tips([tree])
        self.assertEqual(len(conf2tips), 5)
        self.assertListEqual(sorted([CHERRY, TRIPLET_LADDER, TRIPLET_UNRESOLVED, QUARTET_LADDER, OTHER],
                                    key=lambda _: -CONFIG_ORDER.index(_)),
                             sorted(conf2tips.keys(), key=lambda _: -CONFIG_ORDER.index(_)))
        self.assertEqual(len(conf2tips[CHERRY]), 1)
        self.assertEqual(sorted(_.name for _ in conf2tips[CHERRY][0]), ['D1', 'D2'])
        self.assertEqual(len(conf2tips[TRIPLET_UNRESOLVED]), 1)
        self.assertEqual(sorted(_.name for _ in conf2tips[TRIPLET_UNRESOLVED][0]), ['A1', 'A2', 'A3'])
        self.assertEqual(len(conf2tips[TRIPLET_LADDER]), 1)
        self.assertEqual(sorted(_.name for _ in conf2tips[TRIPLET_LADDER][0]), ['C', 'D1', 'D2'])
        self.assertEqual(len(conf2tips[QUARTET_LADDER]), 1)
        self.assertEqual(sorted(_.name for _ in conf2tips[QUARTET_LADDER][0]), ['B', 'C', 'D1', 'D2'])

        tree = Tree(NWK_CONF, format=3)
        conf2tips = get_config2tips([tree])
        self.assertEqual(len(conf2tips), len(CONFIG_ORDER) - 1)
        self.assertListEqual(CONFIG_ORDER[1:],
                             sorted(conf2tips.keys(), key=lambda _: CONFIG_ORDER.index(_)))

        self.assertEqual(len(conf2tips[CHERRY]), 5)
        conf = sorted('-'.join(sorted(_.name for _ in v)) for v in conf2tips[CHERRY])
        self.assertListEqual(conf, ['D1-D2', 'H1-H2', 'K1-K2', 'L1-L2', 'M1-M2'])

        self.assertEqual(len(conf2tips[TRIPLET_UNRESOLVED]), 2)
        conf = sorted('-'.join(sorted(_.name for _ in v)) for v in conf2tips[TRIPLET_UNRESOLVED])
        self.assertListEqual(conf, ['A1-A2-A3', 'F1-F2-F3'])

        self.assertEqual(len(conf2tips[TRIPLET_LADDER]), 2)
        conf = sorted('-'.join(sorted(_.name for _ in v)) for v in conf2tips[TRIPLET_LADDER])
        self.assertListEqual(conf, ['C-D1-D2', 'H1-H2-I'])

        self.assertEqual(len(conf2tips[QUARTET_UNRESOLVED]), 1)
        conf = sorted('-'.join(sorted(_.name for _ in v)) for v in conf2tips[QUARTET_UNRESOLVED])
        self.assertListEqual(conf, ['E1-E2-E3-E4'])

        self.assertEqual(len(conf2tips[QUARTET_TRIPLET_UNRESOLVED_TIP]), 1)
        conf = sorted('-'.join(sorted(_.name for _ in v)) for v in conf2tips[QUARTET_TRIPLET_UNRESOLVED_TIP])
        self.assertListEqual(conf, ['F1-F2-F3-G'])

        self.assertEqual(len(conf2tips[QUARTET_CHERRY_TIP_TIP]), 1)
        conf = sorted('-'.join(sorted(_.name for _ in v)) for v in conf2tips[QUARTET_CHERRY_TIP_TIP])
        self.assertListEqual(conf, ['M1-M2-N-O'])

        self.assertEqual(len(conf2tips[QUARTET_LADDER]), 2)
        conf = sorted('-'.join(sorted(_.name for _ in v)) for v in conf2tips[QUARTET_LADDER])
        self.assertListEqual(conf, ['B-C-D1-D2', 'H1-H2-I-J'])

        self.assertEqual(len(conf2tips[OTHER]), 1)
        conf = sorted('-'.join(sorted(_.name for _ in v)) for v in conf2tips[OTHER])
        self.assertListEqual(conf, ['X'])


    def test_sibling_finder(self):
        tree = Tree(NWK, format=3)
        inode_lists = pick_siblings([tree])
        self.assertEqual(len(inode_lists), 1)
        self.assertEqual(sorted(_.name for _ in inode_lists[0]), ['A', 'BD'])

        tree = Tree(NWK_CONF, format=3)
        inode_lists = pick_siblings([tree])
        self.assertEqual(len(inode_lists), 3)
        conf = sorted('-'.join(sorted(_.name for _ in v)) for v in inode_lists)
        expected_conf = ['A-BD', 'AD-EX-FG-HJ-KL-MO', 'K-L']
        self.assertListEqual(expected_conf, conf)


    def test_tips_in_configs(self):
        tree = Tree(NWK_CONF, format=3)



        features = [f'n_tips_in_{conf}' for conf in TIP_TOPOLOGY_LABELS]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [5 * 2, 2 * 3, 2 * 3, 1 * 4, 1 * 4, 1 * 4, 2 * 4, 1 * 4, 1 * 1]):
            self.assertEqual(real_value, value, msg=f'Wrong {feature_name} value')

        features = [f'frac_tips_in_{conf}' for conf in TIP_TOPOLOGY_LABELS]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [5 * 2 / 28,
                                                    2 * 3 / 28, 2 * 3 / 28,
                                                    1 * 4 / 28, 1 * 4 / 28, 1 * 4 / 28, 2 * 4 / 28, 1 * 4 / 28,
                                                    1 * 1 / 28]):
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')



    def test_inodes_with_wo_siblings(self):
        tree = Tree(NWK_CONF, format=3)

        features = [f'n_inodes_{wwo}_sibling_inodes' for wwo in ('with', 'without')]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [10, 7]):
            self.assertEqual(real_value, value, msg=f'Wrong {feature_name} value')

        features = [f'frac_inodes_{wwo}_sibling_inodes' for wwo in ('with', 'without')]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [10 / 17, 7 / 17]):
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')


    def test_reshuffled_tip_confs(self):
        forest = [Tree(NWK_CONF, format=3)]
        annotate_forest_with_time(forest)

        conf2tips = get_config2tips(forest)
        all_tips = sorted(list(forest[0].iter_leaves()), key=lambda t: getattr(t, TIME) - t.dist)


        real_confs = [sorted(c, key=lambda _: _.name) for c in sorted(conf2tips[CHERRY],
                                                                     key=lambda v: '-'.join(sorted(_.name for _ in v)))]
        # ['D1-D2', 'H1-H2', 'K1-K2', 'L1-L2', 'M1-M2']
        random_confs = get_reshuffled_configs(real_confs, all_tips)
        for random_conf, options in zip(random_confs,
                                        [['D1-F1', 'D1-F2', 'D1-F3', 'F1-D2', 'F2-D2', 'F3-D2'],
                                         ['H1-I', 'I-H2'],
                                         ['K1-L1', 'K1-L2', 'L1-K2', 'L2-K2'],
                                         ['K1-L2', 'K2-L2', 'L1-K2', 'L1-K1'],
                                         ['M1-A1', 'M1-A2', 'M1-A3', 'A1-M2', 'A2-M2', 'A2-M3'],
                                         ]):
            self.assertIn('-'.join(_.name for _ in random_conf), options, 'Random config was not found among possible options')

        real_A, real_F = [sorted(c, key=lambda _: _.name) for c in sorted(conf2tips[TRIPLET_UNRESOLVED],
                                                                      key=lambda v: '-'.join(
                                                                          sorted(_.name for _ in v)))]
        # ['A1-A2-A3', 'F1-F2-F3']
        random_A, random_F = get_reshuffled_configs([real_A, real_F], all_tips)

        counts = Counter([_.name for _ in random_A])
        random_A_name_str = "-".join(_.name for _ in random_A)
        real_A_name_str = "-".join(_.name for _ in real_A)
        self.assertEqual(1, counts['A1'] + counts['A2'] + counts['A3'], f'Random config {random_A_name_str} does not include a tip from the original config {real_A_name_str}')
        self.assertEqual(3, len({_.name for _ in random_A}), f'Some tips are not different in a random config {random_A_name_str}')
        self.assertEqual(0, len({_.name for _ in random_A} - {'A1', 'A2', 'A3'} - {'X', 'G', 'N', 'O', 'M1', 'M2'}), f'Some tips are not different in a random config {random_A_name_str}')

        counts = Counter([_.name for _ in random_F])
        random_F_name_str = "-".join(_.name for _ in random_F)
        real_F_name_str = "-".join(_.name for _ in real_F)
        self.assertEqual(1, counts['F1'] + counts['F2'] + counts['F3'], f'Random config {random_F_name_str} does not include a tip from the original config {real_F_name_str}')
        self.assertEqual(3, len({_.name for _ in random_F}), f'Some tips are not different in a random config {random_F_name_str}')
        self.assertEqual(0, len({_.name for _ in random_F} - {'F1', 'F2', 'F3'} - {'C', 'E1', 'E2', 'E3', 'E4'}), f'Some tips are not different in a random config {random_F_name_str}')

        for c_type in (TRIPLET_LADDER, QUARTET_UNRESOLVED, QUARTET_TRIPLET_UNRESOLVED_TIP, QUARTET_CHERRY_TIP_TIP, QUARTET_LADDER):
            for real_conf, random_conf in zip(conf2tips[c_type],
                                              get_reshuffled_configs(conf2tips[c_type], all_tips)):

                counts = Counter([_.name for _ in random_conf])
                random_conf_name_str = "-".join(_.name for _ in random_conf)
                real_conf_name_str = "-".join(_.name for _ in real_conf)
                self.assertEqual(1, sum(counts[_.name] for _ in real_conf),
                                 f'Random config {random_conf_name_str} does not include a tip from the original config {real_conf_name_str}')
                self.assertEqual(TOPOLOGY_LABEL2N[KEY2TOPOLOGY_LABEL[c_type]], len({_.name for _ in random_conf}),
                                 f'Some tips are not different in a random config {random_conf_name_str}')



    def test_reshuffled_inode_confs(self):
        forest = [Tree(NWK_CONF, format=3)]
        annotate_forest_with_time(forest)

        inode_lists = pick_siblings(forest)
        all_inodes = sorted([n for n in forest[0].traverse() if not n.is_leaf() and not n.is_root()], key=lambda t: getattr(t, TIME) - t.dist)


        for real_conf, random_conf in zip(inode_lists, get_reshuffled_configs(inode_lists, all_inodes)):

            counts = Counter([_.name for _ in random_conf])
            random_conf_name_str = "-".join(_.name for _ in random_conf)
            real_conf_name_str = "-".join(_.name for _ in real_conf)
            self.assertEqual(1, sum(counts[_.name] for _ in real_conf),
                             f'Random config {random_conf_name_str} does not include an inode from the original config {real_conf_name_str}')
            self.assertEqual(len(real_conf), len({_.name for _ in random_conf}),
                             f'Some inodes are not different in a random config {random_conf_name_str}')


    def test_cherry_stats(self):
        tree = Tree(NWK_CONF, format=3)


        real_time_diffs = [1.6 - 0.1, 1.8 - 0.1, 3.1 - 1.7, 3.1 - 2.5, 1.4 - 0.2]
        features = [f'time_diff_in_2_real_{flavour}' for flavour in BASIC_ARRAY_METRICS]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [np.mean(real_time_diffs), np.min(real_time_diffs), np.max(real_time_diffs), np.var(real_time_diffs), np.median(real_time_diffs)]):
            self.assertAlmostEqual(real_value, value, msg=f'Wrong {feature_name} value', places=6)

        features = [f'time_diff_in_2_real_perc{p}' for p in TIP_TIME_PERCENTILES]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   np.percentile(real_time_diffs, TIP_TIME_PERCENTILES)):
            self.assertAlmostEqual(real_value, value, msg=f'Wrong {feature_name} value', places=6)


    def test_quartet_ladder_stats(self):
        tree = Tree(NWK_CONF, format=3)

        times = [[2.6 + 4.9 + 1.6, 2.6 + 4.9 + 0.1, 2.6 + 1.6, 2.3],
                 [0.3 + 0.5 + 1.8, 0.3 + 0.5 + 0.1, 0.3 + 0.1, 3.3]]

        real_time_diffs = [np.mean(np.abs([t[0] - t[1], t[0] - t[2], t[0] - t[3], t[1] - t[2], t[1] - t[3], t[2] - t[3]])) for t in times]
        features = [f'time_diff_in_4L_real_{flavour}' for flavour in BASIC_ARRAY_METRICS]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [np.mean(real_time_diffs), np.min(real_time_diffs),
                                                    np.max(real_time_diffs), np.var(real_time_diffs),
                                                    np.median(real_time_diffs)]):
            self.assertAlmostEqual(real_value, value, msg=f'Wrong {feature_name} value', places=6)

        features = [f'time_diff_in_4L_real_perc{p}' for p in TIP_TIME_PERCENTILES]
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   np.percentile(real_time_diffs, TIP_TIME_PERCENTILES)):
            self.assertAlmostEqual(real_value, value, msg=f'Wrong {feature_name} value', places=6)

