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

def parse_args():
    """Uses argparse to enable user to customize script functionality"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-in_dir', '--input_directory', help='path to input files')
    parser.add_argument('-in_file', '--input_file_path', help='path to input file')
    parser.add_argument('-out', '--output_directory', default='./', help='directory to which output will be written')
    parser.add_argument('-n', '--num_cores', default='1', help='slurm job submission option')
    parser.add_argument('-t', '--runtime', default='1-00:00:00', help='slurm job submission option')
    parser.add_argument('-p', '--queue', default='park', help='slurm job submission option')
    parser.add_argument('--mem_per_cpu', default='8G', help='slurm job submission option')
    parser.add_argument('--mail_type', default='ALL', help='slurm job submission option')
    parser.add_argument('--mail_user', default='ethan.oliver@tufts.edu', help='slurm job submission option')
    parser.add_argument('-gatk', '--gatk_path', default='gatk', help='path to software')
    return parser.parse_args()

def clean_arg_paths(args):
    """Modifies all user-inputted directory paths such that they end with a '/'"""
    d = vars(args)
    for arg in d.keys():
        if 'output_directory' in arg and d[arg]=='./': d[arg] = os.getcwd()    
        if 'directory' in arg and d[arg] is not None and d[arg][-1] != '/': d[arg] += '/'

def return_input_files(args, ext):
    input_bams = [file for file in glob.glob(args.input_directory + '*.' + ext)]
    return input_bams

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

def gen_output_file_name(args, input_file):
    output_file_name = args.output_directory + re.sub('\.vcf.*', '', ntpath.basename(input_file)) + '_filtered.vcf.gz'
    return output_file_name

def return_primary_command(args, output_file_name, input_file):
    primary_command = args.gatk_path +' FilterMutectCalls' + ' \\' + '\n' + \
     '\t' + '-V ' + input_file  + ' \\' + '\n' + \
     '\t' + '-O ' + output_file_name
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

    input_files = return_input_files(args, 'vcf') if args.input_directory is not None else [args.input_file_path]

    for input_file in input_files:
        slurm_command = return_slurm_command(args)
        output_file_name = gen_output_file_name(args, input_file)
        primary_command = return_primary_command(args, output_file_name, input_file)

        sh_file_name = gen_sh_file_name(args, output_file_name)
        write_out(args, slurm_command, primary_command, sh_file_name)

        submit_job(sh_file_name)

if __name__ == "__main__":
    main()
