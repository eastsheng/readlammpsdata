## Examples

### Read trems of lammpsdata

```python
import readlammpsdata as rld
lmp ="PVP.lmp"
trems = rld.read_terms(lmp)
print(trems)
"""output
['Masses', 'Pair Coeffs', 'Bond Coeffs', 'Angle Coeffs', 'Dihedral Coeffs', 'Improper Coeffs', 'Atoms # full', 'Bonds', 'Angles', 'Dihedrals', 'Impropers']
"""
```

### Read data

- Read "Atoms"

  ```python
  Atoms = rld.read_data(lmp,"Atoms")
  # or Atoms = rld.read_data(lmp,"Atoms # full")
  print(Atoms)
  """output
  >>> Read data Atoms successfully !
  
       1      1      1 -0.35160000    1.000  1.00000  0.00000
       2      1      2 0.13720000   -0.337  1.00000  0.00000
       3      1      3 -0.79220000   -1.134  1.00000  1.11526
  	...
      13      1     13 0.10870000    0.222  0.44931  2.64132
      14      1     14 0.11370000   -1.868  0.86334  4.30672
      15      1     15 0.11370000   -1.804 -0.58670  3.28942
      16      1     16 0.14040000   -3.408  1.94658  2.77089
      17      1     17 0.14040000   -3.873  0.22675  2.53818
  """
  ```

- read "others trems" data

  ```python
  Masses = read_data(lmp, "Masses")
  BondCoeffs = read_data(lmp, "Bond Coeffs")
  AngleCoeffs = read_data(lmp, "Angle Coeffs")
  DihedralCoeffs = read_data(lmp, "Dihedral Coeffs")
  ...
  
  ```
  

### Read Box size

```python
xyz = rld.read_box(lmp)
lx = xyz["xhi"]-xyz["xlo"]
ly = xyz["yhi"]-xyz["ylo"]
lz = xyz["zhi"]-xyz["zlo"]
print(xyz)
print(lx,ly,lz)
"""
{'xlo': -3.87301, 'xhi': 46.12699, 'ylo': -0.5867, 'yhi': 49.4133, 'zlo': -0.95115, 'zhi': 49.04885}
50.0 50.0 50.0
"""

lx = rld.read_len(lmp,"x")
ly = rld.read_len(lmp,"y")
lz = rld.read_len(lmp,"z")
print(lx,ly,lz)
"""
>>> Read data Header successfully !
>>> Read size of x direction successfully !
>>> Read data Header successfully !
>>> Read size of y direction successfully !
>>> Read data Header successfully !
>>> Read size of z direction successfully !
50.0 50.0 50.0
"""

```

### Read atomic infos

- Number of atoms:

  ```python
  Natoms = rld.read_atom_info(lmp,"atoms")
  print("Number of atoms is %s" %Natoms)
  
  """
  >>> Read data Header successfully !
  >>> Read data Header successfully !
  Number of atoms is 17
  """
  ```

- Number of bonds:

  ```python
  Nbonds = rld.read_atom_info(lmp,"bonds")
  print("Number of bonds is %s" %Nbonds)
  """
  >>> Read data Header successfully !
  >>> Read data Header successfully !
  Number of bonds is 17
  """
  ```

- Number of angles, dihedrals, impropers, same as above



### Read charges

```python
charges = rld.read_charges(lmp)
print("Charges of atoms are %s" %charges)
print(round(sum(charges),6))
"""
>>> Read charges successfully !
Charges of atoms are [-0.3516  0.1372 -0.7922  0.1074 -0.2058 -0.2204  0.5562 -0.4121  0.1379  0.1379  0.1799  0.1087  0.1087  0.1137  0.1137  0.1404  0.1404]
-0.0
"""
```

### Read volume

```python
vol = rld.read_vol(lmp)
print(vol)
"""
>>> Read data Header successfully !
>>> Read size of x direction successfully !
>>> Read data Header successfully !
>>> Read size of y direction successfully !
>>> Read data Header successfully !
>>> Read size of z direction successfully !
>>> Read volume of system successfully !
125.0
"""
```



### Sort lmp

```python
rld.sort_lmp("PVP.lmp","PVP_sort.lmp")
```



### lammpsdata to xyz

```python
rld.lmp2xyz("PVP.lmp","PVP.xyz")
"""
---------------------  Program Start  ---------------------
>>> Read data Masses successfully !
>>> Convert the id masses to element list successfully !
>>> Read the id masses and element dicts successfully !
>>> Read data Atoms successfully !
>>> Convert lammps data (lmp) file to xyz file successfully !
-------------------- Run time: 0.04 s  --------------------
"""
```

### lammpsdata to lammpstrj

```python
rld.lmp2lammpstrj(lmp,"PVP.lammpstrj")
"""
---------------------  Program Start  ---------------------
>>> Read data Masses successfully !
>>> Convert the id masses to element list successfully !
>>> Read the id masses and element dicts successfully !
>>> Read data Atoms successfully !
>>> Read data Header successfully !
>>> Convert lammps data (lmp) file to lammpstrj file successfully !
-------------------- Run time: 0.0 s  --------------------
"""
```



### others

- to be continued
