# readlammpsdata

A script for reading and modifying LAMMPS data



### Install

```bash
# install from github
git clone git@github.com:eastsheng/readlammpsdata.git
cd readlammpsdata
pip install .
# install from pypi
pip install readlammpsdata
```



### Usages

```python
import readlammpsdata as rld

# 0. read Atoms, Masses etc.
Atoms = rld.read_data(lmp, data_sub_str = "Atoms # full")
Masses = rld.read_data(lmp, data_sub_str = "Masses")
PairCoeffs = rld.read_data(lmp, data_sub_str = "Pair Coeffs")
Bonds = rld.read_data(lmp, data_sub_str = "Bonds")

# 1. read box size
xyz = rld.read_box(lmp)
Lx = xyz["xhi"]-xyz["xlo"]
print(xyz)
print(Lx)

# 2. read atomic number 
Natoms = rld.read_atom_info(lmp,"atoms")
print("Number of atoms is %s" %Natoms)

# 3. read charges 
charges = rld.read_charges(lmp)
print("Charges of atoms are %s" %charges)
print(round(sum(charges),6))
# 4. ......
print(help(rld)) # for read all functions
```

### Fixes

- 2023-11-22
  - [x] Added the `change_lmp_axis` function
  - [x] Added the `coord2zero` function
  - [x] Added the `addH` function
  - [x] Added the `cut_lmp_atoms` function
- 2023-10-21
  - [x] Added the `exchange_position` function
- 2023-10-20
  - [x] Added  the `change_type_order` function
  - [x] Added the `combine_lmp` function
  - [x] Added the `cut_lmp` function
- 2023-10-17
  - [x] Added the `move_boundary` function;

  - [x] Added the `density` function;
- 2023-10-16
  - [x] Added the `modify_methane_hydrate` function;
  - [x] Added  the `modify_header` function;
  - [x] Added the `add_atoms` function;
  - [x] Added the `array2str` function;
- 2023-10-12

  - [x] Added the `sort_lmp` function;

  - [x] Added  the `lmp2xyz` function;
  - [x] Added the `msi2clayff` function;
  - [x] Added the `lmp2tip4p` function;
- 2023-10-08
  - [x] Added the `pdb2xyz` function;
  - [x] Added the `read_formula` function;
  - [x] Added the `modify_pos` function;
  - [x] Added the `modify_pore_size` function;
- 2023-09-23
  - [x] Replaced the `read_Natoms` to the `read_atom_info` function;
  - [x] Added the `read_vol` function;
  - [x] Added the `read_xyz` function;
  - [x] Added the `read_pdb` function;
- 2023-09-22
  - [x] Added the `read_terms` function for reading complex LAMMPS data;
- 2023-09-11
  - [x] Added `read_box ` function;
  - [x] Added `read_Natoms ` function;
  - [x] Added `read_charges ` function;
