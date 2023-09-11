# readlammpsdata

A script for reading lammps data



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
Atoms = rld.read_data(lammpsdata.lmp, data_sub_str = "Atoms # full")
Masses = rld.read_data(lammpsdata.lmp, data_sub_str = "Masses")

# 1. read box size
xyz = rld.read_box(lmp)
Lx = xyz["xhi"]-xyz["xlo"]
print(xyz)
print(Lx)

# 2. read atomic number 
Natoms = rld.read_Natoms(lmp)
print("Number of atoms is %s" %Natoms)

# 3. read charges 
charges = rld.read_charges(lmp)
print("Charges of atoms are %s" %charges)
print(round(sum(charges),6))
```

### Fixes

- 2023-09-11

  - [x] Add `read_box ` function.

  - [x] Add `read_Natoms ` function.

  - [x] Add `read_charges ` function.
