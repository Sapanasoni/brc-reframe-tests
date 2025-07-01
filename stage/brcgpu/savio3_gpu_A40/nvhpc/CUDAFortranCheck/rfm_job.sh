#!/bin/bash
#SBATCH --job-name="rfm_CUDAFortranCheck"
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --output=rfm_job.out
#SBATCH --error=rfm_job.err
#SBATCH --time=0:40:0
#SBATCH --partition=savio3_gpu
#SBATCH --account=ac_scsguest
#SBATCH --qos=savio_debug
#SBATCH --gres=gpu:A40:1
module load nvhpc
srun --cpus-per-task=2 ./CUDAFortranCheck
