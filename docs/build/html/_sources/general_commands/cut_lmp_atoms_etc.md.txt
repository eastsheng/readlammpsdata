### cut_lmp_atoms_etc

> cut lammps data, including bonds and angles and so on.
>
> This function is an improvement on `cut_lmp_atoms`.
>
> `cut_lmp_atoms ` can only handle lmp with no bond angles.

#### Parameters

- **lmp:** original lammps data
- **relmp:** rewrite lammps data
- **cut_block:** {  "dx":[0,0],
                          "dy":[0,0],
                          "dz":[0,0]
                          }, a dictionary, unit/angstrom

#### Returns

- *None*

#### Examples

```python
import readlammpsdata as rld
rld.cut_lmp_atoms_etc(
    lmp,relmp,cut_block={
	        "dx":[-1000,1000],
 		"dy":[-1000,1000],
 		"dz":[-15.9,13.5]})
```

#### Notes

- dx, dy, dz represent the interval of the block to be cut