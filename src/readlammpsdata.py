# A script to read lammps data
import numpy as np
from collections import Counter
import periodictable as pt
import time

def __version__():
    """
    read the version of readlammpsdata
    """
    version = "1.0.9"
    return version

def print_version():
    version = __version__()
    print(50*"-")
    print("@readlammpsdata-"+version)
    print(">>> A script for reading and modifying LAMMPS data!")
    print(50*"-")
    return

def print_line(func):
    
    def wrapper(*args, **kwargs):
        print(21*"-"," Program Start ",21*"-")
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(20*"-","Run time:",round(elapsed_time,2),"s ",20*"-")
    return wrapper

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
    box = {
        "xlo":x[0],
        "xhi":x[1],
        "ylo":y[0],
        "yhi":y[1],
        "zlo":z[0],
        "zhi":z[1],
    }
    return box



def read_atom_info(lmp,info="atoms"):
    """
    read numebr of atoms from lammps data:
    lmp: lammps data file
    info: Keywords to be read, including: 
        "atoms","bonds","angles","dihedrals","impropers",
        "atom types","bond types","angle types","dihedral types","improper types"
    """
    info_list_all = ["atoms","bonds","angles","dihedrals","impropers",
    "atom types","bond types","angle types","dihedral types","improper types"]
    info_list = []
    Header = read_data(lmp,"Header").strip().split("\n")
    for i in range(len(Header)):
        for j in range(len(info_list_all)):
            if info_list_all[j] in Header[i]:
                info_list.append(info_list_all[j])
    info_list.insert(0,"\n")
    info_list.append("\n")
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
    terms = read_terms(lmp)
    data_sub_str = "Atoms"
    for term in terms:
        if "Atoms" in term:
            Atoms_term = term
    Atoms = read_data(lmp, data_sub_str=Atoms_term)
    Atoms = str2array(Atoms)
    charges = np.float64(np.array(Atoms[:,3]))
    print(">>> Read charges successfully !")
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
    Lx = read_len(lmp,direction="x")
    Ly = read_len(lmp,direction="y")
    Lz = read_len(lmp,direction="z")

    vlo = Lx*Ly*Lz*1e-3

    print(">>> Read volume of system successfully !")
    return vlo

@print_line
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

@print_line
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

@print_line
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

@print_line
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

    print(">>> Modified the pore size of lammpsdata successfully !")
    return

@print_line
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
    print(">>> Congratulations! the sorted lmp is successfully generated !")
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
        # try:
        #     element.append(m[3])
        # except:
        #     pass
    idMass_dict = dict(zip(mass_id,mass))
    element = mass2element_list(idMass_dict)
    idElem_dict = dict(zip(mass_id,element))
    print(">>> Read the id masses and element dicts successfully !")
    return idMass_dict, idElem_dict


def mass2element_list(idMass_dict):
    allelements = pt.elements
    all_idMass_dict = {}
    for element in allelements:
        if element.symbol not in ["n"]:
            all_idMass_dict[element.symbol] = element.mass
    elements_list = []
    for key, value in idMass_dict.items():
        ele = find_match(all_idMass_dict,value)
        elements_list.append(ele)
    print(">>> Convert the id masses to element list successfully !")
    return elements_list


def mass2element_symbol(lmp):
    """
    Convert the masses obtained from lammps data to element symbols
    lmp: lammps data
    """
    idMass_dict, idElem_dict = read_mass(lmp)

    elements_list = mass2element_list(idMass_dict)
    elements_symbols = " ".join(elements_list)

    print(">>> Convert the masses obtained from lammps data to element symbols successfully !")
    return elements_symbols


@print_line
def lmp2xyz(lmp,xyzfile):
    """
    convert lammps data (lmp) file to xyz file
    lmp: lammps data file
    xyzfile: xyz file
    """
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
        f.write("Generated by lmp2xyz in 'readlammpsdata' package, Identified by relative atomic mass\n")
        for i in range(numOfAtoms):
            for j in range(4):
                f.write(xyz[i,j]+"\t")
            f.write("\n")
    print(">>> Convert lammps data (lmp) file to xyz file successfully !")
    return


@print_line
def lmp2lammpstrj(lmp,lammpstrj):
    """
    convert lammps data (lmp) file to xyz file
    lmp: lammps data file
    lammpstrj: lammpstrj file
    """
    idMass_dict, idElem_dict = read_mass(lmp)
    Atoms = read_data(lmp,"Atoms").strip()
    Atoms = str2array(Atoms)
    atom_id = Atoms[:,0]
    mol_id = Atoms[:,1]
    type_id = Atoms[:,2]

    elements_list = []
    numOfAtoms = len(type_id)
    for i in range(numOfAtoms):
        elements_list.append(idElem_dict[type_id[i]])
    elements_array = np.array(elements_list).reshape((-1,1))
    pos = Atoms[:,4:7]
    xyz = np.hstack((atom_id.reshape(-1,1),mol_id.reshape(-1,1),elements_array,type_id.reshape(-1,1),pos))
    m,n = xyz.shape
    box = read_box(lmp)
    with open(lammpstrj,"w") as f:
        f.write("ITEM: TIMESTEP\n")
        f.write("0\n")
        f.write("ITEM: NUMBER OF ATOMS\n")
        f.write(str(numOfAtoms)+"\n")
        f.write("ITEM: BOX BOUNDS pp pp pp\n")
        f.write(str(box['xlo'])+'\t'+str(box['xhi'])+"\n")
        f.write(str(box['ylo'])+'\t'+str(box['yhi'])+"\n")
        f.write(str(box['zlo'])+'\t'+str(box['zhi'])+"\n")
        f.write("ITEM: ATOMS id mol element type x y z \n")
        for i in range(m):
            for j in range(n):
                f.write(xyz[i,j]+"\t")
            f.write("\n")
    print(">>> Convert lammps data (lmp) file to lammpstrj file successfully !")
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

def select_term_info(XCoeffs,term):
    m, n = term.shape
    new_terms = []
    for i in range(m):
        for j in range(len(XCoeffs)):
            if int(term[i][1]) == int(XCoeffs[j].split()[0]):
                new_terms.append(term[i].tolist())
                # print(term[i])
    return new_terms

def replace_charges(Atoms,charges_dict,atoms_id_dict):
    for i in range(len(Atoms)):
        Atoms[i,3] = charges_dict[atoms_id_dict[Atoms[i,2]]]
    return Atoms


@print_line
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
    Atoms = str2array(Atoms)
    charges_dict = {"sz":"2.100000","oz":"-1.050000","oh":"-0.950000","ho":"0.425000"}
    atoms_id_dict = {}
    for item in Masses:
        words = item.split()
        key = words[0]
        value = words[-1]
        atoms_id_dict[key] = value
    Atoms = replace_charges(Atoms,charges_dict,atoms_id_dict)
    Atoms = array2str(Atoms)
    
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

        if bond_type_number!=0:
            f.write("\nBond Coeffs\n\n")
        for b in BondCoeffs:
            if bond_type_number == 1:
                b = b.strip().split()
                b[0] = "1"
                b = "\t".join(b)
            f.write("\t"+b+"\n")

        if angle_type_number!=0:
            f.write("\nAngle Coeffs\n\n")
        for a in AngleCoeffs:
            if angle_type_number == 1:
                a = a.strip().split()
                a[0] = "1"
                a = "\t".join(a)
            f.write("\t"+a+"\n")
            
        f.write("\nAtoms")
        f.write(Atoms)

        if bond_number!=0:
            f.write("Bonds\n\n")
        for i in range(bond_number):
            for j in range(4):
                new_bonds[i][0] = str(i+1)
                if bond_type_number == 1:
                    new_bonds[i][1] = str(bond_type_number)

                f.write(new_bonds[i][j]+"\t")
            f.write("\n")
        if angle_number!=0:
            f.write("\nAngles\n\n")
        for i in range(angle_number):
            for j in range(5):
                if angle_type_number == 1:
                    new_angles[i][1] = str(angle_type_number)
                new_angles[i][0] = str(i+1)
                f.write(new_angles[i][j]+"\t")
            f.write("\n")
    print(">>> Convert a lmp obtained from msi2lmp to clayff force field successfully !")
    return

@print_line
def msi2clayff_OH(lmp, clayff_lmp):
    """
    # J. Phys. Chem. B, Vol. 108, No. 4, 2004 1259
    convert a lmp with OH group obtained from msi2lmp (from Materials Studio) to clayff force field
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
    Atoms = str2array(Atoms)
    charges_dict = {"sz":"2.100000","oz":"-1.050000","oh":"-0.950000","ho":"0.425000"}
    atoms_id_dict = {}
    for item in Masses:
        words = item.split()
        key = words[0]
        value = words[-1]
        atoms_id_dict[key] = value
    Atoms = replace_charges(Atoms,charges_dict,atoms_id_dict)
    Atoms = array2str(Atoms)

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
    print(">>> Convert a lmp obtained from msi2lmp to clayff force field successfully !")
    return


@print_line
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

@print_line
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
    elements = mass2element_symbol(lmp).split()
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
        print(">>> Convert TIP4P/CH4 lmp successfully !")
    else:
        print(">>> Convert TIP4P/CT lmp successfully !")

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
    print(">>> Convert a array to a string for writing successfully !")

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

def modify_header(Header,hterm,value):
    """
    modify the "Header" info, including number of "atoms", "bonds", "angles", "dihedrals", "impropers",
    "atom types", "bond types", "angle types", "dihedral types", "improper types",
    "xlo xhi", "ylo yhi", "zlo zhi".
    Header: Header
    hterm: "atoms", "bonds"
    value: number of "atoms", "bonds"..., int; if "xlo xhi", value = [xlo, xhi]
    """
    Header = Header.strip().split("\n")
    for i in range(len(Header)):
        if Header[i]!="":
            Header[i] = Header[i].strip()
            if hterm in Header[i]:
                Header[i] = Header[i].split()
                if len(Header[i]) == 2:
                    Header[i][0] = str(value)
                    Header[i] = "  ".join(Header[i])
                elif len(Header[i]) == 3:
                    Header[i][0] = str(value)
                    Header[i] = " ".join(Header[i])
                elif len(Header[i]) == 4:
                    Header[i][0] = str(value[0])
                    Header[i][1] = str(value[1])
                    Header[i] = " ".join(Header[i])
    Header = "\n".join(Header)+"\n\n"
    print(">>> modify the Header "+ hterm +" successfully !")

    return Header

@print_line
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
    print(">>> Add methane molecules into half cages at the interface successfully !")

    return

@print_line
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
    Atoms = str2array(Atoms_info)[:,:7]
    ll = read_len(lmp,direction)
    box = read_box(lmp)
    lo = box[lo_label]
    hi = box[hi_label]
    m,n = Atoms.shape
    for i in range(m):
        Atoms[i][index] = float(Atoms[i][index])-distance
        if float(Atoms[i][index]) < lo:
            Atoms[i][index] = float(Atoms[i][index])+ll
        elif float(Atoms[i][index]) > hi:
            Atoms[i][index] = float(Atoms[i][index])-ll

        Atoms[i][index] = str(float(Atoms[i][index]))

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
    print(">>> Moved boundary of lammps data successfully !")   
    return

@print_line
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
    print(">>> Calculating density from lammps data successfully !")
    return rho_array


@print_line
def cut_lmp(lmp,relmp,distance,direction="y"):
    """
    cut lammps data of hydrate
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
    print(">>> Cut lammps data successfully !")   
    return

def unique_list(my_list):
    uniquelist = []
    for item in my_list:
        if item not in uniquelist:
            uniquelist.append(item)
    return uniquelist


@print_line
def cut_lmp_atoms(lmp,relmp,cut_block={"dx":[0,0],"dy":[0,0],"dz":[0,0]}):
    """
    cut lammps data
    lmp: original lammps data
    relmp: rewrite lammps data
    cut_block: {"dx":[0,0],
                "dy":[0,0],
                "dz":[0,0]
                } / angstrom
    """
    terms = read_terms(lmp)
    Header = read_data(lmp,"Header")
    Atoms = str2array(read_data(lmp,"Atoms"))
    m,n = Atoms.shape
    Atoms = Atoms.tolist()
    Atoms_save = []
    x_start = cut_block["dx"][0]
    x_stop  = cut_block["dx"][1]
    y_start = cut_block["dy"][0]
    y_stop  = cut_block["dy"][1]
    z_start = cut_block["dz"][0]
    z_stop  = cut_block["dz"][1]

    for i in range(m):
        if float(Atoms[i][4]) <= x_start or float(Atoms[i][4]) >= x_stop:
            Atoms_save.append(Atoms[i])
        if float(Atoms[i][5]) <= y_start or float(Atoms[i][5]) >= y_stop:
            Atoms_save.append(Atoms[i])
        if float(Atoms[i][6]) <= z_start or float(Atoms[i][6]) >= z_stop:
            Atoms_save.append(Atoms[i])
    
    Atoms_save = unique_list(Atoms_save)
    # print(Atoms_save)
    Atoms_save = np.array(Atoms_save)
    natoms = len(Atoms_save)
    for i in range(natoms):
        Atoms_save[i,0] = str(i+1)
    Atoms = array2str(Atoms_save)

    f = open(relmp,"w")
    Header = modify_header(Header,"atoms",natoms)
    f.write(Header)
    for term in terms:
        term_info = read_data(lmp,term)
        if "Atoms" in term:
            f.write(term)
            f.write(Atoms)
        else:
            f.write(term)
            f.write(term_info)
    f.close()
    print(">>> Cut lammps data successfully !")   
    return


@print_line
def combine_lmp(lmp,add_lmp,new_lmp,move_xyz,type_dict):
    """
    combin two lammps data, default combine the first bond and angle (of add_lmp) and first type (of lmp),
    other bonds and angles, add it in order
    lmp: first lammps data
    add_lmp: second lammps data
    new_lmp: combined lammps data
    move_xyz: move_xyz = [dx, dy, dz], for example, move = [0, 60, -13.5]
    type_dict: type in add_lmp, cover, or append the type in lmp
        {"1":"cover","2":"cover","3":"append","4":"append"....,"5":"append"}
        for example: type_dict = {"1":"cover","2":"cover", "3":"append", "4":"append"}
    """

    add_natomtype = 0
    for key, value in type_dict.items():
        if value == "append":
            add_natomtype += 1

    lmp_Atoms_str = read_data(lmp,"Atoms")
    lmp_Atoms = str2array(lmp_Atoms_str)[:,:7]
    add_lmp_Atoms = read_data(add_lmp,"Atoms")
    add_lmp_Atoms = str2array(add_lmp_Atoms)[:,:7]
    max_nid = max(lmp_Atoms[:,0].astype(int))
    max_nmol = max(lmp_Atoms[:,1].astype(int))
    m = len(add_lmp_Atoms)
    natomtypes = read_atom_info(lmp,"atom types")
    new_natomtypes = natomtypes+add_natomtype
    diffence_natoms = new_natomtypes-natomtypes
    origin_id,new_id = [],[]
    for i in range(m):
        try:
            if type_dict[add_lmp_Atoms[i][2]]=="cover":
                pass
            elif type_dict[add_lmp_Atoms[i][2]]=="append":
                add_lmp_Atoms[i][2] = str(natomtypes+int(add_lmp_Atoms[i][2])-diffence_natoms)
            else:
                pass
        except:
            print("??? Default cover atomic types!")

        origin_id.append(int(add_lmp_Atoms[i][0]))
        add_lmp_Atoms[i][0] = str(max_nid+i+1)
        new_id.append(int(add_lmp_Atoms[i][0]))
        add_lmp_Atoms[i][1] = str(max_nmol+int(add_lmp_Atoms[i][1]))
        add_lmp_Atoms[i][4] = str(float(add_lmp_Atoms[i][4])+move_xyz[0])
        add_lmp_Atoms[i][5] = str(float(add_lmp_Atoms[i][5])+move_xyz[1])
        add_lmp_Atoms[i][6] = str(float(add_lmp_Atoms[i][6])+move_xyz[2])

    natoms = len(add_lmp_Atoms)+max_nid
    new_Atoms = np.vstack((lmp_Atoms,add_lmp_Atoms))
    new_Atoms = array2str(new_Atoms)
    id_dict = dict(zip(origin_id,new_id))

    lmp_Bonds_str = read_data(lmp,"Bonds")
    lmp_Bonds = str2array(lmp_Bonds_str)
    add_lmp_Bonds = read_data(add_lmp,"Bonds")
    add_lmp_Bonds = str2array(add_lmp_Bonds).tolist()
    n = len(add_lmp_Bonds)
    max_nb = max(lmp_Bonds[:,0].astype(int))
    for i in range(n):
        add_lmp_Bonds[i][0] = str(max_nb+i+1)
        add_lmp_Bonds[i][2] = np.str_(id_dict[int(add_lmp_Bonds[i][2])])
        add_lmp_Bonds[i][3] = np.str_(id_dict[int(add_lmp_Bonds[i][3])])
    nbonds = len(add_lmp_Bonds)+max_nb
    add_lmp_Bonds = np.array(add_lmp_Bonds)
    new_Bonds = np.vstack((lmp_Bonds,add_lmp_Bonds))
    new_Bonds = array2str(new_Bonds)
    
    lmp_Angles_str = read_data(lmp,"Angles")
    lmp_Angles = str2array(lmp_Angles_str)
    add_lmp_Angles = read_data(add_lmp,"Angles")
    add_lmp_Angles = str2array(add_lmp_Angles).tolist()
    n = len(add_lmp_Angles)
    max_na = max(lmp_Angles[:,0].astype(int))
    for i in range(n):
        add_lmp_Angles[i][0] = str(max_na+i+1)
        add_lmp_Angles[i][2] = str(id_dict[int(add_lmp_Angles[i][2])])
        add_lmp_Angles[i][3] = str(id_dict[int(add_lmp_Angles[i][3])])
        add_lmp_Angles[i][4] = str(id_dict[int(add_lmp_Angles[i][4])])
    nangles = len(add_lmp_Angles)+max_na
    add_lmp_Angles = np.array(add_lmp_Angles)
    new_Angles = np.vstack((lmp_Angles,add_lmp_Angles))
    new_Angles = array2str(new_Angles)
    
    Header = read_data(lmp,"Header")
    Header = modify_header(Header,"atoms",natoms)
    Header = modify_header(Header,"bonds",nbonds)
    Header = modify_header(Header,"angles",nangles)
    Header = modify_header(Header,"atom types",new_natomtypes)
    lmp_ylo = read_box(lmp)["ylo"]
    lmp_yhi = read_box(lmp)["yhi"]
    add_lmp_ylen = read_len(add_lmp,"y")

    Header = modify_header(Header,"ylo yhi",[lmp_ylo,lmp_yhi+add_lmp_ylen])

    lmp_Masses = list(read_mass(lmp)[0].items())
    add_lmp_Masses = list(read_mass(add_lmp)[0].items())

    lmp_Masses = merge_masslists(lmp_Masses,add_lmp_Masses,natomtypes,diffence_natoms)
    lmp_Masses = array2str(np.array(lmp_Masses))

    f = open(new_lmp,"w")
    f.write(Header)
    terms = read_terms(lmp)
    for term in terms:
        term_info = read_data(lmp,term)
        if "Masses" in term:
            term_info = lmp_Masses
        if "Atoms" in term:
            term_info = new_Atoms
        if "Bonds" in term:
            term_info = new_Bonds
        if "Angles" in term:
            term_info = new_Angles
        if "Velocities" in term or \
           "Pair Coeffs" in term or \
           "Bond Coeffs" in term or \
           "Angle Coeffs" in term:
            pass
        else:
            f.write(term)
            f.write(term_info)
    f.close()
    print(">>> Combine lammps data successfully !")   

    return

def merge_masslists(list1, list2,natomtypes,diffence_natoms):
    merged_list = list1
    for item in list2:
        if item not in list1:
            item = list(item)
            item[0] = str(int(item[0])+natomtypes-diffence_natoms)
            merged_list.append(item)
    return merged_list


def change_type_order(lmp,relmp,atom_types=[8,9],updown=4):
    """
    change the order of atomic types
    lmp: lammps data
    relmp: rewrite lammps data
    atom_types: atom types need to move/change, for example: atom_types=[8,9]
    updown: move/change step, > 0 is up ,<0 is down, 
            1 2 3 4 5 6 7 <-8 9; 1 2 3 <-8 9 4 5 6 7, updown = 4
    """
    Masses = list(read_mass(lmp)[0].items())
    nmasses = len(Masses)
    origin_all_types, new_all_types = [],[]
    for i in range(nmasses):
        origin_all_types.append(list(Masses[i])[0])
        if int(Masses[i][0]) in atom_types:
            Masses[i] = list(Masses[i])
            Masses[i][0] = str(int(Masses[i][0])-updown)
        else:
            if int(Masses[i][0]) >= nmasses-updown-1:
                Masses[i] = list(Masses[i])
                Masses[i][0] = str(int(Masses[i][0])+len(atom_types))
    Masses = np.array(Masses)
    Masses =  Masses[np.argsort([int(x) for x in Masses[:, 0]])]
    lmp_Masses = array2str(Masses)
    move_term = origin_all_types[-len(atom_types):]
    new_all_types = origin_all_types[:-len(atom_types) + updown+1] + move_term + \
                    origin_all_types[-2 + updown+1:-len(atom_types)]
    type_dict = dict(zip(new_all_types,origin_all_types))
    # print(type_dict)

    Atoms = str2array(read_data(lmp,"Atoms"))
    m = len(Atoms)
    for i in range(m):
        Atoms[i][2] = type_dict[Atoms[i][2]]
    new_Atoms = array2str(Atoms)
    f = open(relmp,"w")
    Header = read_data(lmp,"Header")
    f.write(Header)
    terms = read_terms(lmp)
    for term in terms:
        term_info = read_data(lmp,term)
        if "Masses" in term:
            term_info = lmp_Masses
        if "Atoms" in term:
            term_info = new_Atoms
        if "Velocities" in term or \
           "Pair Coeffs" in term or \
           "Bond Coeffs" in term or \
           "Angle Coeffs" in term:
            pass
        else:
            f.write(term)
            f.write(term_info)
    f.close()
    print(">>> Change the order of atomic types successfully !")   
    return

@print_line
def exchange_position(lmp,relmp,id1,id2):
    """
    exchange the position id1 and id2
    lmp: lammps data
    relmp: rewrite lammps data
    id1: the id of first particle, a int list, for example, [a1,b1]
    id2: the id of second particle, a int list, for example, [a2,b2]. 
    a1 and a2, b1 and b2 will exchange position
    """
    Atoms = read_data(lmp,"Atoms")
    Atoms = str2array(Atoms)
    m = len(Atoms)
    n = len(id1)
    for j in range(n):
        for i in range(m):
            if int(Atoms[i][0]) == id1[j]:
                mol1 = Atoms[i][1]
                x1,y1,z1 = Atoms[i][4],Atoms[i][5],Atoms[i][6]
            elif int(Atoms[i][0]) == id2[j]:
                mol2 = Atoms[i][1]
                x2,y2,z2 = Atoms[i][4],Atoms[i][5],Atoms[i][6]
        dx = float(x1)-float(x2)
        dy = float(y1)-float(y2)
        dz = float(z1)-float(z2)
        for i in range(m):
            if Atoms[i][1] == mol1:
                Atoms[i][4] = str(float(Atoms[i][4]) - dx)
                Atoms[i][5] = str(float(Atoms[i][5]) - dy)
                Atoms[i][6] = str(float(Atoms[i][6]) - dz)
            elif Atoms[i][1] == mol2:
                Atoms[i][4] = str(float(Atoms[i][4]) + dx)
                Atoms[i][5] = str(float(Atoms[i][5]) + dy)
                Atoms[i][6] = str(float(Atoms[i][6]) + dz)

    new_Atoms = array2str(Atoms)

    f = open(relmp,"w")
    Header = read_data(lmp,"Header")
    f.write(Header)
    terms = read_terms(lmp)
    for term in terms:
        term_info = read_data(lmp,term)
        if "Atoms" in term:
            term_info = new_Atoms

        f.write(term)
        f.write(term_info)
    f.close()
    print(">>> Change the order of atomic types successfully !")   
    return

@print_line
def change_lmp_axis(lmp,relmp,axis_list=["y","z","x"]):
    """
    change axis of lmp full
    Parameters:
    - lmp: lammps data
    - relmp: rewrite lammps data
    - axis_list: a list including new order of axis, like ["y","z","x"]
    """
    axis_dict = {"x":4,"y":5,"z":6}
    Atoms = read_data(lmp,"Atoms")
    Atoms = str2array(Atoms)
    Atoms[:, [axis_dict["x"],axis_dict["y"],axis_dict["z"]]] = \
    Atoms[:, [axis_dict[axis_list[0]],axis_dict[axis_list[1]],axis_dict[axis_list[2]]]]

    Header = read_data(lmp,"Header")
    box = read_box(lmp)
    axis_dict = {"x":["xlo","xhi"],"y":["ylo","yhi"],"z":["zlo","zhi"]}
    new_axis_dict = {axis_list[i]: axis_dict[axis_list[i]] for i in range(len(axis_list))}
    new_keys = ['x', 'y', 'z']
    modified_dict = {new_keys[i]: new_axis_dict[old_key] for i, old_key in enumerate(new_axis_dict)}

    new_xlo = box[modified_dict["x"][0]]
    new_xhi = box[modified_dict["x"][1]]
    new_ylo = box[modified_dict["y"][0]]
    new_yhi = box[modified_dict["y"][1]]
    new_zlo = box[modified_dict["z"][0]]
    new_zhi = box[modified_dict["z"][1]]

    Header = modify_header(Header,"xlo xhi",[new_xlo,new_xhi])
    Header = modify_header(Header,"ylo yhi",[new_ylo,new_yhi])
    Header = modify_header(Header,"zlo zhi",[new_zlo,new_zhi])
    
    new_Atoms = array2str(Atoms)

    f = open(relmp,"w")
    f.write(Header)
    terms = read_terms(lmp)
    for term in terms:
        term_info = read_data(lmp,term)
        if "Atoms" in term:
            term_info = new_Atoms

        f.write(term)
        f.write(term_info)
    f.close()

    print(">>> Change axis to ("+" ".join(axis_list)+") successfully !")
    return

@print_line
def coord2zero(lmp,relmp):
    """
    Coordinate starting point to zero
    Parameters:
    - lmp: lammps data
    - relmp: rewrite lammps data
    """
    Header = read_data(lmp,"Header")
    box = read_box(lmp)
    xlo = float(box["xlo"])
    ylo = float(box["ylo"])
    zlo = float(box["zlo"])
    Atoms = read_data(lmp,"Atoms")
    Atoms = str2array(Atoms)
    xyz = Atoms[:,[4,5,6]].astype(float)
    xyz[:,0] -= xlo
    xyz[:,1] -= ylo
    xyz[:,2] -= zlo
    Atoms[:,[4,5,6]] = xyz
    Lx = round(read_len(lmp,"x"),6)
    Ly = round(read_len(lmp,"y"),6)
    Lz = round(read_len(lmp,"z"),6)
    Header = modify_header(Header,"xlo xhi",[0,Lx])
    Header = modify_header(Header,"ylo yhi",[0,Ly])
    Header = modify_header(Header,"zlo zhi",[0,Lz])
    
    new_Atoms = array2str(Atoms)

    f = open(relmp,"w")
    f.write(Header)
    terms = read_terms(lmp)
    for term in terms:
        term_info = read_data(lmp,term)
        if "Atoms" in term:
            term_info = new_Atoms

        f.write(term)
        f.write(term_info)
    f.close()

    print(">>> Coordinate starting point to zero successfully !")
    return


def adjust_distance_periodic_rectangular(point1, point2, box_size):
    point1_array = np.array(point1)
    point2_array = np.array(point2)
    distances = np.abs(point1_array - point2_array)
    adjusted_distances = np.where(distances > np.array(box_size) / 2, np.array(box_size) - distances, distances)
    
    adjusted_point2 = point1_array + np.sign(point2_array - point1_array) * adjusted_distances

    return point1, adjusted_point2

def find_closest_SiO_index(Atoms_Si,Atoms_Oh,box):
    closest_indices = []
    for row1 in Atoms_Si:
        coords1 = row1[4:7].astype(float)
        point1, adjusted_point2 = adjust_distance_periodic_rectangular(Atoms_Oh[:, 4:7].astype(float),coords1,box)
        distances = np.linalg.norm(point1 - adjusted_point2, axis=1)
        indices = np.where(distances < 2.0)
        # print(indices)
        try:
            closest_index1 = indices[0][0]
            closest_index2 = indices[0][1]
            closest_indices.append([row1[0], Atoms_Oh[closest_index1, 0]])
            closest_indices.append([row1[0], Atoms_Oh[closest_index2, 0]])
        except:
            closest_index1 = indices[0][0]
            closest_indices.append([row1[0], Atoms_Oh[closest_index1, 0]])

    closest_indices = np.array(closest_indices)
    return closest_indices

def find_closest_OH_index(Atoms_Oh,Atoms_Ho):
    closest_indices = []
    for row1 in Atoms_Oh:
        coords1 = row1[4:7].astype(float)
        distances = np.linalg.norm(Atoms_Ho[:, 4:7].astype(float) - coords1, axis=1)
        closest_index = np.argmin(distances)
        closest_indices.append([row1[0], Atoms_Ho[closest_index, 0]])
    closest_indices = np.array(closest_indices)
    return closest_indices

def addH(lmp,relmp,H_block,ang=90,direction="y"):
    """
    Add hydroxyl groups to the surface of SiO2 in one direction or add hydrogen atoms
    Parameters:
    - lmp: lammps data of SiO2
    - relmp: lammps data of SiO2-OH
    - H_block: {"dx":[0,0],
                "dy":[0,0],
                "dz":[0,0]
               } / angstrom
    - ang1: angle° of H =330;
    - ang2: angle° of H =120;
    - direction: rotate direction of H, "x","y","z"
    """
    error = 0.99
    idMass_dict, idElem_dict = read_mass(lmp)
    Lx = read_len(lmp,"x")
    Ly = read_len(lmp,"y")
    Lz = read_len(lmp,"z")
    box = [Lx,Ly,Lz]
    ntype = len(idElem_dict)
    print(">>> Type: element",idElem_dict)
    idElem_dict = {value: key for key, value in idElem_dict.items()}

    Atoms = read_data(lmp,"Atoms")
    Atoms = str2array(Atoms)
    x_start = H_block["dx"][0]
    x_stop  = H_block["dx"][1]
    y_start = H_block["dy"][0]
    y_stop  = H_block["dy"][1]
    z_start = H_block["dz"][0]
    z_stop  = H_block["dz"][1]

    m, n = Atoms.shape
    Si_list, Oh_list = [], []
    start = [x_start,y_start,z_start]
    stop  = [x_stop,y_stop,z_stop]

    for i in range(m):
        if float(Atoms[i][4]) >= x_start and float(Atoms[i][4]) <= x_stop:
            if float(Atoms[i][5]) >= y_start and float(Atoms[i][5]) <= y_stop:
                if float(Atoms[i][6]) >= z_start and float(Atoms[i][6]) <= z_stop:
                    if Atoms[i,2] == "1":#idElem_dict["O"]:
                        if ntype == 4:
                            Atoms[i,2] = str(ntype-1)
                        else:
                            Atoms[i,2] = str(ntype+1)
                        Atoms[i,3] = "-0.950000"
                        Oh_list.append(Atoms[i,0])

        if float(Atoms[i][4]) >= x_start-error and float(Atoms[i][4]) <= x_stop+error:
            if float(Atoms[i][5]) >= y_start-error and float(Atoms[i][5]) <= y_stop+error:
                if float(Atoms[i][6]) >= z_start-error and float(Atoms[i][6]) <= z_stop+error:
                    if Atoms[i,2] == idElem_dict["Si"]:
                        Si_list.append(Atoms[i,0])
    # print(Oh_list)
    # unique_list(my_list)
    Atoms_Ho = Atoms[np.isin(Atoms[:, 0], Oh_list)]
    Atoms_Si = Atoms[np.isin(Atoms[:, 0], Si_list)]
    # print(Atoms_Ho)
    Header = read_data(lmp,"Header")
    # Add an atomic type to hydroxy-oxygen
    # Header = modify_header(Header,"atom types",ntype+1).strip()
    Masses = read_data(lmp,"Masses").strip()
    # Add mass info to hydroxy-oxygen
    if ntype == 2:
        add_Ohmass = "\n"+str(ntype+1)+" "+idMass_dict[idElem_dict["O"]]+"  # Oh"
        Masses += add_Ohmass
        # Add an atomic type for hydroxy hydrogen
        Header = modify_header(Header,"atom types",ntype+2).strip()
        # Add mass info to hydroxy hydrogen
        add_Homass = "\n"+str(ntype+2)+"  1.008000  # H\n"
        Masses += add_Homass
    else:
        pass
    nHo = len(Atoms_Ho)
    print(">>> Add",str(nHo),"hydroxy hydrogen!")
    # Add hydrogen coordinates
    Atoms_Ho[:,0] = np.arange(m + 1,nHo+m+1) # id
    if ntype == 2:
        Atoms_Ho[:,2] = ntype+2 # H type id
        Atoms_Ho[:,3] = "0.425000" # charge
    if ntype == 4:
        Atoms_Ho[:,2] = ntype # H type id
        Atoms_Ho[:,3] = "0.425000" # charge
    
    angle = np.radians(ang)
    if direction=="x":
        matrix = [0, np.cos(angle), np.sin(angle)]
    elif direction=="y":
        matrix = [np.cos(angle), 0, np.sin(angle)]
    elif direction=="z":
        matrix = [np.cos(angle), np.sin(angle), 0]
    else:
        matrix = [0, np.cos(angle), np.sin(angle)]
    dist = np.array(matrix)
    for i in range(nHo):
        Atoms_Ho[i,4:7] = Atoms_Ho[i,4:7].astype(float) + dist

    Atoms_addH = np.vstack((Atoms,Atoms_Ho))

    # Modify the total number of atoms
    Header = modify_header(Header,"atoms",m+nHo).strip()
    # generate Bonds
    try:
        initBonds = str2array(read_data(lmp,"Bonds"))
        init_nBonds=len(initBonds)
    except:
        init_nBonds = 0

    try:
        Atoms_Oh = Atoms[np.isin(Atoms[:, 0], Oh_list)]
        closest_indices0 = find_closest_OH_index(Atoms_Oh,Atoms_Ho)

        addBonds = closest_indices0

        naddBonds = len(addBonds)
        Bondsid = np.arange(1+init_nBonds,naddBonds+init_nBonds+1) # bond id
        addBonds = np.insert(addBonds, 0, 1, axis=1)
        addBonds = np.insert(addBonds, 0, Bondsid, axis=1)
        # Modify the total number of Bonds
        Header = modify_header(Header,"bonds",naddBonds+init_nBonds).strip()
        # Modify the total number of bond types
        Header = modify_header(Header,"bond types",1).strip()
        if init_nBonds == 0:
            Bonds = addBonds
        else:
            Bonds = np.vstack((initBonds,addBonds))
        Bonds = array2str(Bonds).strip()
    except:
        print("??? add Bonds error!")
    # generate Angles
    try:
        initAngles = str2array(read_data(lmp,"Angles"))
        init_nAngles=len(initAngles)
    except:
        init_nAngles = 0
    try:
        closest_indices1 = find_closest_SiO_index(Atoms_Si,Atoms_Oh,box)
        # print(closest_indices1)
        nAngles = len(closest_indices1)
        print(">>> add ",str(nAngles)," Angles!")
        OH_dict = dict(closest_indices0)
        # print(OH_dict)
        new_OH = []
        for i in range(nAngles):
            new_OH.append(OH_dict[closest_indices1[i,1]])
        new_OH = np.array(new_OH).reshape(-1,1)
        addAngles = np.hstack((closest_indices1,new_OH))
        Anglesid = np.arange(1+init_nAngles,nAngles+init_nAngles+1) # angle id
        addAngles = np.insert(addAngles, 0, 1, axis=1) # angle type
        addAngles = np.insert(addAngles, 0, Anglesid, axis=1)
        # Modify the total number of Angles
        Header = modify_header(Header,"angles",init_nAngles+nAngles).strip()
        # Modify the total number of angle types
        Header = modify_header(Header,"angle types",1).strip()
        if init_nAngles == 0:
            Angles = addAngles
        else:
            Angles = np.vstack((initAngles,addAngles))
        Angles = array2str(Angles).strip()
    except:
        print("??? add Angles error!")

    f = open(relmp,"w")
    f.write(Header)
    f.write("\n")
    Atoms_addH = array2str(Atoms_addH).strip()

    f.write("\n"+"Masses"+"\n\n")
    f.write(Masses)
    f.write("\n\n"+"Atoms # full"+"\n\n")
    f.write(Atoms_addH)
    try:
        f.write("\n\n"+"Bonds"+"\n\n")
        f.write(Bonds)
    except:
        print("??? write Bonds error!")

    try:
        f.write("\n\n"+"Angles"+"\n\n")
        f.write(Angles)
    except:
        print("??? write Angles error!")

    f.close()
    print(">>> Add hydroxyl groups successfully!")
    return



if __name__ == '__main__':

    # print(__version__())
    print_version()
    # msi2clayff("sio2_1nm.data","sio2_1nm_clayff.data")


