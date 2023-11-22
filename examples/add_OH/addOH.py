import readlammpsdata as rld
import numpy as np


if __name__ == '__main__':
	lmp = "system.data"
	cutlmp1 = "system_cut1.data"
	cutlmp2 = "system_cut2.data"
	cutlmp3 = "system_cut3.data"
	# # cut groove
	# cut_block1 = {
	# "dx": [-100,100],
	# "dy": [10.5,42.2448],
	# "dz": [10.0,100],
	# }
	# rld.cut_lmp_atoms(lmp,cutlmp1,cut_block1)
	# # cleave pillar
	# cut_block2 = {
	# "dx": [-100,100],
	# "dy": [-100,100],
	# "dz": [25.1870,100],
	# }
	# rld.cut_lmp_atoms(cutlmp1,cutlmp2,cut_block2)

	# # delete Anomalous atom
	# cut_block3 = {
	# "dx": [-100,100],
	# "dy": [42.8860,42.889],
	# "dz": [24.1520,24.1529],
	# }
	# rld.cut_lmp_atoms(cutlmp2,cutlmp3,cut_block3)

	addHlmp1 = "system_addH1.data"
	addHlmp2 = "system_addH2.data"
	addHlmp3 = "system_addH3.data"
	addHlmp4 = "system_addH4.data"
	addHlmp5 = "system_addH5.data"

	# # 1. inner groove
	# H_block1 = {
	# "dx": [-100,100],
	# "dy": [11.7334,42.3448],
	# "dz": [8.90678-0.1,9.3925+0.1],
	# }
	# rld.addH(cutlmp3,addHlmp1,H_block1)
	# charges = rld.read_charges(addHlmp1)

	# # 2. top pillar
	# H_block2 = {
	# "dx": [-100,100],
	# "dy": [-100,100],
	# "dz": [24.1526-0.1,24.6384+0.1],
	# }
	# rld.addH(addHlmp1,addHlmp2,H_block2)
	# charges = rld.read_charges(addHlmp2)

	# # 2.1 side pillar
	# H_block3 = {
	# "dx": [-100,100],
	# "dy": [42.3448-0.1,42.8868+0.1],
	# "dz": [11.3960,100],
	# }
	# rld.addH(addHlmp2,addHlmp3,H_block3,ang=180,direction="x")
	# charges = rld.read_charges(addHlmp3)

	# # 2.2 side pillar
	# H_block4 = {
	# "dx": [-100,100],
	# "dy": [9.93277-0.1,10.4748+0.1],
	# "dz": [11.3960,100],
	# }
	# rld.addH(addHlmp3,addHlmp4,H_block4,ang=0,direction="x")
	# charges = rld.read_charges(addHlmp4)

	# 3 bottom
	H_block5 = {
	"dx": [-100,100],
	"dy": [-100,100],
	"dz": [-100,1],
	}
	rld.addH(addHlmp4,addHlmp5,H_block5,ang=-30,direction="x")
	charges = rld.read_charges(addHlmp5)

	print(">>> Total charges = ",round(sum(charges),4))