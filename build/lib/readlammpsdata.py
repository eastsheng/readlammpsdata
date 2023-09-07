# A script to read lammps data
import numpy as np
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


def search_chars(data_sub_str):
    char_list = ["","Masses",
                    "Pair Coeffs","Bond Coeffs","Angle Coeffs","Dihedral Coeffs","Improper Coeffs",
                    "Atoms","Bonds","Angles","Dihedrals","Impropers",""]
    data_sub_list = ["Header", "Masses",
                    "Pair Coeffs","Bond Coeffs","Angle Coeffs","Dihedral Coeffs","Improper Coeffs",
                    "Atoms","Bonds","Angles","Dihedrals","Impropers"]                
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
    char1,char2 = search_chars(data_sub_str)       
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


if __name__ == '__main__':
    path = "./(C6H9NO)1/"
    lmp1 = path+"tmp/UNK_0735D7.lmp"

    data_sub_list = ["Header", "Masses",
                    "Pair Coeffs","Bond Coeffs","Angle Coeffs","Dihedral Coeffs","Improper Coeffs",
                    "Atoms # full","Bonds","Angles","Dihedrals","Impropers"] 

    # Atoms = read_data(lmp1, data_sub_str = "Atoms # full")
    Atoms = read_data(lmp1, data_sub_str = "Bonds")
    Atoms = str2array(Atoms)
    print(Atoms)


    