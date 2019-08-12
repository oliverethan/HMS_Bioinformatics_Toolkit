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
    parser.add_argument('-tumor_name', '--input_tumor_name', help='name of tumor file')
    parser.add_argument('-out', '--output_directory', default='./', help='directory to which the output will be written to')
    parser.add_argument('-n', '--num_cores', default='1', help='slurm job submission option')
    parser.add_argument('-t', '--runtime', default='4-23:59:59', help='slurm job submission option')
    parser.add_argument('-p', '--queue', default='medium', help='slurm job submission option')
    parser.add_argument('--mem_per_cpu', default='20G', help='slurm job submission option')
    parser.add_argument('--mail_type', default='ALL', help='slurm job submission option')
    parser.add_argument('--mail_user', default='<EMAIL>', help='slurm job submission option')
    parser.add_argument('-gatk', '--gatk_path', default='gatk', help='path to software')
    parser.add_argument('-reference', '--reference_path', default='/n/data1/hms/dbmi/park/jake/Resources/03_pcawg_ref/genome.fa', help='path to reference_path file')
    return parser.parse_args()

def clean_arg_paths(args):
    """Modifies all user-inputted directory paths such that they end with a '/'"""
    d = vars(args)
    for arg in d.keys():
        if 'output_directory' in arg and d[arg]=='./': d[arg] = os.getcwd()
        if 'directory' in arg and d[arg] is not None and d[arg][-1] != '/': d[arg] += '/'


def return_slurm_command(args):
    """Returns slurm command given args provided"""
    slurm_command = '#!/bin/bash\n' + \
                '#SBATCH -J ' + args.input_tumor_name + '\n' + \
                '#SBATCH -n ' + args.num_cores + '\n' + \
                '#SBATCH -t ' + args.runtime + '\n' + \
                '#SBATCH -p ' + args.queue + '\n' + \
                '#SBATCH --mem-per-cpu=' + args.mem_per_cpu + '\n' + \
                '#SBATCH --mail-type=' + args.mail_type + '\n' + \
                '#SBATCH --mail-user=' + args.mail_user + '\n'
    return slurm_command

def gen_output_file_name(args):
    output_file_name = args.output_directory + ntpath.basename(args.input_tumor_name) + '.vcf'
    return output_file_name

def return_primary_command(args, output_file_name):
    primary_command = args.gatk_path + ' --java-options \"-Xmx16g\"' + ' \\' + '\n' + \
     '\t' + 'Mutect2' + ' \\' + '\n' + \
     '\t' + '-R ' + args.reference_path + ' \\' + '\n' + \
     '\t' + '-I ' + args.input_tumor_path  + ' \\' + '\n' + \
     '\t' + '-tumor ' + args.input_tumor_name  + ' \\' + '\n' + \
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

    slurm_command = return_slurm_command(args)
    output_file_name = gen_output_file_name(args)
    primary_command = return_primary_command(args, output_file_name)

    sh_file_name = gen_sh_file_name(args, output_file_name)
    write_out(args, slurm_command, primary_command, sh_file_name)

    submit_job(sh_file_name)

if __name__ == "__main__":
    main()



    























