#!/bin/bash
#SBATCH --job-name="rfm_MPI_HelloWorld"
#SBATCH --ntasks=2
#SBATCH --ntasks-per-node=1
#SBATCH --output=rfm_job.out
#SBATCH --error=rfm_job.err
#SBATCH --time=0:40:0
#SBATCH --partition=lr6
#SBATCH --account=scs
#SBATCH --qos=lr_debug
module load gcc
module load openmpi
srun ./MPI_HelloWorld
