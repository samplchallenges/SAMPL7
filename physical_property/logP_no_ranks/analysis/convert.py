def get_logP(dG):
    ##################################################
    #### Convert transfer free energies to logP's ####
    ##################################################
    #convert kcal/mol to J/mol, 1 kcal/mol equals 4184 J/mol\n"
    A_term = float(-(dG))*float(4184)
    # RT*ln10, where R is 8.314 J/mol*K units and T is 298.15 Kelvins
    B_term = float(8.314)*float(298.15)*float(math.log(10))
    logP = A_term/B_term
    return logP


# Read experimental data.
with open(EXPERIMENTAL_DATA_FILE_PATH, 'r') as f:
    # experimental_data = pd.read_json(f, orient='index')
    names = ('Molecule ID', 'logP mean', 'logP SEM',
             'Assay Type', 'Experimental ID', 'Isomeric SMILES')
    experimental_data = pd.read_csv(f, names=names, skiprows=1)

# Convert numeric values to dtype float.
for col in experimental_data.columns[1:7]:
    experimental_data[col] = pd.to_numeric(experimental_data[col], errors='coerce')
