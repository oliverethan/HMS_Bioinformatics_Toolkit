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
    parser.add_argument('-tumor', '--input_tumor_path', help='path to input tumor file')
    parser.add_argument('-normal', '--input_normal_path', help='path to normal file')
    parser.add_argument('-normal', '--input_normal_path', help='path to normal file')
    parser.add_argument('-out', '--output_name', help='file to which the output will be written to')
    parser.add_argument('-n', '--num_cores', default='1', help='slurm job submission option')
    parser.add_argument('-t', '--runtime', default='10-0:00:00', help='slurm job submission option')
    parser.add_argument('-p', '--queue', default='priopark', help='slurm job submission option')
    parser.add_argument('--mem_per_cpu', default='20G', help='slurm job submission option')
    parser.add_argument('--mail_type', default='FAIL', help='slurm job submission option')
    parser.add_argument('--mail_user', default='<EMAIL>', help='slurm job submission option')
    parser.add_argument('-reference', '--reference_path', default='/n/data1/hms/dbmi/park/jake/Resources/03_pcawg_ref/genome.fa', help='path to reference_path file')
    parser.add_argument('-w', '--wiggle_path', help='path to wiggle file')
    return parser.parse_args()

def clean_arg_paths(args):
    """Modifies all user-inputted directory paths such that they end with a '/'"""
    d = vars(args)
    for arg in d.keys():
        if 'output_directory' in arg and d[arg]=='./': d[arg] = os.getcwd() + '/.' + ntpath.basename(args.input_tumor_path) + '_v_' + ntpath.basename(args.input_normal_path)
        if 'directory' in arg and d[arg] is not None and d[arg][-1] != '/': d[arg] += '/'

def return_slurm_command(args):
    """Returns slurm command given args provided"""
    slurm_command = '#!/bin/bash\n' + \
                '#SBATCH -J ' + "SEQUENZA" + '\n' + \
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
    output_file_name = args.output_name  
    return output_file_name

def return_primary_command(args, output_file_name):
    primary_command = 'sequenza-utils bam2seqz ' + ' \\' + '\n' + \
     '\t' + '-F ' + args.reference_path + ' \\' + '\n' + \
     '\t' + '-n ' + args.input_tumor_path  + ' \\' + '\n' + \
     '\t' + '-t ' + args.input_normal_path + ' \\' + '\n' + \
     '\t' + '-gc ' + args.wiggle_path  + ' \\' + '\n' + \
     '\t' + '-o ' + output_file_name
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
