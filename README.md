#### Supporting Data for the Paper  
## "Contrastive Learning of Dynamical Representations for Enhanced Molecular Sampling"
Kai Zhu, Jintu Zhang, Pietro Novelli, Tingjun Hou, Luigi Bonati

[![arXiv](https://img.shields.io/badge/arXiv-2606.15495-b31b1b.svg)](https://arxiv.org/abs/2606.15495)

All simulation trajectories, input files, trained models, and supporting data are available in the Hugging Face dataset repository:
https://huggingface.co/datasets/Kai-Zhu-2001/SelfTICA

The training of the models was based on the [mlcolvar library](https://github.com/luigibonati/mlcolvar), where the updated relevant code and example notebooks are available:

- [SelfTICA source code](https://github.com/luigibonati/mlcolvar/blob/release/2.0/mlcolvar/cvs/timelagged/selftica.py)
- [SelfTICA tutorial: Müller–Brown potential](https://github.com/luigibonati/mlcolvar/blob/release/2.0/docs/notebooks/tutorials/cvs_SelfTICA.ipynb)

### Repo Structure

- **tutorials**  
  Contains step-by-step tutorials for training SelfTICA collective variables (CVs), including both feed-forward and dual-cutoff GNN-based frameworks.

- **plumed_pytorch_gnn**  
  Provides the PLUMED interface for deploying PyTorch-based GNN CVs in molecular dynamics simulations.

---

- **muller**  
  Files for the tri-well potential system using `PLUMED ves_md_linearexpansion`.
  - **models**: frozen TorchScript models  
  - **run_unbiased**: input files and trajectories from unbiased simulations at different temperatures (used for training)  
  - **run_biased**: input files for biased simulations at $k_B T = 0.6$ used for training  

---

- **alanine**  
  Files for alanine dipeptide in vacuum using `GROMACS`.
  - **data**: topology files  
  - **models**: frozen TorchScript models  
  - **run_biased_multi**: input files for multithermal simulations  
  - **run_biased_nn**: biased simulations using FNN-based CVs  
  - **run_biased_gnn**: biased simulations using GNN-based CVs  

---

- **chignolin**  
  Files for chignolin folding in explicit water using `GROMACS`.
  - **data**: topology and force field files  
  - **models**: frozen TorchScript models  
  - **run_biased_explore**: input files for OPES-Explore simulations using different CVs  

---

- **calixarene**  
  Files for OAMe–G2 host–guest binding in explicit water using `GROMACS`.
  - **data**: topology and force field files  
  - **models**: frozen TorchScript models  
  - **run_unbiased**: input files for unbiased simulations in both bound and unbound states  
  - **run_biased_gnn**: biased simulations using GNN-based SelfTICA CVs  
  - **run_biased_ref**: biased simulations using reference CVs (e.g., coordination number $h$ and $V_2$)  

---

- **fen2**  
  Files for catalytic dissociation of $\mathrm{N_2}$ on Fe(111) surfaces using `LAMMPS`.
  - **data**: topology files  
  - **models**: frozen TorchScript models  
  - **run_initial**: initial biased simulations used to generate training data  
  - **run_biased_explore**: OPES-Explore simulations using different CVs  
