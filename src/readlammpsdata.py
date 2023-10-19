# A script to read lammps data
import numpy as np
from collections import Counter
import periodictable as pt

def __version__():
    """
    read the version of readlammpsdata
    """
    version = "1.0.7"
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
        print(">>> Read data "+sub_char+" successfully !")
        return sub
    except:
        return "??? Warning: There is no "+sub_char+" term in your data!"

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
        print("??? Warning: '"+data_sub_str+"' not found in your data!")     
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
                        print("??? Error: No find 'xlo xhi'!")
    
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

def read_len(lmp,direction):
    """
    read length of box:
    lmp: lammps data file
    direction: direction, direction = x, or y, or z, then return Lx, or Ly, or Lz 
    """
    Lxyz = read_box(lmp)
    Lx = Lxyz["xhi"]-Lxyz["xlo"]
    Ly = Lxyz["yhi"]-Lxyz["ylo"]
    Lz = Lxyz["zhi"]-Lxyz["zlo"]
    if direction == "x" or direction == "X":
        ll = Lx
    elif direction == "y" or direction == "Y":
        ll = Ly
    elif direction == "z" or direction == "Z":
        ll = Lz

    print(">>> Read size of",direction, "direction successfully !")
    return ll


def read_vol(lmp):
    """
    read volume of box:
    lmp: lammps data file
    return unit of volume: nm^3
    """
    Lx = read_len(lmp,direc="x")
    Ly = read_len(lmp,direc="y")
    Lz = read_len(lmp,direc="z")

    vlo = Lx*Ly*Lz*1e-3

    print(">>> Read volume of system successfully !")
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
    print(">>> pdb2xyz successfully!")


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
    
    print(">>> Read formula from xyzfile or pdb file successfully !")
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

    print(">>> Modified lammps data position by xyz or pdb file successfully !")
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

    print("\n>>> Modified the pore size of lammpsdata successfully !\n")
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
    print("\n>>> Congratulations! the sorted lmp is successfully generated !\n")
    return

def find_match(all_idMass_dict,value, tolerance=0.01):
    for key, mass in all_idMass_dict.items():
        if abs(float(value) - mass) < tolerance:
            return key
    return 'CT'
def read_mass(lmp):
    """
    read mass from lammps, return 2 dict: idMass_dict, idElem_dict
    lmp: lammps data
    """
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
    """
    Convert the masses obtained from lammps data to element symbols
    lmp: lammps data
    """
    allelements = pt.elements
    all_idMass_dict = {}
    for element in allelements:
        if element.symbol not in ["n"]:
            all_idMass_dict[element.symbol] = element.mass
    idMass_dict, idElem_dict = read_mass(lmp)
    elements_list = []
    for key, value in idMass_dict.items():
        ele = find_match(all_idMass_dict,value)
        elements_list.append(ele)
    # print(len(elements_list))
    # elements_array = np.array(elements_list).reshape((-1,1))
    # print(elements_array)
    elements_list = " ".join(elements_list)

    print("\n>>> Convert the masses obtained from lammps data to element symbols successfully !\n")
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
    idMass_dict, idElem_dict = read_mass(lmp)
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
    print("\n>>> Convert lammps data (lmp) file to xyz file successfully !\n")
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
    print("\n>>> Convert a lmp obtained from msi2lmp to clayff force field successfully !\n")
    return



def sort_tip4p_ele(dictionary,index,ele='O'):
    """
    If the value of the first element in the dictionary is not 'O', 
    the key value of the subsequent element is 'O'
    dictionary: element dict, such as {1: 'O', 3: 'H', 2: 'C', 4: 'H'}
    index: 1 or 2
    ele: 'O' or "H"
    """
    modify_key = 1
    if dictionary[index] != ele:
        for key, value in dictionary.items():
            if value == ele and key>index:
                modify_key=key
                dictionary[index], dictionary[key] = dictionary[key], dictionary[index]
                break

    old_keys = list(dictionary)
    new_keys = []
    for k in old_keys:
        if k == index:
            new_keys.append(modify_key)
        elif k == modify_key:
            new_keys.append(index)
        else:
            new_keys.append(k)
    new_dictionary = {}
    for key in old_keys:
        value = dictionary.pop(key)
        new_dictionary.update({new_keys[old_keys.index(key)] : value})

    return new_dictionary

def lmp2tip4p(lmp,tip4p_lmp,ua=False):
    """
    lmp to tip4p format, O-H-H
    lmp: lmp from Materials studio using "msi2lmp.exe"
    tip4p_lmp: tip4p lammps data
    """
    f = open(tip4p_lmp,"w")
    # 0. ------> read Header
    Header = read_data(lmp,"Header")
    if ua == True:
        Bonds = str2array(read_data(lmp,"Bonds"))
        ua_nbond = np.count_nonzero(Bonds[:,1]=="1")
        Angles = str2array(read_data(lmp,"Angles"))
        ua_nangle = np.count_nonzero(Angles[:,1]=="1")
        Header = Header.split("\n")
        for i in range(len(Header)):
            if "bonds" in Header[i]:
                Header[i] = Header[i].strip().split()
                Header[i][0] = str(ua_nbond)
                Header[i] = " ".join(Header[i])
                Header[i] = "\t"+Header[i]
            if "angles" in Header[i]:
                Header[i] = Header[i].strip().split()
                Header[i][0] = str(ua_nangle)
                Header[i] = " ".join(Header[i])
                Header[i] = "\t"+Header[i]
            if "bond types" in Header[i]:
                Header[i] = Header[i].strip().split()
                Header[i][0] = "1"
                Header[i] = " ".join(Header[i])
                Header[i] = "\t"+Header[i]
            if "angle types" in Header[i]:
                Header[i] = Header[i].strip().split()
                Header[i][0] = "1"
                Header[i] = " ".join(Header[i])
                Header[i] = "\t"+Header[i]
            f.write(Header[i]+"\n")
    else:
        f.write(Header)
    # 1. ------> modify masses
    elements = mass2element(lmp).split()
    elements = {i: value for i, value in enumerate(elements,1)}
    old_keys = list(elements)
    elements = sort_tip4p_ele(elements,index=1,ele='O')
    elements = sort_tip4p_ele(elements,index=2,ele='H')
    # print(elements)
    f.write("Masses\n\n")
    if ua == True:
        count_mass = 0
        for key, value in elements.items():
            mass = pt.elements.symbol(value).mass
            count_mass += 1
            if count_mass == 3:
                mass = mass + 4*pt.elements.symbol("H").mass
                f.write("\t"+str(count_mass)+"\t"+str(mass)+"\t# "+value+"\n")
            elif count_mass == 4:
                pass
            else:
                f.write("\t"+str(count_mass)+"\t"+str(mass)+"\t# "+value+"\n")
    else:
        count_mass = 0
        for key, value in elements.items():
            mass = pt.elements.symbol(value).mass
            count_mass += 1
            f.write("\t"+str(count_mass)+"\t"+str(mass)+"\t# "+value+"\n")

    # 2. ------> modify Pair Coeffs
    new_keys = list(elements)
    PairCoeffs = read_data(lmp,"Pair Coeffs").strip("\n").split("\n")
    
    if ua == True:
        for i in range(len(PairCoeffs)):
            if PairCoeffs[i] != "":
                PairCoeffs[i] = PairCoeffs[i].strip().split()
                PairCoeffs[i][0] = str(new_keys[i])
                if PairCoeffs[i][0] == "3":
                    PairCoeffs[i][1] = "0.294"
                    PairCoeffs[i][2] = "3.73"
    else:
        for i in range(len(PairCoeffs)):
            if PairCoeffs[i] != "":
                PairCoeffs[i] = PairCoeffs[i].strip().split()
                PairCoeffs[i][0] = str(new_keys[i])
    PairCoeffs.sort(key=lambda x: int(x[0]))
    if ua == True:
        PairCoeffs = PairCoeffs[:-1]
    f.write("\nPair Coeffs\n\n")
    for k in PairCoeffs:
        d = "\t".join(k)
        f.write("\t"+d+"\n")

    # 3. ------> read Bond Coeffs
    BondCoeffs = read_data(lmp,"Bond Coeffs").strip("\n").split("\n")
    f.write("\nBond Coeffs\n\n")
    if ua == True:
        BondCoeffs = BondCoeffs[:-1]
    for b in BondCoeffs:
        f.write(b+"\n")

    # 4. ------> read Angle Coeffs
    AngleCoeffs = read_data(lmp,"Angle Coeffs").strip("\n").split("\n")
    if ua == True:
        AngleCoeffs = AngleCoeffs[:-1]
    f.write("\nAngle Coeffs\n\n")
    for b in AngleCoeffs:
        f.write(b+"\n")

    # 5. ------> read Bonds
    Bonds = str2array(read_data(lmp,"Bonds"))
    # default the type 1 is the O-H bond
    new_water_order, other_order = [], []
    m,n = Bonds.shape
    for i in range(m):
        if Bonds[i][1] == "1":
            new_water_order.append(Bonds[i][2])
            new_water_order.append(Bonds[i][3])
        else:
            other_order.append(Bonds[i][2])
            other_order.append(Bonds[i][3])
    new_water_order = [x for i, x in enumerate(new_water_order) if x not in new_water_order[:i]]
    other_order = [x for i, x in enumerate(other_order) if x not in other_order[:i]]
    new_atom_order = new_water_order+other_order

    # 6. ------> modify Atoms
    Atoms = str2array(read_data(lmp,"Atoms"))
    # sorted by new_atom_order
    sort_dict = {k: v for v, k in enumerate(new_atom_order)}
    sorted_Atoms = Atoms[np.argsort([sort_dict.get(x) for x in Atoms[:, 0]])]
    # modify atom type by old_keys and new_keys
    key_dict = {k: v for k, v in zip(old_keys, new_keys)}
    for i in range(len(sorted_Atoms)):
        sorted_Atoms[i][2] = key_dict[int(sorted_Atoms[i][2])]
        sorted_Atoms[i][0] = str(i+1)
    na, nb = sorted_Atoms.shape
    f.write("\nAtoms\n\n")
    if ua == True:
        count_atoms = 0
        for i in range(na):
            if sorted_Atoms[i][2]=="4":
                pass
            else:
                count_atoms += 1
                f.write("\t"+str(count_atoms)+"\t")
                for j in range(1,nb):
                    f.write("\t"+sorted_Atoms[i][j]+"\t")
                f.write("\n")
    else:
        for i in range(na):
            for j in range(nb):
                f.write("\t"+sorted_Atoms[i][j]+"\t")
            f.write("\n")

    # 7. modify Bonds and Angles by the newest sorted_Atoms
    f.write("\nBonds\n\n")
    count_nbond = 0
    for i in range(na):
        if sorted_Atoms[i][2] == "1":
            for j in range(2):
                count_nbond += 1
                f.write("\t"+str(count_nbond)+"\t"+str(1)+"\t"+sorted_Atoms[i][0]+"\t"+str(int(sorted_Atoms[i][0])+j+1)+"\n")
        if ua == True:
            pass
        else:
            if sorted_Atoms[i][2] == "3":
                for k in range(4):
                    count_nbond += 1
                    f.write("\t"+str(count_nbond)+"\t"+str(2)+"\t"+sorted_Atoms[i][0]+"\t"+str(int(sorted_Atoms[i][0])+k+1)+"\n")
        
    f.write("\nAngles\n\n")
    count_nangle = 0
    for i in range(na):
        if sorted_Atoms[i][2] == "1":
            count_nangle += 1
            f.write("\t"+str(count_nangle)+"\t"+str(1)+"\t"+str(int(sorted_Atoms[i][0])+1)+"\t"+sorted_Atoms[i][0]+"\t"+str(int(sorted_Atoms[i][0])+2)+"\n")
        if ua == True:
            pass
        else:
            if sorted_Atoms[i][2] == "3":
                for k in range(3):
                    count_nangle += 1
                    f.write("\t"+str(count_nangle)+"\t"+str(2)+"\t"+str(int(sorted_Atoms[i][0])+1)+"\t"+sorted_Atoms[i][0]+"\t"+str(int(sorted_Atoms[i][0])+k+2)+"\n")
                for k in range(2):
                    count_nangle += 1
                    f.write("\t"+str(count_nangle)+"\t"+str(2)+"\t"+str(int(sorted_Atoms[i][0])+2)+"\t"+sorted_Atoms[i][0]+"\t"+str(int(sorted_Atoms[i][0])+k+3)+"\n")
                for k in range(1):
                    count_nangle += 1
                    f.write("\t"+str(count_nangle)+"\t"+str(2)+"\t"+str(int(sorted_Atoms[i][0])+3)+"\t"+sorted_Atoms[i][0]+"\t"+str(int(sorted_Atoms[i][0])+k+4)+"\n")
    f.close()
    if ua == True:
        print("\n>>> Convert TIP4P/CH4 lmp successfully !\n")
    else:
        print("\n>>> Convert TIP4P/CT lmp successfully !\n")

    return



def array2str(array):
    """
    convert a array to string format for writing directly. 
    array: a array
    """
    string = ""
    for row in array:
        string += "  ".join(row)+"\n"
    string = "\n\n"+string+"\n"
    print("\n>>> Convert a array to a string for writing successfully !\n")

    return string


def add_atoms(Atoms, add_atoms):
    """
    add position at the end of Atoms, Bonds, Angles, return a string
    Atoms: original Atoms, string
    add_atoms: new positions, list
    """
    add_atoms = np.array(add_atoms)
    Atoms = str2array(Atoms)
    New_Atoms = np.concatenate((Atoms, add_atoms), axis=0)
    New_Atoms = array2str(New_Atoms)

    return New_Atoms

def modify_header(Header,hterm,number):
    """
    modify the "Header" info, including number of "atoms", "bonds", "angles", "dihedrals", "impropers",
    "atom types", "bond types", "angle types", "dihedral types", "improper types",
    "xlo xhi", "ylo yhi", "zlo zhi".
    Header: Header
    hterm: "atoms", "bonds"
    number: number of "atoms", "bonds"...
    """
    Header = Header.strip().split("\n")
    for i in range(len(Header)):
        if Header[i]!="":
            Header[i] = Header[i].strip()
            if hterm in Header[i]:
                Header[i] = Header[i].split()
                if len(Header[i]) == 2:
                    Header[i][0] = str(number)
                    Header[i] = "  ".join(Header[i])
                elif len(Header[i]) == 3:
                    Header[i][0] = str(number)
                    Header[i] = " ".join(Header[i])
    Header = "\n".join(Header)+"\n\n"
    print("\n>>>  modify the Header "+ hterm +" successfully !\n")

    return Header

def modify_methane_hydrate(lmp, relmp, axis="z",distance=1.1):
    """
    add methane molecules into half cages at the interface for its symmetry in pore, ppp to ppf
    lmp: original lmp
    relmp: rewrite lmp
    axis: direction x y z, default axis="z"
    """
    terms = read_terms(lmp)
    box = read_box(lmp)
    xlo = float(box["xlo"])
    xhi = float(box["xhi"])
    ylo = float(box["ylo"])
    yhi = float(box["yhi"])
    zlo = float(box["zlo"])
    zhi = float(box["zhi"])
    lx = xhi-xlo
    ly = yhi-ylo
    lz = zhi-zlo
    if axis == "x" or axis == "X":
        ll = lx
        index = 4
    if axis == "y" or axis == "Y":
        ll = ly
        index = 5
    if axis == "z" or axis == "Z":
        ll = lz
        index = 6
    Header = read_data(lmp,"Header")
    # 1. modify atoms
    Atoms_string = read_data(lmp,"Atoms")
    Atoms = str2array(Atoms_string)
    m,n = Atoms.shape
    Natoms = m
    add_methanes = []
    add_atom_old_id = []
    add_atom_new_id = []
    for i in range(m):
        if abs(float(Atoms[i][index])-zlo) < distance:
            Natoms = Natoms + 1
            add_atom_old_id.append(Atoms[i][0])
            Atoms[i][0] = str(Natoms)
            add_atom_new_id.append(Atoms[i][0])
            Atoms[i][index] = str(ll-float(Atoms[i][index]))
            add_methanes.append(Atoms[i].tolist())
    # print(add_methanes)
    nO,nH = 0,0
    for i in range(len(add_methanes)):
        if add_methanes[i][2] == "1":
            nO += 1
        elif add_methanes[i][2] == "2":
            nH += 1
    if nH%nO != 0:
        print("??? Your operation is error! Please check and modify your 'distance' arg...")
    Atoms = add_atoms(Atoms_string,add_methanes)

    # 2. modify bonds
    Bonds_string = read_data(lmp,"Bonds")
    Bonds = str2array(Bonds_string)
    p,q = Bonds.shape
    Nbonds = p
    add_bonds = []
    for i in range(p):
        concent = Bonds[i][2:]
        for j in range(len(add_atom_old_id)):
            if add_atom_old_id[j] == concent[0]:
                Bonds[i][2] = add_atom_new_id[j]
            elif add_atom_old_id[j] == concent[1]:
                Bonds[i][3] = add_atom_new_id[j]
                add_bonds.append(Bonds[i].tolist())
    for i in range(len(add_bonds)):
        Nbonds += 1
        add_bonds[i][0] = str(Nbonds)
    # print(add_bonds)
    Bonds = add_atoms(Bonds_string,add_bonds)

    # 3. modify angles
    Angles_string = read_data(lmp,"Angles")
    Angles = str2array(Angles_string)
    s,t = Angles.shape
    NAngles = s
    # print(NAngles)
    add_angles = []
    for i in range(s):
        concent = Angles[i][2:]
        for j in range(len(add_atom_old_id)):
            if add_atom_old_id[j] == concent[0]:
                Angles[i][2] = add_atom_new_id[j]
            elif add_atom_old_id[j] == concent[1]:
                Angles[i][3] = add_atom_new_id[j]
            elif add_atom_old_id[j] == concent[2]:
                Angles[i][4] = add_atom_new_id[j]
                add_angles.append(Angles[i].tolist())
    for i in range(len(add_angles)):
        NAngles += 1
        add_angles[i][0] = str(NAngles)
    Angles = add_atoms(Angles_string,add_angles)

    with open(relmp,"w") as f:
        Header = modify_header(Header,hterm="atoms",number=Natoms)
        Header = modify_header(Header,hterm="bonds",number=Nbonds)
        Header = modify_header(Header,hterm="angles",number=NAngles)
        f.write(Header)
        for term in terms:
            if "Atoms" in term:
                term_info = Atoms
            elif "Bonds" in term:
                term_info = Bonds
            elif "Angles" in term:
                term_info = Angles
            else:
                term_info = read_data(lmp,term)
            f.write(term)
            f.write(term_info)
    print("\n>>>  Add methane molecules into half cages at the interface successfully !\n")

    return

def move_boundary(lmp,relmp,distance,direction="y"):
    """
    move boundary of lammps data
    lmp: original lammps data
    relmp: rewrite lammps data
    distance: distance moved, unit/A
    direction: direction, default direction = "y"
    """
    if direction == "x" or direction == "X":
        lo_label, hi_label = "xlo", "xhi"
        index = 4
    elif direction == "y" or direction == "Y":
        lo_label, hi_label = "ylo", "yhi"
        index = 5
    elif direction == "z" or direction == "Z":
        lo_label, hi_label = "zlo", "zhi"
        index = 6
    else:
        print("??? Error! Not",direction,"direction! Please check your direction arg !")
    terms = read_terms(lmp)
    Header = read_data(lmp,"Header")
    Atoms_info = read_data(lmp,"Atoms")
    Atoms = str2array(Atoms_info)
    ll = read_len(lmp,direction)
    box = read_box(lmp)
    lo = box[lo_label]
    hi = box[hi_label]
    m,n = Atoms.shape
    for i in range(m):
        Atoms[i][index] = float(Atoms[i][index])-distance
        if float(Atoms[i][index]) <= lo:
            Atoms[i][index] = float(Atoms[i][index])+ll
        elif float(Atoms[i][index]) >= hi:
            Atoms[i][index] = float(Atoms[i][index])-ll
        Atoms[i][index] = str(Atoms[i][index])
    Atoms_str = array2str(Atoms)
    f = open(relmp,"w")
    f.write(Header)
    for term in terms:
        term_info = read_data(lmp,term)
        if "Atoms" in term:
            term_info = Atoms_str
        f.write(term)
        f.write(term_info)
    f.close()
    print("\n>>> Moved boundary of lammps data successfully !\n")   
    return


def density(lmp,atom_type,density_type="mass",direction="y",nbin=50):
    """
    calculating density from lammps data, return a array, x = array[:,0], density = array[:,1]
    lmp: lammps data
    atom_type: atomic types, a list, [1,2]
    density_type: density type, default "mass" density, another is "number"
    direction: direction, default direction = "y"
    nbin: bin of number along the "y" direction
    """
    A2CM = 1e-8
    amu2g = 6.02214076208112e23
    convert_unit = amu2g*(A2CM)**3
    lx = read_len(lmp,"x")
    ly = read_len(lmp,"y")
    lz = read_len(lmp,"z")
    if direction=="x" or direction=="X":
        ll = lx
        index = 4
        l_label = "xlo"
    elif direction=="y" or direction=="Y":
        ll = ly
        index = 5
        l_label = "ylo"
    elif direction=="z" or direction=="Z":
        ll = lz
        index = 6
        l_label = "zlo"

    dbin = ll/nbin
    lo = read_box(lmp)[l_label]
    dv = lx*lz*dbin*convert_unit
    Atoms = read_data(lmp,"Atoms")
    Atoms = str2array(Atoms)
    Masses = read_mass(lmp)[0]
    m, n = Atoms.shape
    laxis, rho = [], []
    for i in range(nbin):
        dm = 0
        l0 = lo+i*dbin
        l1 = lo+(i+1)*dbin
        for j in range(m):
            if int(Atoms[j][2]) in atom_type:
                if float(Atoms[j][index]) >= l0 and float(Atoms[j][index]) <= l1:
                    if density_type == "mass":
                        dm += float(Masses[Atoms[j][2]])
                    elif density_type == "number":
                        dm += 1
                    else:
                        dm += 1
        rhoi = dm/dv
        li = (l0+l1)/2.0
        laxis.append(li)
        rho.append(rhoi)
    laxis = np.array(laxis).reshape((-1,1))
    rho = np.array(rho).reshape((-1,1))
    rho_array = np.hstack((laxis,rho))
    print("\n>>> Calculating density from lammps data successfully !\n")
    return rho_array



def cut_lmp(lmp,relmp,distance,direction="y"):
    """
    cut lammps data
    lmp: original lammps data
    relmp: rewrite lammps data
    distance: cut distance, unit/A
    direction: direction, default direction = "y"
    """
    if direction == "x" or direction == "X":
        lo_label, hi_label = "xlo", "xhi"
        index = 4
    elif direction == "y" or direction == "Y":
        lo_label, hi_label = "ylo", "yhi"
        index = 5
    elif direction == "z" or direction == "Z":
        lo_label, hi_label = "zlo", "zhi"
        index = 6
    else:
        print("??? Error! Not",direction,"direction! Please check your direction arg !")
    terms = read_terms(lmp)
    Header = read_data(lmp,"Header")
    Atoms_info = read_data(lmp,"Atoms")
    Atoms = str2array(Atoms_info)
    ll = read_len(lmp,direction)
    box = read_box(lmp)
    lo = box[lo_label]
    hi = box[hi_label]
    m,n = Atoms.shape
    cut_mol = []
    for i in range(m):
        if Atoms[i][2] not in ["3","4","5","6","7"]:
            # Atoms[i][index] = float(Atoms[i][index])-distance
            if float(Atoms[i][index]) >= distance:
                cut_mol.append(Atoms[i][1])
            # elif float(Atoms[i][index]) >= distance:
            #     cut_mol.append(Atoms[i][1])

    Atoms = Atoms.tolist()
    Atoms_save = []
    cut_id = []
    for i in range(m):
        if Atoms[i][1] not in cut_mol:
            Atoms_save.append(Atoms[i])
        else:
            cut_id.append(Atoms[i][0])
    Atoms_save = np.array(Atoms_save)   
    natoms = len(Atoms_save)
    saveid = Atoms_save[:,0].tolist()
    for i in range(natoms):
        Atoms_save[i,0] = str(i+1)
    newsaveid = Atoms_save[:,0].tolist()
    Atoms_str = array2str(Atoms_save)
    
    id_dict = dict(zip(saveid,newsaveid))

    Bonds_info = read_data(lmp,"Bonds")
    Bonds = str2array(Bonds_info)
    p, q = Bonds.shape
    Bonds = Bonds.tolist()
    Bonds_cut = []
    for i in range(p):
        if Bonds[i][2] in cut_id or Bonds[i][2] in cut_id:
            pass
        else:
            Bonds_cut.append(Bonds[i])
    Bonds_cut = np.array(Bonds_cut)   
    nbonds = len(Bonds_cut)
    for i in range(nbonds):
        Bonds_cut[i,0] = str(i+1)
        Bonds_cut[i,2] = id_dict[Bonds_cut[i,2]]
        Bonds_cut[i,3] = id_dict[Bonds_cut[i,3]]
    Bonds_str = array2str(Bonds_cut)
    
    Angles_info = read_data(lmp,"Angles")
    Angles = str2array(Angles_info)
    r, s = Angles.shape
    Angles = Angles.tolist()
    Angles_cut = []
    for i in range(r):
        if Angles[i][2] in cut_id or Angles[i][2] in cut_id:
            pass
        else:
            Angles_cut.append(Angles[i])
    Angles_cut = np.array(Angles_cut)   
    nangles = len(Angles_cut)
    for i in range(nangles):
        Angles_cut[i,0] = str(i+1)
        Angles_cut[i,2] = id_dict[Angles_cut[i,2]]
        Angles_cut[i,3] = id_dict[Angles_cut[i,3]]
        Angles_cut[i,4] = id_dict[Angles_cut[i,4]]
    Angles_str = array2str(Angles_cut)

    f = open(relmp,"w")
    Header = modify_header(Header,"atoms",natoms)
    Header = modify_header(Header,"bonds",nbonds)
    Header = modify_header(Header,"angles",nangles)
    f.write(Header)
    for term in terms:
        term_info = read_data(lmp,term)
        if "Atoms" in term:
            term_info = Atoms_str
        if "Bonds" in term:
            term_info = Bonds_str
        if "Angles" in term:
            term_info = Angles_str
        if "Velocities" in term:
            pass
        else:
            f.write(term)
            f.write(term_info)
    f.close()
    print("\n>>> Cut lammps data successfully !\n")   
    return



if __name__ == '__main__':

    print(__version__())
    # msi2clayff("sio2_1nm.data","sio2_1nm_clayff.data")

    