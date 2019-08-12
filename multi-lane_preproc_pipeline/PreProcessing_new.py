# Ethan Oliver
# Harvard Medical School
# Department of Biomedical Informatics
# Park Lab
# 2019


from time import sleep
import argparse
import os
import re
import ntpath
import glob
import sys
import fileinput
from shutil import copyfile

def parse_args():
    """Uses argparse to enable user to customize script functionality"""
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-l', '--list', help='path to file containing input files')
    parser.add_argument('-out', '--output_directory', default='./', help='directory to which the "/.PreProcessing/" directory containing outputs will be written to')
    parser.add_argument('-n', '--num_cores', default='1', help='slurm job submission option')
    parser.add_argument('-t', '--runtime', default='30-00:00:00', help='slurm job submission option')
    parser.add_argument('-p', '--queue', default='park', help='slurm job submission option')
    parser.add_argument('--mem_per_cpu', default='10G', help='slurm job submission option')
    parser.add_argument('--mail_type', default='ALL', help='slurm job submission option')
    parser.add_argument('--mail_user', default='<EMAIL>', help='slurm job submission option')
    parser.add_argument('-overrides', '--overrides_path', default='/n/data1/hms/dbmi/park/alon/software/gatk4-data-processing-master/overrides.conf', help='path to overrides.conf file')
    parser.add_argument('-cromwell', '--cromwell_path', default='/n/data1/hms/dbmi/park/alon/software/cromwell-36.jar', help='path to cromwell.jar file')
    parser.add_argument('-gatk_wdl', '--gatk4_data_processing_path', default='/n/data1/hms/dbmi/park/alon/software/gatk4-data-processing-master/processing-for-variant-discovery-gatk4.wdl', help='path to gatk4-data-processing file')
    parser.add_argument('-input_json', '--input_json_path', default='/n/data1/hms/dbmi/park/alon/software/gatk4-data-processing-master/processing-for-variant-discovery-gatk4.b37.wgs.inputs.json', help='path to gatk4-data-processing file')
    return parser.parse_args()

def clean_arg_paths(args):
    """Modifies all user-inputted directory paths such that they end with a '/'"""
    d = vars(args)
    for arg in d.keys():
        if 'output_directory' in arg and d[arg]=='./': d[arg] = os.getcwd()    
        if 'directory' in arg and d[arg] is not None and d[arg][-1] != '/': d[arg] += '/'

def generate_input_json(args, sample_name):
    dir = args.output_directory + '.PreProcessing/' + '.' + sample_name + '/'
    os.makedirs(dir, exist_ok=True)
    
    copyfile(args.input_json_path, dir + 'input.json')
    with fileinput.FileInput(dir + 'input.json', inplace=True) as file:
        for line in file:
            print(line.replace(
            "SRR475190", sample_name).replace(
            "output_dir/.PreProcessing/.sample_name/list.txt", args.list).replace(
            "output_dir/", args.output_directory + '.PreProcessing/'), end='')

    copyfile(args.overrides_path, dir + 'overrides.conf')
    with fileinput.FileInput(dir + 'overrides.conf', inplace=True) as file:
        for line in file:
            print(line.replace(
            "priopark", args.queue), end='')

    copyfile(args.gatk4_data_processing_path, dir + 'processing-for-variant-discovery-gatk4.wdl')
    with fileinput.FileInput(dir + 'processing-for-variant-discovery-gatk4.wdl', inplace=True) as file:
        for line in file:
            print(line.replace(
            "priopark", args.queue), end='')

    return dir + 'input.json'



def return_slurm_command(args):
    """Returns slurm command given args provided"""
    slurm_command = '#!/bin/bash\n' + \
                '#SBATCH -n ' + args.num_cores + '\n' + \
                '#SBATCH -t ' + args.runtime + '\n' + \
                '#SBATCH -p ' + args.queue + '\n' + \
                '#SBATCH --mem-per-cpu=' + args.mem_per_cpu + '\n' + \
                '#SBATCH --mail-type=' + args.mail_type + '\n' + \
                '#SBATCH --mail-user=' + args.mail_user + '\n' + \
		'#SBATCH --exclude=compute-p-17-[34-46]' + '\n'
    if args.queue in ['park', 'priopark']:
        slurm_command += '#SBATCH --account=park_contrib' + '\n'
    return slurm_command

def gen_output_file_name(args, sample_name):
    output_file_name = args.output_directory + '.PreProcessing/' + '.' + sample_name + '/' + sample_name + '.bam'
    return output_file_name

def return_primary_command(args, output_file_name, input_json):
    primary_command = 'module load gcc/6.2.0 python/2.7.12 samtools/1.3.1 bwa/0.7.15' + '\n' + 'java -Dconfig.file=' + re.sub('input.json', 'overrides.conf', input_json) + ' -jar ' + args.cromwell_path + ' run ' + re.sub('input.json', 'processing-for-variant-discovery-gatk4.wdl', input_json) + ' -i ' + input_json
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

    sample_name =  ntpath.basename(args.list)
    print('Sample_name' , sample_name)

    input_json = generate_input_json(args, sample_name)
    slurm_command = return_slurm_command(args)
    output_file_name = gen_output_file_name(args, sample_name)
    primary_command = return_primary_command(args, output_file_name, input_json)
    sh_file_name = gen_sh_file_name(args, output_file_name)
    write_out(args, slurm_command, primary_command, sh_file_name)

    submit_job(sh_file_name)
    sleep(1)
if __name__ == "__main__":
    main()
