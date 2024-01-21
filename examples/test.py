import readlammpsdata as rld
import numpy as np

lmp = "PVP.lmp"

# Atoms = rld.read_data("PVP.lmp","Atoms")
# print(Atoms)
# rld.sort_lmp("PVP.lmp","PVP_sort.lmp")
print(help(rld))

# lx = rld.read_len(lmp,"x")
# ly = rld.read_len(lmp,"y")
# lz = rld.read_len(lmp,"z")
# print(lx,ly,lz)

rld.lmp2lammpstrj(lmp,"PVP.lammpstrj")