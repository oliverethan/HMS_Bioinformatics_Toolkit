# Ethan Oliver
# Harvard Medical School
# Department of Biomedical Informatics
# Park Lab
# 2019

import argparse
import os
import re
import ntpath
import glob
import sys
from time import sleep

def parse_args():
    """Uses argparse to enable user to customize script functionality"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-in_dir', '--input_directory', help='path to input files')
    parser.add_argument('-out', '--output', help='File to which the output will be written to')
    parser.add_argument('-n', '--num_cores', default='1', help='slurm job submission option')
    parser.add_argument('-t', '--runtime', default='4-23:59:59', help='slurm job submission option')
    parser.add_argument('-p', '--queue', default='park', help='slurm job submission option')
    parser.add_argument('--mem_per_cpu', default='20G', help='slurm job submission option')
    parser.add_argument('--mail_type', default='ALL', help='slurm job submission option')
    parser.add_argument('--mail_user', default='ethan.oliver@tufts.edu', help='slurm job submission option')
    parser.add_argument('-gatk', '--gatk_path', default='gatk', help='path to software')
    return parser.parse_args()

def clean_arg_paths(args):
    """Modifies all user-inputted directory paths such that they end with a '/'"""
    d = vars(args)
    for arg in d.keys():
        if 'output' in arg and d[arg]=='./': d[arg] = os.getcwd()
        if 'directory' in arg and d[arg] is not None and d[arg][-1] != '/': d[arg] += '/'

def gen_output_file_name(args):
    output_file_name = args.output
    return output_file_name


def return_slurm_command(args):
    """Returns slurm command given args provided"""
    slurm_command = '#!/bin/bash\n' + \
                '#SBATCH -J ' + "CreatePON" + '\n' + \
                '#SBATCH -n ' + args.num_cores + '\n' + \
                '#SBATCH -t ' + args.runtime + '\n' + \
                '#SBATCH -p ' + args.queue + '\n' + \
                '#SBATCH --mem-per-cpu=' + args.mem_per_cpu + '\n' + \
                '#SBATCH --mail-type=' + args.mail_type + '\n' + \
                '#SBATCH --mail-user=' + args.mail_user + '\n'
    if args.queue in ['park', 'priopark']:
        slurm_command += '#SBATCH --account=park_contrib' + '\n'
    return slurm_command


def return_primary_command(args, argfile, output_file_name):
    primary_command = args.gatk_path +' CreateSomaticPanelOfNormals' + ' \\' + '\n' + \
     '\t' + '-vcfs ' + argfile  + ' \\' + '\n' + \
     '\t' + '-O ' + output_file_name
    return primary_command




def gen_sh_file_name(args, output_file_name):
    """Generates sh file name"""
    sh_file_name = os.path.dirname(output_file_name) + '/' + os.path.basename(output_file_name) + '.sh'
    return sh_file_name

def write_out(args, slurm_command, primary_command, sh_file_name):
    """"""
    os.makedirs(os.path.dirname(sh_file_name), exist_ok=True)
    with open(sh_file_name, 'w') as file:
        file.write(slurm_command + primary_command)

def submit_job(sh_file_name):
    os.chdir(os.path.dirname(sh_file_name))
    os.system('chmod +x ' + os.path.basename(sh_file_name))
    os.system('sbatch ./' + os.path.basename(sh_file_name))


def return_input_files(args, ext):
    input_vcfs = [file for file in glob.glob(args.input_directory + '*.' + ext)]
    return input_vcfs

def gen_args_file(args , output_file_name):
    input_vcfs = return_input_files(args, 'vcf')
    print('input_vcfs\n')
    print(input_vcfs)
    argfile = os.path.dirname(output_file_name) + '/' + os.path.basename(output_file_name) + '.args'
    os.makedirs(os.path.dirname(argfile), exist_ok=True)
    with open( argfile, 'w') as file:
        for input_file in input_vcfs:
            file.write("%s\n" % input_file)
    return argfile


def main():
    args = parse_args()
    clean_arg_paths(args)
    slurm_command = return_slurm_command(args)
    output_file_name = gen_output_file_name(args)
    print('Outfile: ', output_file_name)
    argfile = gen_args_file(args, output_file_name)
    print('Argfile: ', argfile)

    primary_command = return_primary_command(args, argfile, output_file_name)

    sh_file_name = gen_sh_file_name(args, output_file_name)
    write_out(args, slurm_command, primary_command, sh_file_name)

    submit_job(sh_file_name)

if __name__ == "__main__":
    main()



    























