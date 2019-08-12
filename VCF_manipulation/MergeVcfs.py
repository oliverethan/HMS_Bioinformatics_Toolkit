# Ethan Oliver
# Harvard Medical School
# Department of Biomedical Informatics
# Park Lab
# 2019

import gzip
import argparse
import os
import re
import ntpath
import glob
import sys

def parse_args():
    """Uses argparse to enable user to customize script functionality"""
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-A', '--input_1', help='path to file containing input A')
    parser.add_argument('-B', '--input_2', help='path to file containing input B')
    parser.add_argument('-out', '--output_file', help='file to which the outputs will be written to')
    parser.add_argument('-n', '--num_cores', default='1', help='slurm job submission option')
    parser.add_argument('-t', '--runtime', default='0-11:00:00', help='slurm job submission option')
    parser.add_argument('-p', '--queue', default='short', help='slurm job submission option')
    parser.add_argument('--mem_per_cpu', default='10G', help='slurm job submission option')
    parser.add_argument('--mail_type', default='ALL', help='slurm job submission option')
    parser.add_argument('--mail_user', default='<EMAIL>', help='slurm job submission option')
    parser.add_argument('-picard', '--picard_path', default='/n/data1/hms/dbmi/park/alon/software/picard.jar', help='path to software')
    parser.add_argument('-library', '--library_name', default='lib_name', help='name of the library the sample was prepared with')
    return parser.parse_args()

def clean_arg_paths(args):
    """Modifies all user-inputted directory paths such that they end with a '/'"""
    d = vars(args)
    for arg in d.keys():   
        if 'directory' in arg and d[arg] is not None and d[arg][-1] != '/': d[arg] += '/'


def return_slurm_command(args):
    """Returns slurm command given args provided"""
    slurm_command = '#!/bin/bash\n' + \
                '#SBATCH -n ' + args.num_cores + '\n' + \
                '#SBATCH -t ' + args.runtime + '\n' + \
                '#SBATCH -p ' + args.queue + '\n' + \
                '#SBATCH --mem-per-cpu=' + args.mem_per_cpu + '\n' + \
                '#SBATCH --mail-type=' + args.mail_type + '\n' + \
                '#SBATCH --mail-user=' + args.mail_user + '\n'
    if args.queue in ['park', 'priopark']:
        slurm_command += '#SBATCH --account=park_contrib' + '\n'
    return slurm_command

def gen_output_file_name(args):
    return args.output_file

def return_primary_command(args, output_file_name):
    primary_command = 'java' + ' -jar ' + args.picard_path + ' MergeVcfs' ' \\' + '\n' + \
    '\t' + 'I=' + args.input_1 + ' \\' + '\n' + \
    '\t' + 'I=' + args.input_2 + ' \\' + '\n' + \
    '\t' + 'O=' + output_file_name 
    return primary_command

def gen_sh_file_name(args, output_file_name):
    """Generates sh file name"""
    sh_file_name = os.path.dirname(output_file_name) + '/.sh/' + os.path.basename(output_file_name) + '.sh'
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

def main():
    args = parse_args()
    clean_arg_paths(args)

    slurm_command = return_slurm_command(args)
    output_file_name = gen_output_file_name(args)
    primary_command = return_primary_command(args, output_file_name)

    sh_file_name = gen_sh_file_name(args, output_file_name)
    write_out(args, slurm_command, primary_command, sh_file_name)

    submit_job(sh_file_name)

if __name__ == "__main__":
    main()
