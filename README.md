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

Atoms = rld.read_data(lammpsdata.lmp, data_sub_str = "Atoms # full")
Masses = rld.read_data(lammpsdata.lmp, data_sub_str = "Masses")
```

