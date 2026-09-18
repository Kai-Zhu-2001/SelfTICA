# Reproducing the simulations

[Back to the repository overview](../README.md)

This repository provides archived inputs, models, selected COLVAR data, and custom PLUMED actions. Training notebooks and the larger data collection are linked from the [overview](../README.md#training-code-and-tutorials). Use the paper's [Methods and Supplementary Information](https://arxiv.org/html/2606.15495v3) for system preparation, training settings, and analysis protocols.

## Software requirements

Install the software needed for the selected system before using the commands below.

| Workflow | Requirements |
| --- | --- |
| Tri-well dynamics | PLUMED with the VES module (`ves_md_linearexpansion`); OPES for biased runs |
| Alanine, chignolin, and OAMe–G2 | GROMACS with PLUMED integration; OPES for the supplied biased runs |
| Fe–N₂ | LAMMPS with `fix plumed` and the `mace` pair style; the supplied MACE potential in `fen2/data/` |
| Neural-network CVs | PLUMED with PyTorch/LibTorch support; the matching exported model |
| GNN CVs | The appropriate [GNN interface](../plumed_pytorch_gnn/README.md); Python with MDTraj for `@mdt` atom selections |
| Committor-based bias | LibTorch-enabled PLUMED and [PytorchKolmogorovBias.cpp](../transfer/PytorchKolmogorovBias.cpp) |

The [Supplementary Information](https://arxiv.org/html/2606.15495v3) reports GROMACS 2022.5 for alanine and 2024.5 for chignolin and OAMe–G2. A complete environment lockfile and a tested compatibility matrix are not included here. For training reproduction, obtain the frozen code identified in the paper from the [dataset archive](https://huggingface.co/datasets/Kai-Zhu-2001/SelfTICA); the linked mlcolvar branches may change over time.

## Input and model conventions

| Files | Role |
| --- | --- |
| `plumed.dat`, `plumed-*.dat` | CV definitions, descriptors, biases, and output settings |
| `md_input`, `md_potential` | Tri-well dynamics settings and potential coefficients |
| `*.tpr` | Prepared GROMACS run inputs; the generating `.mdp` files are not included here |
| `in.lammps`, `data.lammps` | LAMMPS run settings and atomic configuration |
| `models/*.pt` and nested model directories | Saved models; use the exact model referenced by the chosen input |
| `COLVAR`, `COLVAR_A`, `COLVAR_B` | Tabulated CV trajectories; column names are recorded in the `#! FIELDS` header |

Transfer-learning files live in `transfer/tri-well/`, `transfer/ala2/`, and `transfer/chignolin/`. Their models include pretraining checkpoints (`*model_state.pt`) and task-specific `*_q.pt` / `*_z.pt` exports. The Kolmogorov-bias inputs reference the `z` models; checkpoints are not interchangeable with simulation exports. Alanine and chignolin transfer inputs include `iter_0` and `iter_1` sampling rounds.

## Launch examples

Use a separate working copy of the repository for simulations: some run directories already contain archived `COLVAR` files, and simulations write into the current directory. Keep the directory layout so that relative paths to models, structures, and C++ sources resolve. Each command block below starts from the root of that working copy.

### Tri-well: unbiased dynamics

```bash
cd tri-well/run_unbiased/1.0kbt
plumed ves_md_linearexpansion md_input
```

This example requires no neural-network model. The archived input requests 10,000,000 steps at a reduced temperature of 1.0; it is a full simulation, not a short installation test. `plumed.dat` writes `COLVAR`, while `md_input` names the potential-grid and histogram outputs. See the [PLUMED command documentation](https://www.plumed.org/doc-v2.9/user-doc/html/ves_md_linearexpansion.html).

### Alanine: unbiased dynamics at 500 K

```bash
cd alanine/run_unbiased/500K
gmx mdrun -s ala2.tpr -plumed plumed.dat -deffnm md
```

Use a GROMACS executable with PLUMED integration that can read the supplied `.tpr`. This input writes torsions, energy, and distance descriptors to `COLVAR`. Other GROMACS runs use the `.tpr` in their own directory (for example, `md.tpr`, `fold.tpr`, or `input.sA.tpr`) and may require custom actions and models.

### Fe–N₂: initial sampling

```bash
cd fen2/run_initial
lmp -in in.lammps
```

The executable name may differ by installation. The input uses the MACE potential in `../data/`, runs initial OPES sampling, and writes `COLVAR`, `traj.lammps`, logs, and restart files. Consult the [LAMMPS PLUMED integration documentation](https://docs.lammps.org/fix_plumed.html) for the required build support.

## Input compatibility notes

- **GNN interfaces:** both C++ implementations register `PYTORCH_GNN`, but accept different selection keywords and model formats. Load the implementation required by the model; see the [interface guide](../plumed_pytorch_gnn/README.md).
- **Fe–N₂ OPES-Explore inputs:** all three `fen2/run_biased_explore/` cases use `GROUPA`, while their loaded `PytorchModelGNN.cpp` accepts `SYSTEM_SELECTION`. Resolve the input/interface/model compatibility before launching these cases. They also request `CUDA`; the interface guide explains GPU requirements and CPU fallback.
- **Chignolin transfer restarts:** the biased transfer inputs use `RESTART=YES`. The required prior bias state is not included in this checkout; supply matching restart files or prepare a consistent fresh-start input before running.
- **OAMe–G2 static bias:** the static DeepTDA bias line in `calixanrene/run_biased_gnn/SelfTICA/plumed.dat` is commented out. Reproducing the combined-bias protocol described in the paper requires the corresponding prior OPES kernels and an appropriate kernel-file path.
- **Archive names:** the host–guest directory is spelled `calixanrene/`, and chignolin inputs include `plumed-desctiptors.dat`. Use these exact paths when working with the archive.

## Recording a reproduction

Record the repository commit (`git rev-parse HEAD`), dataset revision, training-code commit, software/build versions, and any input edits with each run. Preserve random seeds and model identities when comparing with the reported results. Use `COLVAR` headers and the `PRINT` directives to identify observables; output columns vary between systems.

The launch commands document the intended workflows. Successful execution and agreement with the paper still require validation in the appropriate simulation environment.
