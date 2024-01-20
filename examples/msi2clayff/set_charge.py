# correct charges from ligpargen
import numpy as np
import readlammpsdata as rld

def set_charge_from_lmp(lmpfile):
    charge_list = []
    Atoms = rld.read_data(lmp1, data_sub_str = "Atoms")
    Atoms = rld.str2array(Atoms)
    charge_list = Atoms[:,3]
    print(charge_list)
    return charge_list


if __name__ == '__main__':
    # path = "./(C6H9NO)1/"
    # path = "./(C6H9NO)10/"
    # path = "./Lecithin-C42H80NO8P/"
    # path = "./SoyLecithin-C42H84NO8P/"

    path = "./PHL1T/"
    # path = "./PHL2T/"
    # path = "./LHP1T/"
    # path = "./LHP2T/"

    lmp1 = path+"PHL1T.lmp"
    start = 6
    charge_file = path+"system_"+str(start)+".in.charges"
    # charge_list_1 = set_charge_from_key(key1)
    charge_list_1 = set_charge_from_lmp(lmp1)

    charge_sum1 = round(sum(np.array(charge_list_1).astype(float)),4)

    len1 = len(charge_list_1)

    with open(charge_file,'w') as cf:
        L1 = len1        
        for i in range(start-1,start-1+L1):
            cf.write("set type "+str(i+1)+" charge "+charge_list_1[i-start]+'\n')

    print("-------------charges-------------\n",
          lmp1,"(",1,"~",L1,"): sum of charges = ",charge_sum1,"\n")

    