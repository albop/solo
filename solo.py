#!/usr/bin/python

import argparse

from yaml_import import yaml_import

parser = argparse.ArgumentParser(description='Matlab compiler')
parser.add_argument('-r','--print_residuals', action='store_const', const=True, default=False, help='print residuals at the steady-state')
parser.add_argument('input_file', help='model file')
#
args = parser.parse_args()
input_file = args.input_file

output_rad = input_file.strip('.yaml') + '_model'
output_file = output_rad + '.m'



smodel = yaml_import(input_file)


# check steady-state
if args.print_residuals:
    from model import print_residuals
    print_residuals(smodel)


from compiler_matlab import CompilerMatlab
comp = CompilerMatlab(smodel)

txt = comp.process_output()

solution_order = None
txt = comp.process_output( solution_order=solution_order, fname=output_rad)

######

with file(output_file,'w') as f:
    f.write(txt)