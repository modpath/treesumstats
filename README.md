# treesumstats

Representing phylogenetic trees (or forests of such trees) as summary statistics.



[//]: # ([![DOI:10.1093/sysbio/syad059]&#40;https://zenodo.org/badge/DOI/10.1093/sysbio/syad059.svg&#41;]&#40;https://doi.org/10.1093/sysbio/syad059&#41;)
[//]: # ([![GitHub release]&#40;https://img.shields.io/github/v/release/evolbioinfo/treesumstats.svg&#41;]&#40;https://github.com/evolbioinfo/treesumstats/releases&#41;)
[![PyPI version](https://badge.fury.io/py/treesumstats.svg)](https://pypi.org/project/treesumstats/)
[![PyPI downloads](https://shields.io/pypi/dm/treesumstats)](https://pypi.org/project/treesumstats/)
[![Docker pulls](https://img.shields.io/docker/pulls/evolbioinfo/treesumstats)](https://hub.docker.com/r/evolbioinfo/treesumstats/tags)

## Implemented summary statistics



## Input data
One needs to supply a time-scaled phylogenetic tree in newick format. 
If the file contains several trees (one tree per line), it will be considered as a forest.

## Installation

There are 4 alternative ways to run __treesumstats__ on your computer: 
with [docker](https://www.docker.com/community-edition), 
[apptainer](https://apptainer.org/),
in Python3, or via command line (requires installation with Python3).



### Run in python3 or command-line (for linux systems, recommended Ubuntu 21 or newer versions)

You could either install python (version 3.9 or higher) system-wide and then install treesumstats via pip:
```bash
sudo apt install -y python3 python3-pip python3-setuptools python3-distutils
pip3 install treesumstats
```

or alternatively, you could install python (version 3.9 or higher) and treesumstats via [conda](https://conda.io/docs/) (make sure that conda is installed first). 
Here we will create a conda environment called _phyloenv_:
```bash
conda create --name phyloenv python=3.9
conda activate phyloenv
pip install treesumstats
```


#### Basic usage in a command line
If you installed __treesumstats__ in a conda environment (here named _phyloenv_), do not forget to first activate it, e.g.

```bash
conda activate phyloenv
```

[//]: # (Run the following commands to check for the presence of partner notification and estimate BD-PN model parameters.)

[//]: # (The first command applies the PN test to a tree Zurich.nwk and saves the PN-test value to the file cherry_test.txt)

[//]: # (The second command estimated the BD-PN parameters and their 95% CIs for this tree, assuming the sampling probability of 0.25, )

[//]: # (and saves the estimated parameters to a comma-separated file estimates_bdpn.csv.)

[//]: # (The third command estimated the classical BD parameters and their 95% CIs for this tree, assuming the sampling probability of 0.25, )

[//]: # (and saves the estimated parameters to a comma-separated file estimates_bd.csv.)

[//]: # (```bash)

[//]: # (pn_test --nwk Zurich.nwk --log cherry_test.txt)

[//]: # (bdpn_infer --nwk Zurich.nwk --ci --p 0.25 --log estimates_bdpn.csv)

[//]: # (bd_infer --nwk Zurich.nwk --ci --p 0.25 --log estimates_bd.csv)

[//]: # (```)

#### Help

To see detailed options, run:
```bash
treesumstats_encode --help
```


### Run with docker

#### Basic usage
Once [docker](https://www.docker.com/community-edition) is installed, 

[//]: # (run the following command to estimate BD-PN model parameters:)

[//]: # (```bash)

[//]: # (docker run -v <path_to_the_folder_containing_the_tree>:/data:rw -t evolbioinfo/bdpn --nwk /data/Zurich.nwk --ci --p 0.25 --log /data/estimates.csv)

[//]: # (```)

[//]: # ()
[//]: # (This will produce a comma-separated file estimates.csv in the <path_to_the_folder_containing_the_tree> folder,)

[//]: # ( containing the estimated parameter values and their 95% CIs &#40;can be viewed with a text editor, Excel or Libre Office Calc&#41;.)

#### Help

To see advanced options, run
```bash
docker run -t evolbioinfo/treesumstats -h
```



### Run with apptainer

#### Basic usage
Once [apptainer](https://apptainer.org/docs/user/latest/quick_start.html#installation) is installed, 

[//]: # (run the following command to estimate BD-PN model parameters &#40;from the folder where the Zurich.nwk tree is contained&#41;:)

[//]: # ()
[//]: # (```bash)

[//]: # (apptainer run docker://evolbioinfo/bdpn --nwk Zurich.nwk --ci --p 0.25 --log estimates.csv)

[//]: # (```)
[//]: # ()
[//]: # (This will produce a comma-separated file estimates.csv,)

[//]: # ( containing the estimated parameter values and their 95% CIs &#40;can be viewed with a text editor, Excel or Libre Office Calc&#41;.)


#### Help

To see advanced options, run
```bash
apptainer run docker://evolbioinfo/treesumstats -h
```


