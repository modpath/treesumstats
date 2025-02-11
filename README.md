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

Run the following command to calculate the summary statistics for an input tree _tree.nwk_ and save them to an output tab-delimited file _stats.tab_. 
(The non-mandatory option _--add_descriptions_ would add a column with statistics descriptions to the output table.)

```bash
treesumstats_encode --nwk tree.nwk --tab stats.tab --add_descriptions
```

#### Help

To see detailed options, run:
```bash
treesumstats_encode --help
```


### Run with docker

#### Basic usage
Once [docker](https://www.docker.com/community-edition) is installed, 

run the following command to calculate the summary statistics for an input tree _tree.nwk_ and save them to an output tab-delimited file _stats.tab_. 
(The non-mandatory option _--add_descriptions_ would add a column with statistics descriptions to the output table.)


```bash
docker run -v <path_to_the_folder_containing_the_tree>:/data:rw -t evolbioinfo/treesumstats --nwk /data/tree.nwk --tab /data/stats.tab --add_descriptions
```


This will produce a tab-delimited file _stats.tab_ in the <path_to_the_folder_containing_the_tree> folder,

 containing the summary statistic names in the _statistic_ column, their values in the _value_ column and their descriptions in the _description_ column. 

#### Help

To see advanced options, run
```bash
docker run -t evolbioinfo/treesumstats -h
```



### Run with apptainer

#### Basic usage
Once [apptainer](https://apptainer.org/docs/user/latest/quick_start.html#installation) is installed, 

run the following command to calculate the summary statistics for an input tree _tree.nwk_ and save them to an output tab-delimited file _stats.tab_. 
(The non-mandatory option _--add_descriptions_ would add a column with statistics descriptions to the output table.)


```bash
apptainer run docker://evolbioinfo/treesumstats --nwk tree.nwk --tab stats.tab --add_descriptions
```


This will produce a tab-delimited file _stats.tab_,

 containing the summary statistic names in the _statistic_ column, their values in the _value_ column and their descriptions in the _description_ column. 


#### Help

To see advanced options, run
```bash
apptainer run docker://evolbioinfo/treesumstats -h
```


