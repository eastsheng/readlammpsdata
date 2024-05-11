### periodic2interface

> change lmp with periodic boundary to lmp with interface.

#### Parameters

- **lmp**: lammps data with bonds and angles across periodic boundary 
- **relmp**: lammps data with interface
- **direction**: normal direction of interface, default z
- **vacuum**: add a vacuum, unit/Angstrom

#### Returns

- *None*

#### Examples

```python
import readlammpsdata as rld

if __name__ == '__main__':
	
	lmp = "1_npt_system.data"
	relmp = "1_npt_system_z.data"
	rld.periodic2interface(lmp,relmp,direction="z",vacuum=50)
	print(help(rld.periodic2interface))
```

| wrap                                                         | unwrap                                                       |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| ![image-20240511141949022](https://gitee.com/eastsheng/VnoteFigures/raw/master/worknotes/2024/202405111419191.png) | ![image-20240511142023313](https://gitee.com/eastsheng/VnoteFigures/raw/master/worknotes/2024/202405111420354.png) |



#### Notes

- None