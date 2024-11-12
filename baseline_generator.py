import os
import random
import csv
from numpy import sort

from annotated_intake import segment_intake


def all_baselines():
    dir_path = 'ground_truth/Segments'
    for song in os.scandir(dir_path):
        create_even_baseline(song.name)
        create_random_baseline(song.name)

def create_even_baseline(song_file):
    gt_file = 'ground_truth/Segments/' + song_file
    ground_truth = segment_intake(gt_file)


    baseline = []

    length = ground_truth[len(ground_truth) - 1] - ground_truth[0]
    interval = length / (len(ground_truth) - 1)

    #create boundaries
    for e in range(0, len(ground_truth)):
        baseline.append(ground_truth[0] + e*interval)

    try:
        os.mkdir('outputs/Baseline_Even')
    except FileExistsError:
        print('Folder \"outputs/Baseline_Even\" already exists')

    row = ['id', 'start', 'end', 'label']
    last = ''
    count = 0

    file_path = 'outputs/Baseline_Even/' + create_csv_name(song_file, 'Baseline_Even')
    with open(file_path, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        first = 1
        for boundary in baseline:
            if first == 1:
                first = 0
            else:
                row = []
                row.append(count)
                row.append(last)
                row.append(str(boundary))
                row.append(count % 5)
            csv_writer.writerow(row)
            count += 1
            last = str(boundary)

def create_random_baseline(song_file):
    gt_file = 'ground_truth/Segments/' + song_file
    ground_truth = ground_truth = segment_intake(gt_file)

    baseline = []

    #create boundaries
    for e in range(0, len(ground_truth)):
        baseline.append(random.uniform(ground_truth[0], ground_truth[len(ground_truth) - 1]))
    baseline = sort(baseline)

    try:
        os.mkdir('outputs/Baseline_Random')
    except FileExistsError:
        print('Folder \"outputs/Baseline_Random\" already exists')

    row = ['id', 'start', 'end', 'label']
    last = ''
    count = 0

    file_path = 'outputs/Baseline_Random/' + create_csv_name(song_file, 'Baseline_Random')

    with open(file_path, 'w', newline='') as file:
        csv_writer = csv.writer(file)
        first = 1
        for boundary in baseline:
            if first == 1:
                first = 0
            else:
                row = []
                row.append(count)
                row.append(last)
                row.append(str(boundary))
                row.append(random.randint(0,4))
            csv_writer.writerow(row)
            count += 1
            last = str(boundary)

def create_csv_name(song_file, algo):
    new_name = ''
    if '0039' in song_file:
        new_name = 'Bulletproof_' + algo + '.csv'
    if '0043' in song_file:
        new_name = 'CallMeMaybe_' + algo + '.csv'
    if '0094' in song_file:
        new_name = 'Fireflies_' + algo + '.csv'
    if '0360' in song_file:
        new_name = 'CoolerThanMe_' + algo + '.csv'
    if '0618' in song_file:
        new_name = 'Clocks_' + algo + '.csv'
    if '0654' in song_file:
        new_name = 'Dynamite_' + algo + '.csv'
    if '0854' in song_file:
        new_name = 'OverMyHead_' + algo + '.csv'
    if '0910' in song_file:
        new_name = 'Solo_' + algo + '.csv'
    return new_name


all_baselines()