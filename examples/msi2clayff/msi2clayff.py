# rewrite the lammps data to fit the clayff from the msi2lmp.exe 
# e.g. this example, rewriting the hydroxyl SiO2 data
# J. Phys. Chem. B, Vol. 108, No. 4, 2004 1259

import readlammpsdata as rld

if __name__ == '__main__':
	# inital lammpsdata obtained from msi2lmp.exe tool
	msi_data = "sio2_1nm.data"
	clayff_data = "sio2_1nm_clayff.data"

	rld.msi2clayff(msi_data,clayff_data)