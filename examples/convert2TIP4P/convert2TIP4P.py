import readlammpsdata as rld


if __name__ == "__main__":
	# print(help(rld))
	lmp = "Methane_hydrate.data"
	tip4p_lmp = "Methane_hydrate_tip4p.data"
	tip4p_lmp_ua = "Methane_hydrate_UA_tip4p.data"
	rld.lmp2tip4p(lmp,tip4p_lmp,ua=False)
	rld.lmp2tip4p(lmp,tip4p_lmp_ua,ua=True)
