### str2array

#### Parameters

- **string**:  The input array string.

#### Returns

- **array**: A  NumPy array.

#### Examples

```python
import readlammpsdata as rld
Atoms = rld.read_data("UNK_0735D7.lmp","Atoms")
print(Atoms)
Atoms = rld.str2array(Atoms)
print(Atoms)

"""
>>> Read data Atoms successfully !


     1      1      1 -0.35160000    1.000  1.00000  0.00000
     2      1      2 0.13720000   -0.337  1.00000  0.00000
     3      1      3 -0.79220000   -1.134  1.00000  1.11526
	...
    16      1     16 0.14040000   -3.408  1.94658  2.77089
    17      1     17 0.14040000   -3.873  0.22675  2.53818
    


[['1' '1' '1' '-0.35160000' '1.000' '1.00000' '0.00000']
 ['2' '1' '2' '0.13720000' '-0.337' '1.00000' '0.00000']
 ['3' '1' '3' '-0.79220000' '-1.134' '1.00000' '1.11526']
	...
 ['16' '1' '16' '0.14040000' '-3.408' '1.94658' '2.77089']
 ['17' '1' '17' '0.14040000' '-3.873' '0.22675' '2.53818']]    
"""

```

#### Notes

- The input string is in the form of a matrix