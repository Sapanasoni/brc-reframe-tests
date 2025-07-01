#!/bin/bash
#SBATCH --job-name="rfm_HelloMultiLangTest_a000fc24"
#SBATCH --ntasks=1
#SBATCH --output=rfm_job.out
#SBATCH --error=rfm_job.err
#SBATCH --time=0:40:0
#SBATCH --partition=savio3
#SBATCH --account=ac_scsguest
#SBATCH --qos=savio_debug
module load gcc
srun ./HelloMultiLangTest_2
