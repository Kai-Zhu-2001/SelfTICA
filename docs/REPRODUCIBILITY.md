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
| GNN CVs | The appropriate [GNN interface](../plumed/README.md); Python with MDTraj for `@mdt` atom selections |
| Committor-based bias | LibTorch-enabled PLUMED and [PytorchKolmogorovBias.cpp](../plumed/PytorchKolmogorovBias.cpp) |

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

Transfer-learning files live in `transfer/tri-well/`, `transfer/alanine/`, and `transfer/chignolin/`. Their models include pretraining checkpoints (`*model_state.pt`) and task-specific `*_q.pt` / `*_z.pt` exports. The Kolmogorov-bias inputs reference the `z` models; checkpoints are not interchangeable with simulation exports. Alanine and chignolin transfer inputs include `iter_0` and `iter_1` sampling rounds.

## Preparing generated inputs

Some repeated simulation inputs are generated at their historical run paths before launch. Use Python 3.9 or newer and invoke the preparation CLI from the repository root:

```bash
python scripts/prepare_runs.py --list
python scripts/prepare_runs.py --check
python scripts/prepare_runs.py --run REPO_RELATIVE_RUN_DIRECTORY
python scripts/prepare_runs.py --all
```

`--list` shows preparation targets only. `--check` validates the full catalog without writing, `--run` prepares one exact leaf run directory, and `--all` prepares every catalog entry. The shared-file catalog is `scripts/shared-inputs.json`. Canonical files live in each system's `common/` directory, while the 120 alanine experiments are recorded in `alanine/experiments.csv` and rendered from `alanine/templates/fnn.dat.in` or `alanine/templates/gnn.dat.in`. The templates' only placeholder is `@MODEL_PATH@`.

Generated inputs are ignored by Git. For lasting changes, edit the shared source, template, or CSV rather than its generated copy. A shared file can contain paths relative to its destination run directory; do not execute inputs directly from `common/`. Models, scientific data, numerical settings, and simulation dependencies remain unchanged by preparation.

Preparation is safe to repeat: an identical existing file is skipped. If any selected destination differs, the command aborts before writing any selected files. To refresh a deliberately changed generated input, manually move that specific file aside and run preparation again; avoid broad cleanup commands. Run simulations in an independent working copy because archived and newly produced outputs share run directories. Keeping each simulation in its original run directory preserves relative references and isolates its outputs from other runs.

## Launch examples

Use a separate working copy of the repository for simulations: some run directories already contain archived `COLVAR` files, and simulations write into the current directory. Keep the directory layout so that relative paths to models, structures, and C++ sources resolve. Each command block below starts from the root of that working copy and prepares the selected generated inputs before changing directories.

### Tri-well: unbiased dynamics

```bash
python scripts/prepare_runs.py --run tri-well/run_unbiased/1.0kbt
cd tri-well/run_unbiased/1.0kbt
plumed ves_md_linearexpansion md_input
```

This example requires no neural-network model. The archived input requests 10,000,000 steps at a reduced temperature of 1.0; it is a full simulation, not a short installation test. `plumed.dat` writes `COLVAR`, while `md_input` names the potential-grid and histogram outputs. See the [PLUMED command documentation](https://www.plumed.org/doc-v2.9/user-doc/html/ves_md_linearexpansion.html).

### Alanine: unbiased dynamics at 500 K

```bash
python scripts/prepare_runs.py --run alanine/run_unbiased/500K
cd alanine/run_unbiased/500K
gmx mdrun -s ala2.tpr -plumed plumed.dat -deffnm md
```

Use a GROMACS executable with PLUMED integration that can read the supplied `.tpr`. This input writes torsions, energy, and distance descriptors to `COLVAR`. Other GROMACS runs use the `.tpr` in their own directory (for example, `md.tpr`, `fold.tpr`, or `input.sA.tpr`) and may require custom actions and models.

### Fe–N₂: initial sampling

`fen2/run_initial` is unchanged and does not need preparation.

```bash
cd fen2/run_initial
lmp -in in.lammps
```

The executable name may differ by installation. The input uses the MACE potential in `../data/`, runs initial OPES sampling, and writes `COLVAR`, `traj.lammps`, logs, and restart files. Consult the [LAMMPS PLUMED integration documentation](https://docs.lammps.org/fix_plumed.html) for the required build support.

## Input compatibility notes

- **GNN interfaces:** both C++ implementations register `PYTORCH_GNN`, but accept different selection keywords and model formats. Load the implementation required by the model; see the [interface guide](../plumed/README.md).
- **Fe–N₂ OPES-Explore inputs:** all three `fen2/run_biased_explore/` cases use `GROUPA`, while their loaded `PytorchModelGNN.cpp` accepts `SYSTEM_SELECTION`. Resolve the input/interface/model compatibility before launching these cases. They also request `CUDA`; the interface guide explains GPU requirements and CPU fallback.
- **Chignolin transfer restarts:** the biased transfer inputs use `RESTART=YES`. The required prior bias state is not included in this checkout; supply matching restart files or prepare a consistent fresh-start input before running.
- **OAMe–G2 static bias:** the static DeepTDA bias line in `calixarene/run_biased_gnn/SelfTICA/plumed.dat` is commented out. Reproducing the combined-bias protocol described in the paper requires the corresponding prior OPES kernels and an appropriate kernel-file path.

## Recording a reproduction

Record the repository commit (`git rev-parse HEAD`), dataset revision, training-code commit, software/build versions, and any input edits with each run. Preserve random seeds and model identities when comparing with the reported results. Use `COLVAR` headers and the `PRINT` directives to identify observables; output columns vary between systems.

The launch commands document the intended workflows. Successful execution and agreement with the paper still require validation in the appropriate simulation environment.
