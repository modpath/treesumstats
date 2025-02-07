from collections import Counter, defaultdict

import numpy as np
from scipy.special import digamma

from treesumstats import FeatureCalculator, NORMALIZED

TOPOLOGY_LABELS = ['2', '3U', '3L', '4U', '4U3U1', '4U211', '4L', '4B', 'O']

TIP = 1

CHERRY = (TIP, TIP)

TRIPLET_UNRESOLVED = (TIP, TIP, TIP)
TRIPLET_LADDER = (CHERRY, TIP)

QUARTET_UNRESOLVED = (TIP, TIP, TIP, TIP)
QUARTET_TRIPLET_UNRESOLVED_TIP = (TRIPLET_UNRESOLVED, TIP)
QUARTET_CHERRY_TIP_TIP = (CHERRY, TIP, TIP)
QUARTET_LADDER = (TRIPLET_LADDER, TIP)
QUARTET_BALANCED = (CHERRY, CHERRY)

OTHER = 2

CONFIG_ORDER = [TIP, CHERRY, TRIPLET_UNRESOLVED, TRIPLET_LADDER,
                QUARTET_UNRESOLVED, QUARTET_TRIPLET_UNRESOLVED_TIP, QUARTET_CHERRY_TIP_TIP, QUARTET_LADDER, QUARTET_BALANCED,
                OTHER]

TOPOLOGY_LABEL2NAME = {'2': 'cherries', '3U': 'unresolved triplets', '3L': 'resolved triplets',
                       '4U': 'fully unresolved quartets',
                       '4U3U1': 'partially resolved quartets with an unresolved triplet and a tip as children',
                       '4U211': 'partially resolved quartets with a cherry and two tips as three children',
                       '4L': 'ladderized fully resolved quartets',
                       '4B': 'balanced quartets (with two cherries as children)'}

class SubtreeFeatureCalculator(FeatureCalculator):
    """Computes tree topology-related summary statistics."""

    def __init__(self):
        self._n_inodes = None
        self._forest = None
        self._topo2tips = None
        self._n_tips = None

    def help(self, feature_name, *args, **kwargs):
        if 'tips_in_' in feature_name:
            conf = feature_name[feature_name.find('tips_in_') + len('tips_in_'):]
            measure = 'fraction' if feature_name.startswith('frac') else 'number'
            if 'O' == conf:
                return f'{measure} of forest tips that are not part of any subtree of size 2, 3 or 4.'
            return f'{measure} of forest tips that are found in {TOPOLOGY_LABEL2NAME[conf]}.'
        return None

    def feature_names(self):
        return [f'frac_tips_in_{conf}' for conf in TOPOLOGY_LABELS] \
            + [f'n_tips_in_{conf}' for conf in TOPOLOGY_LABELS]

    def set_forest(self, forest, **kwargs):
        self._forest = forest
        self._topo2tips = None
        self._n_tips = None
        self._n_inodes = None

    @property
    def n_tips(self):
        if self._n_tips is None:
            self._n_tips = sum(len(tree) for tree in self._forest)
        return self._n_tips

    @property
    def n_inodes(self):
        """Number of internal nodes in the forest"""
        if self._n_inodes is None:
            self._n_inodes = sum(sum(1 for _ in tree.traverse() if not _.is_leaf()) for tree in self._forest)
        return self._n_inodes

    @property
    def conf2tips(self):
        if self._topo2tips is None:
            self._topo2tips = defaultdict(list)
            feature = 'configuration'
            for tree in self._forest:
                for n in tree.traverse('postorder'):
                    if n.is_leaf():
                        if not n.is_root():
                            n.add_feature(feature, TIP)
                        continue

                    if len(n) > 4:
                        self._topo2tips[OTHER].extend(_ for _ in n.children if _.is_leaf())
                    else:
                        config = tuple(
                            sorted([getattr(c, feature) for c in n.children], key=lambda _: -CONFIG_ORDER.index(_)))
                        n.add_feature(feature, config)
                        self._topo2tips[config].append(list(n.iter_leaves()))

                    for c in n.children:
                        c.del_feature(feature)
        return self._topo2tips

    def calculate(self, feature_name, **kwargs):
        if 'tips_in_' in feature_name:
            conf = feature_name[feature_name.find('tips_in_') + len('tips_in_'):]
            denominator = self.n_tips if feature_name.startswith('frac') else 1
            if 'O' == conf:
                return len(self.conf2tips[OTHER]) / denominator
            if '2' == conf:
                return len(self.conf2tips[CHERRY]) * 2 / denominator
            if '3U' == conf:
                return len(self.conf2tips[TRIPLET_UNRESOLVED]) * 3 / denominator
            if '3L' == conf:
                return len(self.conf2tips[TRIPLET_LADDER]) * 3 / denominator
            if '4U' == conf:
                return len(self.conf2tips[QUARTET_UNRESOLVED]) * 4 / denominator
            if '4U3U1' == conf:
                return len(self.conf2tips[QUARTET_TRIPLET_UNRESOLVED_TIP]) * 4 / denominator
            if '4U211' == conf:
                return len(self.conf2tips[QUARTET_CHERRY_TIP_TIP]) * 4 / denominator
            if '4L' == conf:
                return len(self.conf2tips[QUARTET_LADDER]) * 4 / denominator
            if '4B' == conf:
                return len(self.conf2tips[QUARTET_BALANCED]) * 4 / denominator
        return None

