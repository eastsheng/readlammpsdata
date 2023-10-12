import readlammpsdata as rld

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

def msi2clayff(lmp,clayff_lmp):
	Header = rld.read_data(lmp,"Header")
	# print(Header)
	Masses = rld.read_data(lmp,"Masses").split("\n")
	mass_dict = {"sz":"28.085500","oz":"15.999400","oh":"15.999400","ho":"1.007970"}
	Masses = replace_term_info(Masses,mass_dict)
	
	PairCoeffs = rld.read_data(lmp,"Pair Coeffs").split("\n")
	pair_dict = {"sz":"0.00000184050       3.3020000000",
				 "oz":"0.15540000000       3.1655700000",
				 "oh":"0.15540000000       3.1655700000",
				 "ho":"0.00000000000       0.0000000000"}
	PairCoeffs = replace_term_info(PairCoeffs,pair_dict)

	BondCoeffs = rld.read_data(lmp,"Bond Coeffs").split("\n")
	bond_dict = {"oh-ho":"554.1349     1.0000"}
	BondCoeffs = replace_term_info(BondCoeffs,bond_dict)
	bond_type_number = len(BondCoeffs)

	AngleCoeffs = rld.read_data(lmp,"Angle Coeffs").split("\n")
	angle_dict = {"sz-oh-ho":"30.0     109.47"}
	AngleCoeffs = replace_term_info(AngleCoeffs,angle_dict)
	angle_type_number = len(AngleCoeffs)

	Atoms = rld.read_data(lmp,"Atoms")
	# print(Atoms)

	Bonds = rld.read_data(lmp,"Bonds")
	Bonds = rld.str2array(Bonds)
	new_bonds = select_term_info(BondCoeffs,Bonds)
	bond_number = len(new_bonds)
	
	Angles = rld.read_data(lmp,"Angles")
	Angles = rld.str2array(Angles)
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
	lmp = "sio2_1nm.data"
	clayff_lmp = "sio2_1nm_clayff.data"
	msi2clayff(lmp,clayff_lmp)