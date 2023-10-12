# A script to read lammps data
import numpy as np
from collections import Counter
import periodictable as pt

def __version__():
    """
    read the version of readlammpsdata
    """
    version = "1.0.6"
    return version

def extract_substring(string, char1, char2):
    """
    extract substring
    """
    if char1 == "":
        start_index = 0
    else:
        start_index = string.index(char1) + len(char1)

    if char2 == "":
        end_index = None
    else:
        end_index = string.index(char2)
    return string[start_index:end_index]

def read_data_sub(wholestr,sub_char,char1,char2):
    """
    extract substring based on subchar
    """
    try:
        sub = extract_substring(wholestr, char1,char2)
        sub.strip()
        print("Read data "+sub_char+" successfully !")
        return sub
    except:
        return "Warning: There is no "+sub_char+" term in your data!"

def read_terms(lmp):
    """
    Read the composition of the lammps data
    """
    terms = ["Masses",
             "Pair Coeffs","Bond Coeffs","Angle Coeffs","Dihedral Coeffs","Improper Coeffs",
             "Atoms","Velocities","Bonds","Angles","Dihedrals","Impropers"]
    new_terms = []
    with open(lmp, "r") as f:
        for line in f:
            line = line.strip()
            if line != "":
                for i in range(len(terms)):
                    if terms[i] in line:
                        new_terms.append(line)
    # print("Your lmp is composed of ",new_terms)
    return new_terms

def search_chars(lmp, data_sub_str):
    """
    Matches the keyword to be read
    lmp: lammps data file
    data_sub_str: data keyword to be read, for exammples:
    'Masses', 'Pair Coeffs', 'Bond Coeffs', 'Angle Coeffs', 'Dihedral Coeffs', 'Improper Coeffs', 'Bonds', 'Angles', 'Dihedrals', 'Impropers'
    """
    char_list = read_terms(lmp)
    char_list.insert(0,"")
    char_list.append("")
    # print("Your lmp is composed of ",char_list)
    data_sub_list = read_terms(lmp)
    data_sub_list.insert(0,"Header")
    # print("Your lmp is composed of ",data_sub_list)
    # char_list = ["","Masses",
    #                 "Pair Coeffs","Bond Coeffs","Angle Coeffs","Dihedral Coeffs","Improper Coeffs",
    #                 "Atoms","Bonds","Angles","Dihedrals","Impropers",""]
    # data_sub_list = ["Header", "Masses",
    #                 "Pair Coeffs","Bond Coeffs","Angle Coeffs","Dihedral Coeffs","Improper Coeffs",
    #                 "Atoms","Bonds","Angles","Dihedrals","Impropers"]                


    # if data_sub_str in ["Atoms # full", "Atoms #"]:
    #     char_list[7] = "Atoms # full"
    #     data_sub_list[7] = "Atoms # full"
    # else:
    #     pass

    for i in range(len(data_sub_list)):
        if data_sub_str in data_sub_list[i]:
            char1, char2 = char_list[i],char_list[i+1]
        else:
            pass
    try:
        return char1, char2
    except:
        char1, char2 = "",""
        print("Warning: '"+data_sub_str+"' not found in your data!")     
    return char1, char2

def read_data(lmp, data_sub_str):
    """
    read data of lammps data:
    lmp: lammps data file
    data_sub_str: data keyword to be read, for exammples:
    'Masses', 'Pair Coeffs', 'Bond Coeffs', 'Angle Coeffs', 'Dihedral Coeffs', 'Improper Coeffs', 'Bonds', 'Angles', 'Dihedrals', 'Impropers'
    """
    char1,char2 = search_chars(lmp,data_sub_str)       
    if char1 == "" and char2 == "":
        pass
    else:
        with open(lmp,'r') as sc:
            wholestr=sc.read()
            # print(wholestr)
            sub = read_data_sub(wholestr,data_sub_str,char1,char2)

        return sub

def str2array(strings):
    """
    convert string to a array
    """
    strings = list(strings.strip().split("\n"))
    strings = list(map(lambda ll:ll.split(), strings))
    array = np.array(strings)
    return array

def read_box(lmp):
    """
    read box size of lammps data:
    lmp: lammps data file
    return a dictionary including box info, for example:
            {'xlo': 0.0, 'xhi': 60.0, 
             'ylo': 0.0, 'yhi': 60.0, 
             'zlo': 0.0, 'zhi': 60.0}
    """
    Header = read_data(lmp, data_sub_str = "Header")
    try:
        x = extract_substring(Header,"improper types","xlo xhi").strip().split()
    except:
        try:
            x = extract_substring(Header,"dihedral types","xlo xhi").strip().split()
        except:
            try:
                x = extract_substring(Header,"angle types","xlo xhi").strip().split()
            except:
                try:
                    x = extract_substring(Header,"bond types","xlo xhi").strip().split()
                except:
                    try:
                        x = extract_substring(Header,"bond types","xlo xhi").strip().split()
                    except:
                        print("Error: No find 'xlo xhi'!")
    
    y = extract_substring(Header,"xlo xhi","ylo yhi").strip().split()
    z = extract_substring(Header,"ylo yhi","zlo zhi").strip().split()
    x = list(map(lambda f:float(f), x))
    y = list(map(lambda f:float(f), y))
    z = list(map(lambda f:float(f), z))
    xyz = {
        "xlo":x[0],
        "xhi":x[1],
        "ylo":y[0],
        "yhi":y[1],
        "zlo":z[0],
        "zhi":z[1],
    }
    return xyz



def read_atom_info(lmp,info="atoms"):
    """
    read numebr of atoms from lammps data:
    lmp: lammps data file
    info: Keywords to be read, including: 
        "atoms","bonds","angles","dihedrals","impropers",
        "atom types","bond types","angle types","dihedral types","improper types"
    """
    info_list = ["\n","atoms","bonds","angles","dihedrals","impropers",
    "atom types","bond types","angle types","dihedral types","improper types","\n"]

    for i in range(len(info_list)):
        if info == info_list[i]:
            info0 = info_list[i-1]
            info1 = info_list[i]
    Header = read_data(lmp, data_sub_str = "Header")
    Natoms = extract_substring(Header,info0,info1).strip().split()
    Natoms = list(map(lambda f:int(f), Natoms))[-1]
    return Natoms

def read_charges(lmp):
    """
    read charges info from lammps data:
    lmp: lammps data file
    return charges of all atoms
    """
    # try:
    Atoms = read_data(lmp, data_sub_str = "Atoms")
    Atoms = str2array(Atoms)
    # except:
    #     Atoms = read_data(lmp, data_sub_str = "Atoms # full")
    #     Atoms = str2array(Atoms)

    charges = np.float64(np.array(Atoms[:,3]))

    # charges = list(map(lambda f:float(f), Atoms[:,3]))

    return charges


def read_vol(lmp):
    """
    read volume of box:
    lmp: lammps data file
    return unit of volume: nm^3
    """
    Lxyz = read_box(lmp)
    Lx = Lxyz["xhi"]-Lxyz["xlo"]
    Ly = Lxyz["yhi"]-Lxyz["ylo"]
    Lz = Lxyz["zhi"]-Lxyz["zlo"]
    vlo = Lx*Ly*Lz*1e-3
    return vlo


def read_xyz(xyzfile,term="all"):
    """
    read xyz info from xyzfile
    term: 
          if term == "elements", return "elements"
          if term == "xyz", return "xyz"
          if term == "all" or other, return "elements, xyz"
    """
    xyz = np.loadtxt(xyzfile,dtype="str",skiprows=2)
    elements = " ".join(xyz[:,0].tolist())
    xyz = np.float64(xyz[:,1:])
    if term == "elements":
        return elements
    if term == "xyz":
        return xyz
    if term == "all":
        return elements, xyz
    else:
        return elements, xyz

def read_pdb(pdbfile,term="all"):
    """
    read pdf from pdbfile
    pdbfile: pdb file
    term: 
          if term == "elements", return "elements"
          if term == "xyz", return "xyz"
          if term == "conect", return "conect"
          if term == "all" or other, return "elements, xyz, conect"

    """
    new_line = []
    conect = []
    with open(pdbfile,"r") as f:
        for index, line in enumerate(f):
            if "ATOM" in line:
                element = line[76:78]
                if element == "":
                    element = line[12:14].strip()
                x = line[31:38].strip()
                y = line[39:46].strip()
                z = line[47:54].strip()
                # print(element,x,y,z)
                new_line.append([element,x,y,z])
            if "CONECT" in line:
                conect.append(line.strip().split()[1:])
        # atom_number = len(new_line)
    new_line = np.array(new_line)
    elements = " ".join(new_line[:,0].tolist())
    xyz = np.float64(new_line[:,1:])
    try:
        # print(conect)
        conect = np.array(conect)
        conect = np.int64(np.array(conect))
    except:
        conect=conect

    if term == "elements":
        return elements
    elif term == "xyz":
        return xyz
    elif term == "conect":
        return conect
    elif term == "all":
        return elements, xyz
    else:
        return elements, xyz, conect


def pdb2xyz(pdbfile,xyzfile):
    """
    convert pdb file to xyz file
    pdbfile: pdb file
    xyzfile: xyz file
    """
    elements, xyz = read_pdb(pdbfile)
    elements = elements.split()
    atom_number = len(elements)
    with open(xyzfile,"w") as f:
        f.write(str(atom_number)+"\n")
        f.write("generted by 'readlammpsdata': https://github.com/eastsheng/readlammpsdata\n")
        for i in range(atom_number):
            f.write(elements[i]+"\t"+str(xyz[i][0])+"\t"+str(xyz[i][1])+"\t"+str(xyz[i][2])+"\n")
    print("pdb2xyz successfully!")


def read_formula(file):
    """
    read molecular formula from xyzfile or pdb file
    file: xyzfile or pdb file
    """
    try:
        elements,xyz = read_xyz(file)
    except:
        elements,xyz = read_pdb(file)

    elements = elements.split()
    element_counts = Counter(elements)
    chemical_formula = ''
    for element, count in element_counts.items():
        chemical_formula += element
        chemical_formula += " "
        if count > 1:
            chemical_formula += str(count)
            chemical_formula += " "
    return chemical_formula


def modify_pos(lmp,pdbxyz):
    """
    modify lammps data position by xyz or pdb file
    lmp: lammps data
    pdbxyz: pdb or xyz file
    """
    Atoms = read_data(lmp,"Atoms")
    Atoms = str2array(Atoms)
    m, n = Atoms.shape
    # print(Atoms)
    try:
        elements, xyz = read_xyz(pdbxyz)
    except:
        elements, xyz = read_pdb(pdbxyz)
    for i in range(m):
        Atoms[i,4] = xyz[i,0]
        Atoms[i,5] = xyz[i,1]
        Atoms[i,6] = xyz[i,2]
    return Atoms

def modify_pore_size(lammpsdata,modify_data,modify_size=0,pdbxyz=None):
    """
    modify the pore size of lammpsdata
    lammpsdata: lammps data file name
    modify_data: rewrite lammps data file name
    modify_size: increase or decrease pore size, unit/nm
    pdbxyz: pdb of xyz file, modify lammpsdata position by pdb or xyz, default None
    """
    # modify header
    Header = read_data(lammpsdata,"Header").split("\n")
    for i in range(len(Header)):
        # print(Header[i])
        if "zlo zhi" in Header[i]:
            Header[i] = Header[i].split()
            Header[i][1] = float(Header[i][1])+modify_size*10
            Header[i][1] = Header[i][1]-float(Header[i][0])
            Header[i][0] = "0.0"
            Header[i][1] = str(Header[i][1])
            Header[i] = "\t".join(Header[i])

    Masses = read_data(lammpsdata,"Masses")
    PairCoeffs = read_data(lammpsdata,"Pair Coeffs")
    BondCoeffs = read_data(lammpsdata,"Bond Coeffs")
    AngleCoeffs = read_data(lammpsdata,"Angle Coeffs")
    DihedralCoeffs = read_data(lammpsdata,"Dihedral Coeffs")
    ImproperCoeffs = read_data(lammpsdata,"Improper Coeffs")

    # modify Atoms
    Lxyz = read_box(lammpsdata)
    Lx = Lxyz["xhi"]-Lxyz["xlo"]
    Ly = Lxyz["yhi"]-Lxyz["ylo"]
    Lz = Lxyz["zhi"]-Lxyz["zlo"]
    Atoms = read_data(lammpsdata,"Atoms")
    Atoms = str2array(Atoms)
    try:
        Atoms = modify_pos(lammpsdata,pdbxyz)
    except:
        pass
    m, n = Atoms.shape
    for i in range(m):
        Atoms[i,6] = float(Atoms[i,6])
        if float(Atoms[i,6]) > (Lz/2.0):
            Atoms[i,6] = float(Atoms[i,6]) + modify_size*10
            Atoms[i,6] = str(Atoms[i,6])
    # modify Bonds
    Bonds = read_data(lammpsdata,"Bonds")
    # print(Bonds)
    # modify Bonds
    Angles = read_data(lammpsdata,"Angles")
    # print(Angles)
    Dihedrals = read_data(lammpsdata,"Dihedrals")
    # print(Dihedrals)
    Impropers = read_data(lammpsdata,"Impropers")
    # print(Impropers)
    with open(modify_data,"w") as f:
        for h in Header:
            f.write(h+"\n")
        if Masses:
            f.write("Masses")
            f.write(Masses)
        if PairCoeffs:
            f.write("Pair Coeffs")
            f.write(PairCoeffs)
        if BondCoeffs:
            f.write("Bond Coeffs")
            f.write(BondCoeffs)
        if AngleCoeffs:
            f.write("Angle Coeffs")
            f.write(AngleCoeffs)
        if DihedralCoeffs:
            f.write("Dihedral Coeffs")
            f.write(DihedralCoeffs)
        if ImproperCoeffs:
            f.write("\nImproper Coeffs")
            f.write(ImproperCoeffs)

        f.write("Atoms\n\n")
        for i in range(m):
            for j in range(n):
                f.write(Atoms[i][j]+"\t")
            f.write("\n")
        if Bonds:
            f.write("\nBonds")
            f.write(Bonds)
        if Angles:      
            f.write("Angles")
            f.write(Angles)

        if Dihedrals:
            f.write("Dihedrals")
            f.write(Dihedrals)          
        if Impropers:
            f.write("Impropers")
            f.write(Impropers)  
    return


def sort_lmp(lmp,rewrite_lmp):
    """
    Sort all the contents of lmp by the first column id
    lmp: lammps data file name that needs to be sorted
    rewrite_lmp: the sorted lammps data file name
    """
    f = open(rewrite_lmp,"w")
    Header = read_data(lmp,"Header").strip()
    terms = read_terms(lmp)
    f.write(Header)
    f.write("\n")
    for term in terms:
        data_term = read_data(lmp,term)
        data_term = str2array(data_term)
        data_term = data_term[np.argsort(data_term[:,0].astype(int))]
        f.write("\n"+term+"\n\n")
        m, n = data_term.shape
        for i in range(m):
            for j in range(n):
                f.write(data_term[i][j]+"\t")
            f.write("\n")
    f.close()
    print("\nCongratulations! the sorted lmp is successfully generated !\n")
    return

def find_match(all_idMass_dict,value, tolerance=0.01):
    for key, mass in all_idMass_dict.items():
        if abs(float(value) - mass) < tolerance:
            return key
    return 'CT'
def massDict(lmp):
    Masses = read_data(lmp,"Masses").strip().split("\n")
    # print(Masses)
    mass_id, mass, element= [],[],[]
    for m in Masses:
        m = m.split()
        mass_id.append(m[0])
        mass.append(m[1])
        try:
            element.append(m[3])
        except:
            pass
    idMass_dict = dict(zip(mass_id,mass))
    idElem_dict = dict(zip(mass_id,element))

    return idMass_dict, idElem_dict

def mass2element(lmp):
    allelements = pt.elements
    all_idMass_dict = {}
    for element in allelements:
        if element.symbol not in ["n"]:
            all_idMass_dict[element.symbol] = element.mass
    idMass_dict, idElem_dict = massDict(lmp)
    elements_list = []
    for key, value in idMass_dict.items():
        ele = find_match(all_idMass_dict,value)
        elements_list.append(ele)
    # print(len(elements_list))
    # elements_array = np.array(elements_list).reshape((-1,1))
    # print(elements_array)
    elements_list = " ".join(elements_list)
    return elements_list

def lmp2xyz(lmp,xyzfile,elements=None):
    """
    convert lammps data (lmp) file to xyz file
    lmp: lammps data file
    xyzfile: xyz file
    elements: A list of elements by atomic type in order, there are three methods:
            elements = None: Identified by relative atomic mass
            elements = [A list of elements]: you can specify it manually
            elements = other, such as 1, 2, 3, or lmp... : read from the 'Masses' comment of the lmp file
    """
    if elements == None:
        element = mass2element(lmp)
    elif isinstance(elements,list):
        element = elements
    else:
        pass
    idMass_dict, idElem_dict = massDict(lmp)
    Atoms = read_data(lmp,"Atoms").strip()
    Atoms = str2array(Atoms)
    type_id = Atoms[:,2]
    pos = Atoms[:,4:7]
    elements_list = []
    numOfAtoms = len(type_id)
    for i in range(numOfAtoms):
        elements_list.append(idElem_dict[type_id[i]])

    elements_array = np.array(elements_list).reshape((-1,1))

    xyz = np.hstack((elements_array,pos))

    with open(xyzfile,"w") as f:
        f.write(str(numOfAtoms)+"\n")
        if elements == None:
            f.write("Generated by lmp2xyz in 'readlammpsdata' package, Identified by relative atomic mass\n")
        elif isinstance(elements,list):
            f.write("Generated by lmp2xyz in 'readlammpsdata' package, [A list of elements]: you specify it manually\n")
        else:
            f.write("Generated by lmp2xyz in 'readlammpsdata' package, read from the 'Masses' comment of the lmp file\n")
        for i in range(numOfAtoms):
            for j in range(4):
                f.write(xyz[i,j]+"\t")
            f.write("\n")
    print("\nGenerate xyz file successfully !\n")
    return


def replace_term_info(term,a_dict):
    new_term = []
    for i in range(len(term)):
        for key, value in a_dict.items():
            if key in term[i]:
                term[i] = term[i].strip().split(' ', 2)
                term[i][2] = str(value) + ' # ' + key
                temp = '  '.join(term[i])
                new_term.append(temp)
                # print(temp)
    # term = [x for x in term if x not in [""]]
    return new_term

def select_term_info(XCoeffs,term,):
    m, n = term.shape
    new_terms = []
    for i in range(m):
        for j in range(len(XCoeffs)):
            if int(term[i][1]) == int(XCoeffs[j].split()[0]):
                new_terms.append(term[i].tolist())
                # print(term[i])
    return new_terms

def msi2clayff(lmp, clayff_lmp):
    """
    # J. Phys. Chem. B, Vol. 108, No. 4, 2004 1259
    convert a lmp obtained from msi2lmp (from Materials Studio) to clayff force field
    lmp: original lmp obtained from msi2lmp
    clayff_lmp: rewrite lammps data
    """
    Header = read_data(lmp,"Header")
    # print(Header)
    Masses = read_data(lmp,"Masses").split("\n")
    mass_dict = {"sz":"28.085500","oz":"15.999400","oh":"15.999400","ho":"1.007970"}
    Masses = replace_term_info(Masses,mass_dict)
    
    PairCoeffs = read_data(lmp,"Pair Coeffs").split("\n")
    pair_dict = {"sz":"0.00000184050       3.3020000000",
                 "oz":"0.15540000000       3.1655700000",
                 "oh":"0.15540000000       3.1655700000",
                 "ho":"0.00000000000       0.0000000000"}
    PairCoeffs = replace_term_info(PairCoeffs,pair_dict)

    BondCoeffs = read_data(lmp,"Bond Coeffs").split("\n")
    bond_dict = {"oh-ho":"554.1349     1.0000"}
    BondCoeffs = replace_term_info(BondCoeffs,bond_dict)
    bond_type_number = len(BondCoeffs)

    AngleCoeffs = read_data(lmp,"Angle Coeffs").split("\n")
    angle_dict = {"sz-oh-ho":"30.0     109.47"}
    AngleCoeffs = replace_term_info(AngleCoeffs,angle_dict)
    angle_type_number = len(AngleCoeffs)

    Atoms = read_data(lmp,"Atoms")
    # print(Atoms)

    Bonds = read_data(lmp,"Bonds")
    Bonds = str2array(Bonds)
    new_bonds = select_term_info(BondCoeffs,Bonds)
    bond_number = len(new_bonds)
    
    Angles = read_data(lmp,"Angles")
    Angles = str2array(Angles)
    new_angles = select_term_info(AngleCoeffs,Angles)
    angle_number = len(new_angles)

    with open(clayff_lmp,"w") as f:
        Header = Header.split("\n")
        for i in range(len(Header)):
            if "bonds" in Header[i]:
                Header[i] = "     "+str(bond_number)+" bonds"
                print(Header[i])
            elif "angles" in Header[i]:
                Header[i] = "     "+str(angle_number)+" angles"
                print(Header[i])
            elif "dihedrals" in Header[i]:
                Header[i] = "     0 dihedrals"
            elif "impropers" in Header[i]:
                Header[i] = "     0 impropers"
                print(Header[i])
            elif "bond types" in Header[i]:
                Header[i] = "   "+str(bond_type_number)+" bond types"
                print(Header[i])
            elif "angle types" in Header[i]:
                Header[i] = "   "+str(angle_type_number)+" angle types"
                print(Header[i])
            elif "dihedral types" in Header[i]:
                Header[i] = "   0 dihedral types"
                print(Header[i])

        for h in Header:
            f.write(h+"\n")

        f.write("Masses\n\n")
        for m in Masses:
            f.write("\t"+m+"\n")

        f.write("\nPair Coeffs\n\n")
        for p in PairCoeffs:
            f.write("\t"+p+"\n")

        f.write("\nBond Coeffs\n\n")
        for b in BondCoeffs:
            if bond_type_number == 1:
                b = b.strip().split()
                b[0] = "1"
                b = "\t".join(b)
            f.write("\t"+b+"\n")

        f.write("\nAngle Coeffs\n\n")
        for a in AngleCoeffs:
            if angle_type_number == 1:
                a = a.strip().split()
                a[0] = "1"
                a = "\t".join(a)
            f.write("\t"+a+"\n")
            
        f.write("\nAtoms")
        f.write(Atoms)

        f.write("Bonds\n\n")
        for i in range(bond_number):
            for j in range(4):
                new_bonds[i][0] = str(i+1)
                if bond_type_number == 1:
                    new_bonds[i][1] = str(bond_type_number)

                f.write(new_bonds[i][j]+"\t")
            f.write("\n")

        f.write("\nAngles\n\n")
        for i in range(angle_number):
            for j in range(5):
                if angle_type_number == 1:
                    new_angles[i][1] = str(angle_type_number)
                new_angles[i][0] = str(i+1)
                f.write(new_angles[i][j]+"\t")
            f.write("\n")

    return
if __name__ == '__main__':

    print(__version__())
    # msi2clayff("sio2_1nm.data","sio2_1nm_clayff.data")

    