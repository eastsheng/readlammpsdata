# A script to read lammps data
import numpy as np

def __version__():

    version = "1.0.4"
    
    return print(version)

def extract_substring(string, char1, char2):
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
    try:
        sub = extract_substring(wholestr, char1,char2)
        sub.strip()
        print("Read data "+sub_char+" successfully !")
        return sub
    except:
        return "Warning: There is no "+sub_char+" term in your data!"

def read_terms(lmpfile):
    terms = ["Masses",
             "Pair Coeffs","Bond Coeffs","Angle Coeffs","Dihedral Coeffs","Improper Coeffs",
             "Atoms","Bonds","Angles","Dihedrals","Impropers"]
    new_terms = []
    with open(lmpfile, "r") as f:
        for line in f:
            # print(line)
            if line != "\n":
                line = line.split()[0]
                if line in terms:
                    new_terms.append(line)

    return new_terms

def search_chars(data_sub_str,lmpfile):
    char_list = read_terms(lmpfile)
    char_list.insert(0,"")
    char_list.append("")
    data_sub_list = read_terms(lmpfile)
    data_sub_list.insert(0,"Header")

    # char_list = ["","Masses",
    #                 "Pair Coeffs","Bond Coeffs","Angle Coeffs","Dihedral Coeffs","Improper Coeffs",
    #                 "Atoms","Bonds","Angles","Dihedrals","Impropers",""]
    # data_sub_list = ["Header", "Masses",
    #                 "Pair Coeffs","Bond Coeffs","Angle Coeffs","Dihedral Coeffs","Improper Coeffs",
    #                 "Atoms","Bonds","Angles","Dihedrals","Impropers"]                


    if data_sub_str in ["Atoms # full", "Atoms #"]:
        char_list[7] = "Atoms # full"
        data_sub_list[7] = "Atoms # full"
    else:
        pass

    for i in range(len(data_sub_list)):
        if data_sub_str == data_sub_list[i]:
            char1, char2 = char_list[i],char_list[i+1]
        else:
            pass
    try:
        return char1, char2
    except:
        char1, char2 = "",""
        print("ERROR: your 'data_sub_str' arg is error !")     
    return char1, char2

def read_data(lmpfile, data_sub_str):
    char1,char2 = search_chars(data_sub_str,lmpfile)       
    with open(lmpfile,'r') as sc:
        wholestr=sc.read()
        # print(wholestr)
        sub = read_data_sub(wholestr,data_sub_str,char1,char2)

    return sub

def str2array(strings):
    strings = list(strings.strip().split("\n"))
    strings = list(map(lambda ll:ll.split(), strings))
    array = np.array(strings)
    return array

def read_box(lmp):
    """
    read box size of lammps data:
    lmp: lammps data file
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



def read_Natoms(lmp):
    """
    read numebr of atoms from lammps data:
    lmp: lammps data file
    """
    Header = read_data(lmp, data_sub_str = "Header")
    Natoms = extract_substring(Header,"\n","atoms").strip().split()
    Natoms = list(map(lambda f:int(f), Natoms))[-1]
    return Natoms

def read_charges(lmp):
    """
    read charges info from lammps data:
    lmp: lammps data file
    """
    try:
        Atoms = read_data(lmp, data_sub_str = "Atoms")
        Atoms = str2array(Atoms)
    except:
        Atoms = read_data(lmp, data_sub_str = "Atoms # full")
        Atoms = str2array(Atoms)

    charges = np.float64(np.array(Atoms[:,3]))

    # charges = list(map(lambda f:float(f), Atoms[:,3]))

    return charges




if __name__ == '__main__':
    # path = "./(C6H9NO)1/"
    # lmp1 = path+"tmp/UNK_0735D7.lmp"

    # data_sub_list = ["Header", "Masses",
    #                 "Pair Coeffs","Bond Coeffs","Angle Coeffs","Dihedral Coeffs","Improper Coeffs",
    #                 "Atoms # full","Bonds","Angles","Dihedrals","Impropers"] 

    # # Atoms = read_data(lmp1, data_sub_str = "Atoms # full")
    # Atoms = read_data(lmp1, data_sub_str = "Bonds")
    # # Atoms = str2array(Atoms)
    # print(Atoms)
    __version__()

    