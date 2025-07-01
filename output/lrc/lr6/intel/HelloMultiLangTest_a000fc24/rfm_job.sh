#!/bin/bash
#SBATCH --job-name="rfm_HelloMultiLangTest_a000fc24"
#SBATCH --ntasks=1
#SBATCH --output=rfm_job.out
#SBATCH --error=rfm_job.err
#SBATCH --time=0:40:0
#SBATCH --partition=lr6
#SBATCH --account=scs
#SBATCH --qos=lr_debug
module load intel-oneapi-compilers
srun ./HelloMultiLangTest_2
