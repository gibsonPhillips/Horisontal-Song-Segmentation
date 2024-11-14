# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import csv

def calculate_rand_index(gt_filepath, pd_filepath):

    interval = 0.5

    #get the ground truth information
    ground_truth = []
    with open(gt_filepath, 'r') as gt_file:
        row = []
        for line in gt_file:
             ground_truth.append(line.split(" "))

    #get the prediction information
    predictions = []
    with open(pd_filepath, 'r') as pd_file:
        csv_reader = csv.reader(pd_file)
        for row in csv_reader:
            predictions.append(row)


    points = [] # array of points
    numOfPoints = int(float(ground_truth[len(ground_truth) - 1][0])/interval + 1)

    #making the array of point values
    for i in range(0, numOfPoints):
        points.append(i*interval)

    #main parsing
    count = 0
    agreement = 0
    for i in points:
        for j in points:
            if i < j:
                if prediction_check(predictions, i, j) == ground_truth_check(ground_truth, i, j):
                    agreement += 1
                    #print(str(i) + " " + str(j)) # for testing
                count += 1
    return float(agreement)/float(count)


def prediction_check(predictions, i, j):
    first = 1
    i_segment = '-1'
    j_segment = '-2'
    for row in predictions:
        if first == 1:
            first = 0
        else:
            lower = float(row[1])
            upper = float(row[2])
            if lower <= i < upper:
                i_segment = row[3]
            if lower <= j < upper:
                j_segment = row[3]
    if i_segment == j_segment:
        #print(str(i) + ' ' + str(j))  # for testing
        return 1
    else:
        return 0

def ground_truth_check(ground_truth, i, j):
    first = 1
    i_segment = '-1'
    j_segment = '-2'
    last_row = []
    for row in ground_truth:
        if first == 1:
            first = 0
        else:
            lower = float(last_row[0])
            upper = float(row[0])
            if lower <= i < upper:
                i_segment = last_row[1]
            if lower <= j < upper:
                j_segment = last_row[1]
        last_row = row
    if i_segment == j_segment:
        #print(str(i) + ' ' + str(j)) # for testing
        return 1
    else:
        return 0


test_score = calculate_rand_index('ground_truth/Segments/Fireflies_Segments.txt', 'outputs/Baseline_Even/Fireflies_Baseline_Even.csv')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
