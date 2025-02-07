from treesumstats.basic_sumstats import BasicFeatureCalculator
from treesumstats.branch_sumstats import BranchFeatureCalculator
from treesumstats.event_time_sumstats import EventTimeFeatureCalculator
from treesumstats.ltt_sumstats import LTTFeatureCalculator
from treesumstats.subtree_sumstats import SubtreeFeatureCalculator
from treesumstats.topology_sumstats import TopologyFeatureCalculator
from treesumstats import FeatureRegistry, FeatureManager
from treesumstats.resolution_sumstats import ResolutionFeatureCalculator
from treesumstats.transmission_chain_sumstats import TransmissionChainFeatureCalculator
from treesumstats.tree_manager import read_forest

FeatureRegistry.register(ResolutionFeatureCalculator())
FeatureRegistry.register(TopologyFeatureCalculator())
FeatureRegistry.register(EventTimeFeatureCalculator())
FeatureRegistry.register(BasicFeatureCalculator())
FeatureRegistry.register(BranchFeatureCalculator())
FeatureRegistry.register(TransmissionChainFeatureCalculator())
FeatureRegistry.register(LTTFeatureCalculator())
FeatureRegistry.register(SubtreeFeatureCalculator())



def main():
    """
    Entry point for tree encoding with command-line arguments.
    :return: void
    """
    import argparse

    parser = argparse.ArgumentParser(description="Encode trees with summary statistics.")
    parser.add_argument('--nwk', type=str, default='/home/azhukova/projects/bdpn/simulations_dl/test/BDCT0/forest.1.nwk', help="input tree/forest files in newick format")
    params = parser.parse_args()

    forest = read_forest(params.nwk)


    for feature_name, value in zip(FeatureManager.available_features(), FeatureManager.compute_features(forest)):
        print(f'{feature_name}\t{value}\t({FeatureManager.help(feature_name)})')


if '__main__' == __name__:
    main()