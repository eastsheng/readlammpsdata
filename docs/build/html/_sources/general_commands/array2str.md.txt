### array2str

#### Parameters

- **array**:  The input NumPy array.

#### Returns

- **string**: A string representing the NumPy array.

#### Examples

```python
import readlammpsdata as rld
import numpy as np
arr = np.array([[1, 2, 3, 4],[4, 5, 6, 7],[8, 9, 10, 11]])
string = rld.array2str(arr)
print(type(arr))
with open("string.txt","w") as f:
	f.write(string)
print(type(string))

"""
[1 2 3 4]
[4 5 6 7]
[ 8  9 10 11]
>>> Convert a array to a string for writing successfully !
<class 'numpy.ndarray'>
<class 'str'>
"""

# string.txt
"""


1  2  3  4
4  5  6  7
8  9  10  11


"""
```

#### Notes

- This function is to facilitate writing files.