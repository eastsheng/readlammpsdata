# correct charges from ligpargen
import numpy as np
import readlammpsdata as rld


if __name__ == '__main__':
    path = "./"
    lmp = path+"UNK_0735D7.lmp"

    data_sub_list = ["Header", "Masses",
                    "Pair Coeffs","Bond Coeffs","Angle Coeffs","Dihedral Coeffs","Improper Coeffs",
                    "Atoms # full","Bonds","Angles","Dihedrals","Impropers"] 

    # 1. read box size
    xyz = rld.read_box(lmp)
    Lx = xyz["xhi"]-xyz["xlo"]
    print(xyz)
    print(Lx)
    # 2. read atomic number 
    Natoms = rld.read_Natoms(lmp)
    print("Number of atoms is %s" %Natoms)
    # 3. read charges 
    charges = rld.read_charges(lmp)
    print("Charges of atoms are %s" %charges)
    print(round(sum(charges),6))
    x = rld.read_data(lmp,data_sub_str = "Masses")
    print(x)


    