import json
import os

def create_data_and_clean():
    data = {}
    if os.path.isfile('dealernet.json'):
        with open('dealernet.json') as json_file:
            data['dealernet'] = json.load(json_file)
    else:
        data['dealernet'] = None

    if os.path.isfile('experian.json'):
        with open('experian.json') as json_file:
            data['experian'] = json.load(json_file)
    else:
        data['experian'] = None

    if os.path.isfile('equifax.json'):
        with open('equifax.json') as json_file:
            data['equifax'] = json.load(json_file)
    else:
        data['equifax'] = None

    # Delete the files 'dealernet.json', 'experian.json', and 'equifax.json'.
    if os.path.isfile('dealernet.json'):
        os.remove('dealernet.json')
    if os.path.isfile('experian.json'):
        os.remove('experian.json')
    if os.path.isfile('equifax.json'):
        os.remove('equifax.json')

    return data

def merge_dicts_with_values(values_dict, nulls_dict):
    for key, value in values_dict.items():
        if isinstance(value, dict) and key in nulls_dict:
            nulls_dict[key] = merge_dicts_with_values(value, nulls_dict[key])
        else:   
            nulls_dict[key] = value
    return nulls_dict

def fill_empty_data(data):

    # Read the file 'null_data.json'
    with open('empty_data.json') as json_file:
        dict_with_nulls = json.load(json_file)

    # Fill the missing values in the dictionary with nulls
    new_dict = merge_dicts_with_values(data, dict_with_nulls)
    
    return new_dict

def validar_rut(rut):
    if "-" not in rut:
        return False

    rut = rut.replace(".", "").upper()
    if len(rut) < 3:
        return False

    # Eliminamos el guion
    rut = rut.replace("-", "")

    try:
        rut = int(rut)
    except ValueError:
        return False

    return True

if __name__ == "__main__":

    # Read 'example_data.json'
    with open('example_data.json') as json_file:
        data = json.load(json_file)

    # Run Flask app
    output = fill_empty_data(data)

    # Write the output to 'new_data.json'
    with open('new_data.json', 'w') as outfile:
        json.dump(output, outfile, indent=4)
