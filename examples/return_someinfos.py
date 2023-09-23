# correct charges from ligpargen
import numpy as np
import readlammpsdata as rld


if __name__ == '__main__':
    path = "./"
    lmp = path+"UNK_0735D7.lmp"
    print(rld.__version__())
    # trems = rld.read_terms(lmp)
    # print(trems)
    # # 0. read data
    # Masses = rld.read_data(lmp,"Pair Coeffs")
    # print(Masses)
    # # 1. read box size
    # xyz = rld.read_box(lmp)
    # Lx = xyz["xhi"]-xyz["xlo"]
    # print(xyz)
    # print(Lx)
    # # 2.1 read atomic number 
    # Natoms = rld.read_atom_info(lmp,"atoms")
    # print("Number of atoms is %s" %Natoms)
    # # 2.2 read bonds number 
    # Nbonds = rld.read_atom_info(lmp,"bonds")
    # print("Number of bonds is %s" %Nbonds)
    # # 2.3 read angles number 
    # Nangles = rld.read_atom_info(lmp,"angles")
    # print("Number of angles is %s" %Nangles)
    # # 2.4 read dihedrals number 
    # Ndihedrals = rld.read_atom_info(lmp,"dihedrals")
    # print("Number of dihedrals is %s" %Ndihedrals)
    # # 2.5 read impropers number 
    # Nimpropers = rld.read_atom_info(lmp,"impropers")
    # print("Number of impropers is %s" %Nimpropers)
    # # 2.6 read impropers number 
    # Nimpropers = rld.read_atom_info(lmp,"angle types")
    # print("Number of improper types is %s" %Nimpropers)

    # # 3. read charges 
    # charges = rld.read_charges(lmp)
    # print("Charges of atoms are %s" %charges)
    # print(round(sum(charges),6))
    # x = rld.read_data(lmp,data_sub_str = "Masses")
    # print(x)

    # # 4. read vol
    # vol = rld.read_vol(lmp)
    # print(help(rld.read_data))
    
    # # 5. read xyz from xyz file    # xyzfile = "./Lecithin.xyz"
    # elements, xyz = rld.read_xyz(xyzfile)
    # print(elements)
    # # 6. read pdb from pdb file
    pdbfile = "./Lecithin.pdb"
    elements = rld.read_pdb(pdbfile,"all")
    print(elements[0])
    print(help(rld.read_pdb))

