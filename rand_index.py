# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os

def rand_index(song_file, algorithm, interval):

    gt_file = 'annotations/GroundTruth/' + song_file
    pd_file = 'annotations/Prediction/' + algorithm + '/' + song_file

    #get the ground truth boundaries
    ground_truth = []
    with open(gt_file, 'r') as file:
        # Read each line in the file
        for line in file:
            # Print each line
            ground_truth.append(float(line.strip()))

    #get the prediction boundaries
    prediction = []
    with open(pd_file, 'r') as file:
        # Read each line in the file
        prediction = []
        for line in file:
            # Print each line
            prediction.append(float(line.strip()))


    points = [] # array of points
    numOfPoints = int(ground_truth[len(ground_truth) - 1]/interval) + 1

    #making the array of point values
    for i in range(0, numOfPoints):
        points.append(i*interval)

    #main parsing
    count = 0
    agreement = 0
    for i in points:
        for j in points:
            if i < j:
                if check_points(ground_truth, i, j) == check_points(prediction, i, j):
                    agreement += 1
                count += 1
    return float(agreement)/float(count)
def check_points(arr, point1, point2):
    agreed = 1
    for e in arr:
        if (e > point1) & (e > point2):
            break
        if (e > point1) & (e < point2):
            agreed = 0
            break
    return agreed

def go_thru_all_algos():
    all_algos = ''
    directory = 'annotations/Prediction'
    for algodir in os.scandir(directory):
        all_algos = all_algos + algodir.name + '\n'
        count = 0
        sum = 0.0
        for song in os.scandir(algodir):
            score = rand_index(song.name, algodir.name, 0.5)
            all_algos = all_algos + song.name + '\'s score is ' + str(score) + '\n'
            sum = sum + score
            count += 1
        all_algos = all_algos + 'Songs Tested: ' + str(count) + '\n'
        all_algos = all_algos + 'Average Score: ' + str(sum/float(count)) + '\n\n'

    return all_algos





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #print(rand_index('fireflies.txt', 'foote', 0.5))
    all_algos = go_thru_all_algos()
    all_scores_path = 'annotations/all_scores.txt'
    with open(all_scores_path, 'w') as file:
        file.write(all_algos)
    quit()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
