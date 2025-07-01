#!/bin/bash
#SBATCH --job-name="rfm_Matlab_Parallel_MonteCarloPi"
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --output=rfm_job.out
#SBATCH --error=rfm_job.err
#SBATCH --time=0:40:0
#SBATCH --partition=lr6
#SBATCH --account=scs
#SBATCH --qos=lr_debug
module load matlab
srun --cpus-per-task=8 matlab -nosplash -nodesktop -r parallel_monte_carlo
