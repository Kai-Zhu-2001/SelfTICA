#### Supporting data for the paper:
## "Everything everywhere all at once, a probability-based enhanced sampling approach to rare events"
### Repo structure
- **tutorials**: contains detailed tutorials for the training of the SelfTICA CV and the dual-cutoff GNN framework.
- **plumed_pytorch_gnn**: contains the plumed interface for GNN-based CVs
- **alanine**:  files for alanine dipeptide in vacuum using `Gromacs`
  - **data**: topology files
  - **models**: frozen torchscript models
  - **run_biased_multi**: input files for multithermal simulations
  - **run_biased_nn**: input files for biased simulations using fnn-based CVs
  - **run_biased_gnn**: input files for biased simulations using gnn-based CVs
  - **run_biased_ref**: input files for biased simulations using phi and psi as CVs
- **chignolin**: files for chignolin folding in explicit water using `Gromacs`
  - **data**: topology and force field files
  - **models**: frozen torchscript models
  - **run_biased_multi**: input files for multithermal simulations
  - **run_biased_multi_gnn**: input files for multi-walker biased simulations using gnn-based SelfTICA CVs
- **sodium**: files for sodium phase transition using `LAMMPS`
  - **data**: topology files
  - **models**: frozen torchscript models
  - **run_unibased**: input files for unibased simulations in both liquid and solid states
  - **run_biased_gnn**: input files for biased simulations using gnn-based SelfTICA CVs
  - **run_biased_ref**: input files for biased simulations using order parameter, potential energy, and volumeas as CVs
- **calixarene**: files for OAMe-G2 binding in explicit water using `Gromacs`
  - **data**: topology files
  - **models**: frozen torchscript models
  - **run_unibased**: input files for unibased simulations in both bind and unbind states
  - **run_biased_gnn**: input files for biased simulations using gnn-based SelfTICA CVs
  - **run_biased_ref**: input files for biased simulations using order h and V2 as CVs
