import unittest

import numpy as np
from ete3 import Tree

from treesumstats import FeatureManager, FeatureRegistry, NORMALIZED, BASIC_ARRAY_METRICS
from treesumstats.transmission_chain_sumstats import TransmissionChainFeatureCalculator, CHAIN, CHAIN_PERCENTILES

NWK = '((A:0.2, B:0.3, A1:0.4)AB:1, (C:0.8, (D:1.2, (E:1.4, F:0.1)EF:1.7)DF:1.5)CF:0.3)root:0.1;'

FeatureRegistry.register(TransmissionChainFeatureCalculator(chain_len=2))


class TransmissionChainTest(unittest.TestCase):


    def test_n_chain_stats(self):
        tree = Tree(NWK, format=3)

        features = [f'n_2-{CHAIN}', f'n_2-{CHAIN}_{NORMALIZED}']

        chains = np.array([0.3 + 0.8, 1.5 + 1.2, 1.7 + 0.1])
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [len(chains), len(chains) / 5]):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

    def test_chain_metric_stats(self):
        tree = Tree(NWK, format=3)

        features = [f'brlen_sum_2-{CHAIN}_{flavour}' for flavour in BASIC_ARRAY_METRICS]

        chains = np.array([0.3 + 0.8, 1.5 + 1.2, 1.7 + 0.1])
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   [np.mean(chains), np.min(chains), np.max(chains), np.var(chains), np.median(chains)]):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')

    def test_chain_percentile_stats(self):
        tree = Tree(NWK, format=3)

        features = [f'brlen_sum_2-{CHAIN}_perc{p}' for p in CHAIN_PERCENTILES]

        chains = np.array([0.3 + 0.8, 1.5 + 1.2, 1.7 + 0.1])
        for feature_name, value, real_value in zip(features,
                                                   FeatureManager.compute_features([tree], *features),
                                                   np.percentile(chains, CHAIN_PERCENTILES)):
            print(feature_name, real_value, value)
            self.assertAlmostEqual(real_value, value, places=6, msg=f'Wrong {feature_name} value')
