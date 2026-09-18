# Custom PLUMED interfaces

This directory contains two GNN interfaces and a descriptor-based committor-bias
interface. All three require PLUMED with LibTorch support.

## GNN collective variables

The GNN sources evaluate exported TorchScript graph neural networks during
molecular dynamics and expose their collective variables as `gnn.node-0`,
`gnn.node-1`, and so on. PLUMED can then use these outputs in biasing actions.

### Choose the matching interface

Both files register the **same `PYTORCH_GNN` action**. Load only the source that
matches the exported model and input syntax; they are not interchangeable.

| Property | [PytorchGNN.cpp](PytorchGNN.cpp) | [PytorchModelGNN.cpp](PytorchModelGNN.cpp) |
| --- | --- | --- |
| System atoms | `GROUPA` | `SYSTEM_SELECTION` |
| Optional environment atoms | `GROUPB` | `ENVIRONMENT_SELECTION` |
| Optional subsystem atoms | `SUBGROUPA` | `SUBSYSTEM_SELECTION` |
| Environment buffer | `BUFFER` input, in PLUMED length units | Model attribute `buffer`, in angstroms |
| Output-count attribute | Exactly one of `n_out` or `n_cvs` | `n_out` |
| Subsystem cutoff attribute | `cutoff_l` | `long_range_cutoff` |
| TorchScript forward call | `forward(graph, false)` | `forward(graph)` |
| Committor bias | Optional `KBIAS` and related keywords | No built-in committor bias |

Both require the model attributes `atomic_numbers` and exactly one of `r_max`
or `cutoff`. Model distances and cutoffs use **angstroms**, including when
PLUMED uses another length unit. The subsystem cutoff is required when a
subsystem is selected. Environment and system groups must not overlap, and the
subsystem must be contained in the system group.

The graph dictionaries also differ: long-range edge masks are named
`edge_masks_le` in `PytorchGNN.cpp` and `edge_masks_lr` in `PytorchModelGNN.cpp`.
Export a model for the selected interface; renaming input keywords alone does
not establish model compatibility.

### Compilation and runtime requirements

- PLUMED with LibTorch support enabled (`__PLUMED_HAS_LIBTORCH`), matching
  PLUMED headers, and a C++ compiler for loading these source files.
- The LibTorch C++ library and an exported TorchScript model implementing the
  selected graph interface. A Python PyTorch installation alone is insufficient.
- A `STRUCTURE` PDB containing **all simulated atoms in simulation order**.
  Atom names must be element symbols, such as `C`, `N`, `O`, and `H`.
- For molecular dynamics, an engine connected to PLUMED; OPES must be available
  for the examples that use `OPES_METAD` or `OPES_METAD_EXPLORE`.
- Inputs using `@mdt` selections also require Python and MDTraj.

The default evaluation uses CPU and float32. `FLOAT64` selects double precision.
`CUDA` requests GPU evaluation and requires a CUDA-enabled LibTorch installation
and an available device; these sources fall back to CPU if CUDA is unavailable.
`CUDA` and `SERIAL` cannot be enabled together.

This directory does not include a standalone build system or a validated
PLUMED/LibTorch version matrix. Check compatibility with the local PLUMED build
before launching production simulations.

### Repository examples

- [Alanine SelfTICA input](../alanine/run_biased_gnn/SelfTICA/T1_dataset/0/plumed.dat):
  loads `PytorchGNN.cpp`, selects protein heavy atoms with `GROUPA`, and biases
  `gnn.node-0` with OPES.
- [Calixarene SelfTICA input](../calixarene/run_biased_gnn/SelfTICA/plumed.dat):
  adds water oxygen atoms through `GROUPB`, subsystem edges through `SUBGROUPA`,
  and an explicit `BUFFER`; OPES biases the SelfTICA output `tica.node-0`.
- [FeN2 OPES-Explore inputs](../fen2/run_biased_explore/): all three cases
  (`SelfTICA`, `d_n2`, and `coord`) load `PytorchModelGNN.cpp` but use `GROUPA`.
  The supplied source expects `SYSTEM_SELECTION`; these inputs need that
  correction and a matching model before use with the supplied interface.

Run each input from its simulation directory so that relative `LOAD`, `MODEL`,
and `STRUCTURE` paths resolve correctly. The referenced model and structure
files must also be present. Loading a source successfully does not validate a
model, atom selection, or simulation protocol.

## Committor bias

[PytorchKolmogorovBias.cpp](PytorchKolmogorovBias.cpp) registers
`PYTORCH_KOLMOGOROV_BIAS`. It takes descriptors through `ARG`, loads the scalar
`z` model specified by `FILE`, and exposes the Kolmogorov bias as `kbias`.
The simulation input applies this bias with `BIASVALUE`.

See the [tri-well example](../transfer/tri-well/biased_sims/state_A/plumed.dat)
and the [alanine example](../transfer/alanine/biased_sims/iter_0/state_A/plumed.dat)
for model paths, bias parameters, and descriptor definitions. Run each input
from its simulation directory so that the relative `LOAD` path resolves.
