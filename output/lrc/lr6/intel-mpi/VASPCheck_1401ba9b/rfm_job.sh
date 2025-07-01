#!/bin/bash
#SBATCH --job-name="rfm_VASPCheck_1401ba9b"
#SBATCH --ntasks=2
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=16
#SBATCH --output=rfm_job.out
#SBATCH --error=rfm_job.err
#SBATCH --time=0:40:0
#SBATCH --partition=lr6
#SBATCH --account=scs
#SBATCH --qos=lr_debug
module load intel-oneapi-compilers
module load intel-oneapi-mpi
module load vasp
export OMP_NUM_THREADS=16
srun --mpi=pmi2 --cpus-per-task=16 vasp_std
