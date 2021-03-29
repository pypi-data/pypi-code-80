import linecache, os, sys

def get_val():
    """ Extracts control parameters from pople.inp """
    current_dir_path = os.getcwd()

    input_file = current_dir_path + "/pople.inp"

    inp_par = ["openmpi_dir","orca_dir","install_dir","maxcore_mb","nproc","method_opt_freq", "basis_opt_freq", "custombasis_opt_freq", "String_Opt", "MGGA", "FROZEN_GEOM", "method_ccsdt", \
               "basis_ccsdt", "custombasis_ccsdt", "DLPNO_CCSDT", "method_mp2_s", "basis_mp2_s", "custombasis_mp2_s", "method_mp2", "basis_mp2", "custombasis_mp2", "flag_RIMP2", \
               "flag_DLPNOMP2", "method_hf3", "basis_hf3", "custombasis_hf3", "method_hf4", "basis_hf4", "custombasis_hf4", "scalfac", "calc_IP", "verticalIP", "calc_EA", \
               "verticalEA", "calc_PA", "calc_AE", "calc_BE", "calc_HF", "conv_scf", "HLCeqZERO", "SOSCF", "SCFDIIS", "SO_3rdrow_mols", "LSHIFT", "optdiis", "HF_CBS_default", \
               "HF_CBS_orca_23_def2",  "HF_CBS_orca_34_def2", "HF_CBS_orca_23_cc", "HF_CBS_orca_34_cc", "restart_cc", "restart_mp2", "restart_hf3", "restart_hf4",  \
               "switch_RIMP2_small", "switch_read_RIMP2_small", "AA", "BB", "CC", "DD" , "EE", "ApAp", "method_type", "job_type"]
    val = {}

    with open(input_file,"r") as ini_inp:
        for line in ini_inp:
            if not line.startswith("#"):
                if "=" in line:
                    val_line = line.split("=")
                    val_key = val_line[0].strip()
                    if val_key.strip() in inp_par:
                        if "#" in val_line[1]: ### CHECK!!!!!!
                            val_split = val_line[1].split("#")   ## this condition is to make sure if some comments are added to the input line, the comment (that follows # ) is ignored
                            if ( val_split[0].strip() == "True" ) or (val_split[0].strip() == "TRUE") or (val_split[0].strip() == "T") or (val_split[0].strip() == ".true." ) or (val_split[0].strip() == "t"):
                                 val[val_key] = "true"
                            elif ( val_split[0].strip() == "False" ) or (val_split[0].strip() == "FALSE") or (val_split[0].strip() == "F") or (val_split[0].strip() == ".false.") or (val_split[0].strip() == "t"):
                                val[val_key] = "false"
                            else:
                                 val[val_key] = val_split[0].strip()
                        else:
                           if ( val_line[1].strip() == "True" ) or ( val_line[1].strip() == "TRUE") or ( val_line[1].strip() == "T") or ( val_line[1].strip() == ".true.") or ( val_line[1].strip() == "t"):
                                val[val_key] = "true"
                           elif ( val_line[1].strip() == "False" ) or (val_line[1].strip() == "FALSE") or (val_line[1].strip() == "F") or (val_line[1].strip() == ".false.") or (val_line[1].strip() == "f"):
                               val[val_key] = "false"
                           else:
                                val[val_key] = val_line[1].strip()


                    else: 
                
                        print("Keyword not in the list of parameters, please check for typos")
                        print("List of valid keywords are:")
                        for l in range(len(inp_par)):
                            print(inp_par[l])

    return(val)



