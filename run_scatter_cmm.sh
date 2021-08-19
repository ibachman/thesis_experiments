#!/bin/bash

#SBATCH -J niclabs
#SBATCH --ntasks=1
#SBATCH --array=1-4
#SBATCH --mem-per-cpu=1000M
#SBATCH -p general
#SBATCH --output=nt_log_%A_%a.out
#SBATCH --mail-user=ivana@niclabs.cl (--mail-user=ivana@niclabs.cl)
#SBATCH --mail-type=ALL

ml Python/3.8.2

pip3 install -r requirements.txt

srun python3 -u data_proc/thesis_figures.py 5NN simple_graphs
srun python3 -u data_proc/thesis_figures.py GPA simple_graphs
srun python3 -u data_proc/thesis_figures.py YAO simple_graphs
srun python3 -u data_proc/thesis_figures.py ER simple_graphs
