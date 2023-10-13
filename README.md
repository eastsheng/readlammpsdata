# readlammpsdata

A script for reading LAMMPS data



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
```

### Fixes

- 2023-10-12
  - [x] Add the `sort_lmp` function;
  - [x] Add the `lmp2xyz` function;
  - [x] Add the `msi2clayff` function;
  - [x] Add the `lmp2tip4p` function;
  
- 2023-10-08
  - [x] Add the `pdb2xyz` function;
  - [x] Add the `read_formula` function;
  - [x] Add the `modify_pos` function;
  - [x] Add the `modify_pore_size` function;
- 2023-09-23
  - [x] Replace the `read_Natoms` to the `read_atom_info` function;
  - [x] Add the `read_vol` function;
  - [x] Add the `read_xyz` function;
  - [x] Add the `read_pdb` function;
- 2023-09-22
  - [x] Add the `read_terms` function for reading complex LAMMPS data;
- 2023-09-11
  - [x] Add `read_box ` function;
  - [x] Add `read_Natoms ` function;
  - [x] Add `read_charges ` function;
