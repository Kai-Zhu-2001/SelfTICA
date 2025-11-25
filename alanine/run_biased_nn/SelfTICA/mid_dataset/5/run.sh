#!/bin/bash
#SBATCH -J ala2_tica
#SBATCH -o ala2_tica.log
#SBATCH -e ala2_tica.err 
#SBATCH -N 1
#SBATCH -p gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
##SBATCH -w gpu06

export LD_PRELOAD="/home/zhukai/anaconda3/envs/mlcolvar-gnn/lib/python3.10/site-packages/torch/lib/libc10.so:/home/zhukai/anaconda3/envs/mlcolvar-gnn/lib/python3.10/site-packages/torch/lib/libtorch_cpu.so:/home/zhukai/opt/plumed2.9.3-gnn/lib/libplumedKernel.so"
module load cuda/11.8
gmx_mpi mdrun -ntomp 8 -bonded gpu --plumed plumed.dat -s ala2.tpr -nsteps 10000000  


