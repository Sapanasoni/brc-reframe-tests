#!/bin/bash
#SBATCH --job-name="rfm_OpenACCFortranCheck_39c80135"
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=2
#SBATCH --output=rfm_job.out
#SBATCH --error=rfm_job.err
#SBATCH --time=0:40:0
#SBATCH --partition=savio4_gpu
#SBATCH --account=ac_scsguest
#SBATCH --qos=a5k_gpu4_normal
#SBATCH --mincpus=4
#SBATCH --gres=gpu:A5000:1
#SBATCH --cpus-per-task=4
module load nvhpc
srun --cpus-per-task=2 ./OpenACCFortranCheck
