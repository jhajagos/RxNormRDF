__author__ = 'Janos G. Hajagos'

import json
import logging
import zipfile as zf
import os

import glob

def extract_zip_file(file_name, directory=None):
    """"Extract a zipfile into a directory"""
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


def main():
    get_file_from_the_web(None)

    if not os.path.exists("../extract/temp/"):
        extract_zip_file("../extract/RxNorm_full_prescribe_03042013.zip", directory="../extract/temp/")

    file_layout_dict = read_file_layout()
    import pprint
    pprint.pprint(file_layout_dict)



if __name__ == "__main__":
    main()
