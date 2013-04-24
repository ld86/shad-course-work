#!/opt/local/bin/python3.2
#_*_ coding: utf-8 _*_

import os
import argparse 
import names_grep as ngrep

def get_fb2_files_from_dir(dir_path):
    #TODO:recursive traverse of directory
    if not dir_path.endswith('/'):
        dir_path.append('/')
    return [dir_path + name for name in os.listdir(dir_path) if name.lower().endswith('.fb2') \
            or name.lower().endswith('.fb2.xml')]

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', type = str, metavar = 'directory', default='corpus/')
    parser.add_argument('-f', type = str, metavar = 'filename', nargs = '*', default = list())
    return parser.parse_args()

def prepare_csv_file_with_heroes(file_name):
    fd = open(file_name, 'r')
    text = fd.read()
    fd.close()
    parser = ngrep.FB2_parser(text)
    name_calc = ngrep.Names_calculator(parser.get_text())
    fd = open(file_name + ".txt", 'w')
    fd.write(parser.get_text())
    fd.close()
    names = name_calc.names_lemmas.values()
    fd = open(file_name + '.names', 'w')
    for name in names:
        fd.write(';'.join([name.name, str(name.count), str(name.start), str(name.finish)]) + "\r\n")
    fd.close()


def main():
    args = parse_args()
    v = vars(args)
    directory_name = args.d
    file_names = args.f
    file_names += get_fb2_files_from_dir(directory_name)
    for f in file_names:
        prepare_csv_file_with_heroes(f)

if __name__ == "__main__":
    main();
