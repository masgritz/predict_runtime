import subprocess
import os
import sys
import re
import pandas as pd
import numpy as np
import argparse


def natural_sort(l):
    def convert(text): return int(text) if text.isdigit() else text.lower()
    def alphanum_key(key): return [convert(c)
                                   for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


def run_awk(path):
    base_command = "awk -F '|' '{print $1,$3}' "
    decoded_out = []
    column_names = []
    values = []

    for root, dirs, files in os.walk(path):
        for direc in dirs:
            for file in natural_sort(files):
                command_file = base_command + root + direc + file
                process = subprocess.Popen(
                    command_file, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
                out, err = process.communicate()

                decoded_out = out.decode(
                    'utf-8').replace('elapsed', ' runtime').split()
                values.append(decoded_out[::2])

    column_names = decoded_out[1::2]

    df = pd.DataFrame(values, columns=column_names)

    regex = re.compile(r"^\d{1,2}\:\d{2}\.\d{2}")
    df['runtime'] = '0:' + df['runtime'].where(df['runtime'].str.match(regex))
    df['seconds'] = pd.to_timedelta(df['runtime']).dt.total_seconds()

    df = df.apply(pd.to_numeric, errors='ignore')

    df.to_csv(path + 'output_parsed.csv', index=False)


def main():
    run_awk('/home/masgritz/benchmark/NAS_OMP_Turing') # colocar caminho aqui


if __name__ == "__main__":
    main()
