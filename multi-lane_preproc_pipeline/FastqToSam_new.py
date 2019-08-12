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
    parser.add_argument('-in_dir', '--input_directory', default='./', help='path to directory containing input files')
    parser.add_argument('-out', '--output_directory', default='./', help='directory to which the "/.FastqToSam/" directory containing outputs will be written to')
    parser.add_argument('-n', '--num_cores', default='1', help='slurm job submission option')
    parser.add_argument('-t', '--runtime', default='0-01:00:00', help='slurm job submission option')
    parser.add_argument('-p', '--queue', default='park', help='slurm job submission option')
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
        if 'input_directory' in arg and d[arg]=='./': d[arg] = os.getcwd() 
        if 'output_directory' in arg and d[arg]=='./': d[arg] = os.getcwd()    
        if 'directory' in arg and d[arg] is not None and d[arg][-1] != '/': d[arg] += '/'

def return_input_files(args, ext):
    print('Input Directory:')
    print(args.input_directory)
    input_fastqs = [os.path.realpath(file) for file in glob.glob(args.input_directory + '*.' + ext)]
    return input_fastqs

def return_samples(args):
    input_fastqs = return_input_files(args, 'fastq.gz')
    samples = []
    for input_fastq in input_fastqs:
        samples.append(
            re.sub('.fastq.gz', '',
	    re.sub('_R._', '_R_', 
                ntpath.basename(input_fastq))))
    return list(set(samples))

def return_sample_input_files(sample, input_files):
    sample_input_files = []
    matcher_index = sample.find('_R_') + 2
    matcher = sample[:matcher_index] + '.' + sample[matcher_index:]
    for input_file in input_files:
        match = re.search(matcher, input_file)
        if match:
            sample_input_files.append(input_file)
    sample_input_files.sort()
    return sample_input_files

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

def gen_output_file_name(args, sample):
    output_file_name = args.output_directory + '.FastqToSam/' + sample + '.bam'
    return output_file_name

def return_twoq_command(args, output_file_name, sample, sample_input_files):
    tmp_dir = args.output_directory + '.FastqToSam/.sh/tmp'
    os.makedirs(tmp_dir, exist_ok=True)
    primary_command = 'java -Xmx8G -Djava.io.tmpdir=' + tmp_dir + ' -jar ' + args.picard_path + ' FastqToSam' ' \\' + '\n' + \
    '\t' + 'FASTQ=' + sample_input_files[0] + ' \\' + '\n' + \
    '\t' + 'FASTQ2=' + sample_input_files[1] + ' \\' + '\n' + \
    '\t' + 'OUTPUT=' + args.output_directory + '.FastqToSam/' + sample + '.bam' ' \\' + '\n' + \
    '\t' + 'READ_GROUP_NAME=' + sample + '_RG' ' \\' + '\n' + \
    '\t' + 'SAMPLE_NAME=' + sample + ' \\' + '\n' + \
    '\t' + 'LIBRARY_NAME=' + args.library_name + ' \\' + '\n' + \
    '\t' + 'PLATFORM=illumina' + ' \\' + '\n' + \
    '\t' + 'TMP_DIR=' + tmp_dir
    return primary_command

def return_oneq_command(args, output_file_name, sample, sample_input_files):
    tmp_dir = args.output_directory + '.FastqToSam/.sh/tmp'
    os.makedirs(tmp_dir, exist_ok=True)
    primary_command = 'java -Xmx8G -Djava.io.tmpdir=' + tmp_dir + ' -jar ' + args.picard_path + ' FastqToSam' ' \\' + '\n' + \
    '\t' + 'FASTQ=' + sample_input_files[0] + ' \\' + '\n' + \
    '\t' + 'OUTPUT=' + args.output_directory + '.FastqToSam/' + sample + '.bam' ' \\' + '\n' + \
    '\t' + 'READ_GROUP_NAME=' + sample + '_RG' ' \\' + '\n' + \
    '\t' + 'SAMPLE_NAME=' + sample + ' \\' + '\n' + \
    '\t' + 'LIBRARY_NAME=' + args.library_name + ' \\' + '\n' + \
    '\t' + 'PLATFORM=illumina' + ' \\' + '\n' + \
    '\t' + 'TMP_DIR=' + tmp_dir
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
    input_files = return_input_files(args, 'fastq.gz')
    # print('Files:')
    # print(input_files)
    samples = return_samples(args)
    print('Samples:')
    print(samples)

    for sample in samples:
        print('Sample to match with:')
        print(sample)
        sample_input_files = return_sample_input_files(sample, input_files)
        print('Sample_Input_Files:')
        print(sample_input_files)
        slurm_command = return_slurm_command(args)
        output_file_name = gen_output_file_name(args, sample)
        primary_command = ""
        if(len(sample_input_files) == 1):
            primary_command = return_oneq_command(args, output_file_name, sample, sample_input_files)
        else:
            primary_command = return_twoq_command(args, output_file_name, sample, sample_input_files)



        sh_file_name = gen_sh_file_name(args, output_file_name)
        write_out(args, slurm_command, primary_command, sh_file_name)

        submit_job(sh_file_name)

if __name__ == "__main__":
    main()
