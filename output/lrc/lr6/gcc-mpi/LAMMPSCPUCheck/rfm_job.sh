#!/bin/bash
#SBATCH --job-name="rfm_LAMMPSCPUCheck"
#SBATCH --ntasks=24
#SBATCH --ntasks-per-node=12
#SBATCH --output=rfm_job.out
#SBATCH --error=rfm_job.err
#SBATCH --time=0:40:0
#SBATCH --exclusive
#SBATCH --partition=lr6
#SBATCH --account=scs
#SBATCH --qos=lr_debug
module load gcc
module load openmpi
module load lammps
srun lmp -in in.lj
