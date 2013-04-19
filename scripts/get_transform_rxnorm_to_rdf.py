__author__ = 'Janos G. Hajagos'

import json
import logging
import zipfile as zf
import os
import pprint


class RRFReader(object):
    def __init__(self, file_name, column_position, delimiter = "|"):
        self.delimiter = delimiter
        self.file_name = file_name
        self.column_position = column_position

        try:
            self.fp = open(file_name, 'r')
        except IOError:
            logging.error("Cannot open '%s'", os.path.abspath(file_name))
            raise

    def __iter__(self):
        return self

    def next(self):

        try:
            line = self.fp.next()
            split_line = line.rstrip().split(self.delimiter)
            rrf_dictionary = {}
            i = 0

            for cell_value in split_line[:-1]:
                if len(cell_value) == 0:
                    cell_value = None

                rrf_dictionary[self.column_position[i]] = cell_value

                i += 1

            return rrf_dictionary

        except StopIteration:
            raise StopIteration


def extract_zip_file(file_name, directory=None):
    """Extract a zipfile into a directory"""
    full_path_to_file = os.path.abspath(file_name)
    try:
        zip_file_obj = zf.ZipFile(full_path_to_file, "r")
    except IOError:
        logging.error("Could not open file '%s'" % full_path_to_file)
        raise

    try:
        zip_file_obj.extractall(directory)
    except IOError:
        logging.error("Could not extract zip file '%s'" % full_path_to_file)

    return True

def get_file_from_the_web(url):
    pass


def clean_temp_directory():
    pass
    # files_to_remove = glob.glob("../temp/")
    # for file_to_remove in files_to_remove:
    #     if os.path.isfile(file_to_remove):
    #         os.remove(file_to_remove)
    #     elif os.path.isdir(file_to_remove):
    #         os.rmdir(file_to_remove)


def read_file_layout():
    fj = open("rxnorm_file_layout.json", "r")
    file_layout_json = json.load(fj)

    file_layout_json_cleaned = {}

    for file_name in file_layout_json:
        file_index_dict = {}
        for string_number in file_layout_json[file_name]:
            file_index_dict[int(string_number)] = file_layout_json[file_name][string_number]
        file_layout_json_cleaned[file_name] = file_index_dict

    return file_layout_json_cleaned


def initialize_or_increment(dict, key):
    if key in dict:
        dict[key] += 1
    else:
        dict[key] = 1
    return dict


def main():
    get_file_from_the_web(None)
    temp_directory = "../extract/temp/"
    if not os.path.exists("../extract/temp/"):
        extract_zip_file("../extract/RxNorm_full_prescribe_03042013.zip", directory=temp_directory)

    file_layout_dict = read_file_layout()

    temp_rrf_directory = os.path.join(temp_directory, "rrf")
    rxnconso_file_name = "RXNCONSO.RRF"
    rxnconso_file_path = os.path.join(temp_rrf_directory, rxnconso_file_name)

    rxnconso_reader = RRFReader(rxnconso_file_path, file_layout_dict[rxnconso_file_name])

    sab_dict = {}
    rxcui_dict = {}
    tty_dict = {}
    i = 0
    for rxaui_info in rxnconso_reader:
        rxcui = rxaui_info["rxcui"] # RXCUI = concept unique identifier
        rxaui = rxaui_info["rxaui"] # RXAUI = atomic unique identifier
        sab = rxaui_info["sab"] # SAB = source vocabulary source
        code = rxaui_info["code"] # code if applicable
        tty = rxaui_info["tty"] # TTY = Term type

        if rxcui in rxcui_dict:
            rxcui_dict[rxcui] += [rxaui]
        else:
            rxcui_dict[rxcui] = [rxaui]

        sab_dict = initialize_or_increment(sab_dict, sab)
        tty_dict = initialize_or_increment(tty_dict, tty)

        i += 1

    print("Number of RXAUIs is %s" % i)
    print("Number of RXCUIs is %s" % len(rxcui_dict.keys()))
    print("Counts of SAB (source vocabularies)")
    pprint.pprint(sab_dict)
    print("Counts of TTY (term types)")
    pprint.pprint(tty_dict)

    rxnrel_file_name = "RXNREL.RRF"
    rxnrel_file_path = os.path.join(temp_rrf_directory, rxnrel_file_name)
    rxnrel_reader = RRFReader(rxnrel_file_path, file_layout_dict[rxnrel_file_name])

    i = 0
    rela_dict = {}
    rel_dict = {}

    for rxnrel in rxnrel_reader:
        rela = rxnrel["rela"]
        rel = rxnrel["rel"]

        if rela:
            initialize_or_increment(rela_dict, rela)
        if rel:
            initialize_or_increment(rel_dict, rel)
        i += 1

    print("Number of relations in the file is %s" % i)
    pprint.pprint(rela_dict)

    print("Count of rel (simple relationships)")
    pprint.pprint(rel_dict)

    rxnsat_file_name = "RXNSAT.RRF" # attribute file
    rxnsat_file_path = os.path.join(temp_rrf_directory, rxnsat_file_name)
    rxnsat_reader = RRFReader(rxnsat_file_path, file_layout_dict[rxnsat_file_name])

    i = 0
    atn_dict = {}
    for rxnsat in rxnsat_reader:
        if "atn" in rxnsat:
            atn = rxnsat["atn"]
            initialize_or_increment(atn_dict, atn)
        i += 1

    print("Number of attributes in file is %s" % i)
    pprint.pprint(atn_dict)

    clean_temp_directory()




if __name__ == "__main__":
    main()
