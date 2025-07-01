#!/bin/bash
#SBATCH --job-name="rfm_MPI_HelloWorld"
#SBATCH --ntasks=2
#SBATCH --ntasks-per-node=1
#SBATCH --output=rfm_job.out
#SBATCH --error=rfm_job.err
#SBATCH --time=0:40:0
#SBATCH --partition=savio2
#SBATCH --account=ac_scsguest
#SBATCH --qos=savio_debug
module load intel-oneapi-compilers
module load intel-oneapi-mpi
srun --mpi=pmi2 ./MPI_HelloWorld
