import os

from enrichwrap import enrich, add_mapping


def get_variables_for_execute(sas_data):
    retval = []
    for key in sas_data.keys():
        inner = ['                  in_out ']
        val = sas_data[key]
        if isinstance(val, float) or isinstance(val, int):
            inner.append('double ')
        elif isinstance(val, str):
            inner.append('varchar ')
        else:
            # Tackle else other types
            print('what to print')
        inner.append(key)
        inner.append(',')
        retval.append(''.join(inner))

    return retval

def is_numeric(val):
    if isinstance(val, float) or isinstance(val, int):
        return True
    return False

def get_variables_for_initialization(sas_data):
    retval = []
    for key in sas_data.keys():
        val = sas_data[key]
        inner = ['       ']
        inner.append(key)
        inner.append(' = ')
        if is_numeric(val):
            inner.append('0;')
        elif isinstance(val, str):
            inner.append('None;')
        else:
            # Tackle else other types
            print('check this')
        retval.append(''.join(inner))

    return retval

#             rc = py.appendSrcLine('   "Output: outcome,full,_6_previouslyusedpi,_6_nodelaytoinputpi,_6_fluidtypingpi,_6_consistentip,_6_consistentdevice" ');
def get_inner_python_output_line(sas_data):
    retval = []
    if len(sas_data.keys()) == 0:
        return ''.join(retval)

    # Bail out if there are too many keys, as it will blow out the 32767 character limit for ID DS2
    if len(sas_data.keys()) > 100:
        retval.append('             rc = py.appendSrcLine(\'   "Output: outcome,full')
    else:
        for key in sas_data.keys():
            if len(retval) == 0:
                retval.append('             rc = py.appendSrcLine(\'   "Output: outcome,full,')
            else:
                retval.append(',')
            retval.append(key)

    retval.append('" \');')
    return ''.join(retval)


def get_inner_python_init_variables(sas_data):
    retval = []
    # Bail out if there are too many keys, as it will blow out the 32767 character limit for ID DS2
    if len(sas_data.keys()) > 100:
        return ''

    for key in sas_data.keys():
        val = sas_data[key]
        inner = ['             rc = py.appendSrcLine(\'   ']
        inner.append(key)
        if is_numeric(val):
            inner.append(' = 0\');')
        else:
            inner.append(' = None\');')

        retval.append(''.join(inner))

    return retval

def get_assignment_from_sasdata(sas_data):
    # Bail out if there are too many keys, as it will blow out the 32767 character limit for ID DS2
    if len(sas_data.keys()) == 0 or len(sas_data.keys()) > 100:
        return ''

    retval = ['             rc = py.appendSrcLine(\'   if len(vendor_response.keys()) > 0:\');']
    for key in sas_data.keys():
        inner = ['             rc = py.appendSrcLine(\'      ']
        inner.append(key)
        inner.append(' = ')
        inner.append('sas_data["')
        inner.append(key)
        inner.append('"]\');')
        retval.append(''.join(inner))

    return retval

def get_predefined_enrichment():
    return ['biocatch', 'giact', 'socure', 'payfoneverify', 'payfonetrust', 'bokugpir', 'bokumaa', 'datavisor',
            'giact', 'iovation']

def get_mappings_and_call_enrich(tool, mapping_in):
    retval = ''
    if tool in get_predefined_enrichment():
        str1 = '             rc = py.appendSrcLine(\'   mappings = enrichwrap.get_' + tool + '_mappings()\');'
        str2 = '             rc = py.appendSrcLine(\'   val = enrichwrap.enrich("' + tool + '", sample_data, None, target_url, target_port, None, mappings)\');'
        retval = '\n'.join([str1, str2])
    elif mapping_in is not None:
        inner =     ['             rc = py.appendSrcLine(\'   if mapping_in is not None:\');']
        inner.append('             rc = py.appendSrcLine(\'      mappings = enrichwrap.add_mapping_in_str(mapping_in, mapping_out, custom_target, False)\');')
        inner.append('             rc = py.appendSrcLine(\'   else:\');')
        inner.append('             rc = py.appendSrcLine(\'      mappings = None\');')
        inner.append('             rc = py.appendSrcLine(\'   val = enrichwrap.enrich(custom_target, sample_data, None, target_url, target_port, targets, mappings)\');')
        retval = '\n'.join(inner)
    else:
        str1 = '             rc = py.appendSrcLine(\'   mappings = None\');'
        str2 = '             rc = py.appendSrcLine(\'   val = enrichwrap.enrich(None, sample_data, None, target_url, target_port, None, mappings)\');'
        retval = '\n'.join([str1, str2])

    return retval

def get_check_if_keys_is_populated(tool):
    if tool in get_predefined_enrichment():
        str1 = '             rc = py.appendSrcLine(\'   if "' + tool + '" in vendor_response.keys():\');'
        str2 = '             rc = py.appendSrcLine(\'      outcome = vendor_response["' + tool + '"]["result"]\');'
    else:
        str1 = '             rc = py.appendSrcLine(\'   if len(vendor_response.keys()) == 0:\');'
        str2 = '             rc = py.appendSrcLine(\'      outcome = "intedetermined"\');'

    return '\n'.join([str1, str2])

def get_return_line(sas_data):
    # Bail out if there are too many keys, as it will blow out the 32767 character limit for ID DS2
    if len(sas_data.keys()) > 100:
        return '             rc = py.appendSrcLine(\'   return outcome,full\');'

    retval = ['             rc = py.appendSrcLine(\'   return outcome,full,']
    inner = []
    for key in sas_data.keys():
        if len(inner) > 0:
            inner.append(',')
        inner.append(key)
    retval.append(''.join(inner))
    retval.append('\');')
    return ''.join(retval)

def get_py_str(key, matching_val):
    inner = ['       ']
    inner.append(key)
    inner.append(' = py.get')
    if is_numeric(matching_val):
        inner.append('Double')
    else:
        inner.append('String')
    inner.append('(\'')
    inner.append(key)
    inner.append('\');')
    return ''.join(inner)

def get_space_num(sas_data):
    maxstrlen = 0
    for key in sas_data.keys():
        thislen = len(get_py_str(key, sas_data[key]))
        maxstrlen = max(thislen, maxstrlen)
    maxstrlen += 10
    return maxstrlen

def get_end_variables(sas_data):
    retval = []
    maxstrlen = get_space_num(sas_data)

    # Bail out if there are too many keys, as it will blow out the 32767 character limit for ID DS2
    if len(sas_data.keys()) <= 100:
        for key in sas_data.keys():
            str1 = get_py_str(key, sas_data[key])
            spacenum = maxstrlen - len(str1)
            inner = [str1]
            for _ in range(spacenum):
                inner.append(' ')

            inner.append('if rc then return;')
            retval.append(''.join(inner))

    str2 = '       val = py.getString(\'outcome\');'
    str_outcome = [str2]
    spacenum = maxstrlen - len(str2)
    for _ in range(spacenum):
        str_outcome.append(' ')
    str_outcome.append('if rc then return;')
    retval.append(''.join(str_outcome))

    str3 = '       res_json = py.getString(\'full\');'
    str_res_json = [str3]
    spacenum = maxstrlen - len(str3)
    for _ in range(spacenum):
        str_res_json.append(' ')
    str_res_json.append('if rc then return;')
    retval.append(''.join(str_res_json))

    return retval


def gen_ds2_structure(tool, mappings, sample_data=None, targets=None, mappings_in=None, mappings_out=None, write_to=None):
    if write_to is not None and os.path.isdir(write_to):
        IDFiles = write_to + os.path.sep
    else:
        starting_dir = os.path.dirname(__file__)
        IDFiles = starting_dir + os.path.sep + '..' + os.path.sep + 'ID_modules' + os.path.sep + 'ds2' + os.path.sep

    print('Content for structure will go here [%s]' % IDFiles)
    #list_samples = glob.glob(IDFiles + '*.*')

    bench = None
    filename = IDFiles + 'bench_' + tool + '.txt'
    if os.path.isfile(filename):
        bench_file = open(filename, 'r')
        bench = bench_file.read()
        bench_file.close()

    if mappings is not None:
        outgoing_data = enrich(tool, sample_data, None, '10.44.16.24', '8200', None, mappings)
    else:
        created_mappings = add_mapping(mappings_in, mappings_out, tool, False)
        outgoing_data = enrich(tool, sample_data, None, '10.44.16.24', '8200', targets, created_mappings)

    sas_data = outgoing_data['sas_data']

    id_content = ['package "${PACKAGE_NAME}" /inline;',
                  '   dcl package pymas py;',
                  '   dcl double revision;',
                  '   method execute(',
                  '                  varchar(32767) url,',
                  '                  varchar port,',
                  '                  varchar(32767) pycode,',
                  '                  in_out varchar RETVAL,',
                  '                  in_out varchar val,',
                  '                  in_out double rc,',
                  ]
    id_content.extend(get_variables_for_execute(sas_data))
    id_content.append('                  in_out varchar(32767) res_json);',)
    id_content.append('')
    id_content.extend(get_variables_for_initialization(sas_data))
    id_content.append('       res_json = \'\';')
    id_content.append('')
    id_content.append('       if null(py) then do;')
    id_content.append('          py = _new_ pymas();')
    id_content.append('          rc = py.useModule(\'enrichshim\', 1);')
    id_content.append('          if rc then do;')
    id_content.append('             rc = py.appendSrcLine(\'import enrichwrap\');')
    id_content.append('             rc = py.appendSrcLine(\'import json\');')
    id_content.append('             rc = py.appendSrcLine(\'\');')
    id_content.append('             rc = py.appendSrcLine(\'def get_steps(s):\');')
    id_content.append('             rc = py.appendSrcLine(\'   "Output: r" \');')
    id_content.append('             rc = py.appendSrcLine(\'   r = enrichwrap.get_steps(s)\');')
    id_content.append('             rc = py.appendSrcLine(\'   return str(r)\');')
    id_content.append('             rc = py.appendSrcLine(\'\');')
    id_content.append('             rc = py.appendSrcLine(\'def enrich(in_data, target_url, target_port, custom_target=None, custom_body=None, mapping_in=None, mapping_out=None):\');')
    id_content.append(get_inner_python_output_line(sas_data))
    id_content.append('             rc = py.appendSrcLine(\'   sample_data = in_data\');')
    id_content.append('             rc = py.appendSrcLine(\'   if custom_target is not None and custom_body is not None:\');')
    id_content.append('             rc = py.appendSrcLine(\'      targets = enrichwrap.add_target_with_map_str(custom_target, custom_body)\');')
    id_content.append('             rc = py.appendSrcLine(\'   else:\');')
    id_content.append('             rc = py.appendSrcLine(\'      targets = None\');')
    id_content.append('             rc = py.appendSrcLine(\'   outcome = None\');')
    id_content.extend(get_inner_python_init_variables(sas_data))
    id_content.append(get_mappings_and_call_enrich(tool, mappings_in))
    id_content.append('             rc = py.appendSrcLine(\'   sas_data = val["sas_data"]\');')
    id_content.append('             rc = py.appendSrcLine(\'   vendor_response = val["vendor_response"]\');')
    id_content.append(get_check_if_keys_is_populated(tool))
    id_content.extend(get_assignment_from_sasdata(sas_data))
    id_content.append('             rc = py.appendSrcLine(\'   full = json.dumps(sas_data)\');')
    id_content.append(get_return_line(sas_data))
    id_content.append('             pycode = py.getSource();')
    id_content.append('             revision = py.publish(pycode, \'enrichshim\');')
    id_content.append('             if revision lt 1 then do;')
    id_content.append('                rc = -1;')
    id_content.append('                RETVAL = \'problem in usemodule\';')
    id_content.append('                return;')
    id_content.append('             end; /* End of if revision lt 1 */')
    id_content.append('          end; /* End of if useModule failed */')
    id_content.append('')
    id_content.append('          rc = py.useMethod(\'enrich\');')
    id_content.append('          if rc then return;')
    id_content.append('       end; /* end of if null(py) */')
    id_content.append('')
    id_content.append('       sample_in = \'{"UniqueId": 23456, "username": "John Q Public"}\';')
    id_content.append('')
    id_content.append('       py.setString(\'in_data\', sample_in);')
    id_content.append('       py.setString(\'target_url\', \'10.44.16.24\');')
    if tool not in get_predefined_enrichment():
        id_content.append('       py.setString(\'target_port\', \'8400\');')
    else:
        id_content.append('       py.setString(\'target_port\', \'8200\');')
    id_content.append('       py.setString(\'custom_target\', \'' + tool + '\');')
    if tool not in get_predefined_enrichment():
        id_content.append('       py.setString(\'custom_body\', \'{"url": "http://10.44.16.24:8400/custom_site/items", "mechanism": "GET", "params": {"name": "John", "age": 22}}\');')
        id_content.append('       py.setString(\'mapping_in\', \'{"UniqueId": "uniqueId", "username": "user_name"}\');')
        id_content.append('       py.setString(\'mapping_out\', \'{"_a_score": "score", "_a_confidence": "confidence", "_a_reference": "reference"}\');')
    id_content.append('       rc = py.execute();')
    id_content.extend(get_end_variables(sas_data))
    id_content.append('   end;')
    id_content.append('endpackage;')
    id_content.append('')

    if bench is None:
        bench_file = open(filename, 'w')
        bench = '\n'.join(id_content)
        bench_file.write(bench)
        bench_file.close()
    elif bench != id_content:
        compare_file = open(IDFiles + 'compare_' + tool + '.txt', 'w')
        strcontent = '\n'.join(id_content)
        compare_file.write(strcontent)
        compare_file.close()

    return bench, '\n'.join(id_content)


