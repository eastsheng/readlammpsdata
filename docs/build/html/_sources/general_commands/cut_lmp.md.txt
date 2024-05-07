### cut_lmp

> cut lammps data along axis

#### Parameters

- **lmp:** original lammps data
- **relmp:** rewrite lammps data
- **distance: **cut distance, unit/angstrom
- **direction:** direction, default direction = "y"

#### Returns

- *None*

#### Examples

```python
import readlammpsdata as rld
rld.cut_lmp(lmp,relmp,distance, direction='y')
```

#### Notes

- The input string is in the form of a matrix