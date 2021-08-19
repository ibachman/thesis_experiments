#!/bin/bash

#SBATCH -J niclabs
#SBATCH -c 10
#SBATCH -p general
#SBATCH --output=log_%A.out
#SBATCH -e err_%A.err
#SBATCH --mail-user=ivana@niclabs.cl (--mail-user=ivana@niclabs.cl)
#SBATCH --mail-type=ALL

ml Python/3.8.2

mkdir -p test_results/degree
mkdir -p test_results/distance
mkdir -p test_results/random
mkdir -p test_results/simple_graphs
mkdir -p test_results/seismic

pip3 install -r requirements.txt

srun python3 -u job_manager.py -g jobs-api.felipequintanilla.cl -m cmm -w 10
