import csv
import os

# import numpy as np

from annotated_intake import *
from data_intake import *
from rand_index import calculate_rand_index

### config data
ACCEPTABLE_THRESHOLD_1 = 0.5
ACCEPTABLE_THRESHOLD_2 = 3

# outputs tuples as timestamps (boundary, nearest beat, nearest downbeat), distance(seconds)
def nearest_beat_finder(algo_boundary, anno_beats):
    nearest_beats = []
    
    beat_times = [beat[0] for beat in anno_beats]
    beat_nums = [beat[1] for beat in anno_beats]
    downbeat_times = [beat[0] for beat in anno_beats if beat[1] == 1]

    for boundary in algo_boundary:

        # I know
        # innifficiantly checked every timestamp every time
        index, nearest_beat = min(enumerate(beat_times), key=lambda x: abs(x[1] - boundary))
        nearest_beat_num = beat_nums[index]
        nearest_downbeat = (min(downbeat_times, key=lambda x: abs(x-boundary)))

        nearest_beats.append((boundary, nearest_beat, nearest_downbeat, nearest_beat_num))
    beat_distance = beat_distances(nearest_beats)
    return nearest_beats, beat_distance


def beat_distances(nearest_beats):
    distances = []
    for row in nearest_beats:
        boundary, nearest_beat, nearest_downbeat = row[0], row[1], row[2]
        distances.append((boundary - nearest_beat, boundary - nearest_downbeat))
    return distances


# algo_segments is [timestamps]
# anno_segments is
def nearest_segment_finder(algo_segments, anno_segments):
    nearest_segments = []
    
    for boundary in algo_segments:

        # I know
        # innifficiantly checked every timestamp every time
        nearest_segment = (min(anno_segments, key=lambda x: abs(x - boundary)))
        nearest_segments.append((boundary, nearest_segment))

    distance = segment_distance(nearest_segments)
    return nearest_segments, distance


def segment_distance(nearest_segments):
    segment_distances = []
    for row in nearest_segments:
        boundary, nearest_segment = row[0], row[1]
        segment_distances.append(boundary - nearest_segment)
    return segment_distances

# takes list of values and returns average of values
def averager(data):
    if len(data) > 2:
        return sum(data[1:-1]) / len(data[1:-1])
    else:
        return None

# takes list of values and returns list of absolute values?
def AbVa(list):
    AbVa_list = [abs(i) for i in list]
    return AbVa_list

def boundariesGroundTruth(distToGTBounds, totalBounds, threshold):
    gtBoundsNum = 0
    for distGTBound in distToGTBounds:
        if abs(distGTBound) < threshold:
            gtBoundsNum += 1
    return gtBoundsNum/totalBounds

def groundTruthBoundariesFound(distToGTBounds, nearestGTBounds, gtBounds, threshold):
    gtBoundsFound = set()
    for i in range(len(nearestGTBounds)):
        gtBound = nearestGTBounds[i][1]
        distGTBound = distToGTBounds[i]
        if abs(distGTBound) < threshold and gtBound not in gtBoundsFound:
            gtBoundsFound.add(gtBound)
    return len(gtBoundsFound)/len(gtBounds)

def make_csv_tuple(boundaries, labels, nearest_beats, nearest_beats_distance, nearest_segments, nearest_segments_distance):
    # boundaries, label, nearest_beats, nearest_beats_distance, nearest_segments, nearest_segments_distance = raw_data

    csv_tuples = []

    # 1th indexed id numbers
    i = 1
    for boundary, label, nearest_beat, nearest_beat_distance, nearest_segment, nearest_segment_distance in zip(boundaries, labels, nearest_beats, nearest_beats_distance, nearest_segments, nearest_segments_distance):

        if(i != 1):
            csv_tuples.append((
                i,  # Segment index
                boundary,
                label,
                nearest_beat[1], # timestamp of nearest beat
                nearest_beat[3],
                nearest_beat_distance[0], # distance from beat
                nearest_beat[2], # timestamp of nearest downbeat
                nearest_beat_distance[1], # distance from downbeat
                nearest_segment[1],
                nearest_segment_distance
            ))
        else:
            csv_tuples.append((i,boundary,label,'NA','NA','NA','NA','NA','NA','NA'))
        i += 1

    tuple = csv_tuples[i-2]
    csv_tuples.pop(i-2)
    csv_tuples.append((tuple[0], tuple[1], tuple[2],'NA','NA','NA','NA','NA','NA','NA'))
    return csv_tuples


# write distances to a CSV file
def write_csv(csv_name, song_name, labels, anno_beats, anno_segments, boundaries, nearest_beats, nearest_beats_distance, nearest_segments, nearest_segments_distance, rand_index_score):
    data = make_csv_tuple(boundaries,
                          labels,
                          nearest_beats,
                          nearest_beats_distance,
                          nearest_segments,
                          nearest_segments_distance)
    
    averageTimeBetweenBeats = float(anno_beats[1][0]) - float(anno_beats[0][0])

    with open(csv_name, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        csv_writer.writerow([])
        csv_writer.writerow([song_name])

        # !!! update headers
        # headers
        csv_writer.writerow(['Boundary', 'Boundary_Timestamp', "Label", 'Nearest_Beat', 'Nearest_Beat_Number', 'Dist_to_Nearest_Beat',
                             'Nearest_Downbeat', 'Dist_to_Nearest_Downbeat', "Nearest_GT_Segment", "Dist_to_Nearest_GT_Segment"])

        for tuple in data:
            csv_writer.writerow(tuple)


        nearest_any_beat = averager(AbVa([i[0] for i in nearest_beats_distance]))
        nearest_downbeats = averager(AbVa([i[1] for i in nearest_beats_distance]))
        nearest_gt_segments = averager(AbVa(nearest_segments_distance))
        nearest_any_beat_ps = nearest_any_beat / averageTimeBetweenBeats
        nearest_downbeats_ps = nearest_downbeats / averageTimeBetweenBeats
        nearest_gt_segments_ps = nearest_gt_segments / averageTimeBetweenBeats
        gt_boundaries_1 = boundariesGroundTruth(nearest_segments_distance, len(data), ACCEPTABLE_THRESHOLD_1)
        gt_boundaries_found_1 = groundTruthBoundariesFound(nearest_segments_distance, nearest_segments, anno_segments, ACCEPTABLE_THRESHOLD_1)
        gt_boundaries_2 = boundariesGroundTruth(nearest_segments_distance, len(data), ACCEPTABLE_THRESHOLD_2)
        gt_boundaries_found_2 = groundTruthBoundariesFound(nearest_segments_distance, nearest_segments, anno_segments, ACCEPTABLE_THRESHOLD_2)
        gt_boundaries_3 = boundariesGroundTruth(nearest_segments_distance, len(data), averageTimeBetweenBeats*2)
        gt_boundaries_found_3 = groundTruthBoundariesFound(nearest_segments_distance, nearest_segments, anno_segments, averageTimeBetweenBeats*2)


        # anal headers
        csv_writer.writerow(["Averages", "", "", "", nearest_any_beat, "", nearest_downbeats, "", nearest_gt_segments])
        csv_writer.writerow(["Proximity Scores", "", "", "", nearest_any_beat_ps, "", nearest_downbeats_ps, "", nearest_gt_segments_ps])
        csv_writer.writerow(["Percent of ground truth boundaries (0.5 sec)", gt_boundaries_1])
        csv_writer.writerow(["Percent of ground truth boundaries found (0.5 sec)", gt_boundaries_found_1])
        csv_writer.writerow(["Percent of ground truth boundaries (3 sec)", gt_boundaries_2])
        csv_writer.writerow(["Percent of ground truth boundaries found (3 sec)", gt_boundaries_found_2])
        csv_writer.writerow(["Percent of ground truth boundaries (2 beats)", gt_boundaries_3])
        csv_writer.writerow(["Percent of ground truth boundaries found (2 beats)", gt_boundaries_found_3])
        csv_writer.writerow(["Average time between beats", averageTimeBetweenBeats])
        csv_writer.writerow(["Rand Index Score", rand_index_score])
    return nearest_any_beat, nearest_downbeats, nearest_gt_segments, nearest_any_beat_ps, nearest_downbeats_ps, nearest_gt_segments_ps, gt_boundaries_1, gt_boundaries_found_1, gt_boundaries_2, gt_boundaries_found_2, gt_boundaries_3, gt_boundaries_found_3

def linear_normalize(data):
    min_val = min(data)
    max_val = max(data)
    normalized_data = [(x - min_val) / (max_val - min_val) for x in data]
    return normalized_data

def calculate_final_scores(heuristics):
    # Normalization
    normalized_1 = linear_normalize([row[1] for row in heuristics])
    normalized_found_1 = linear_normalize([row[2] for row in heuristics])
    normalized_2 = linear_normalize([row[3] for row in heuristics])
    normalized_found_2 = linear_normalize([row[4] for row in heuristics])
    normalized_3 = linear_normalize([row[5] for row in heuristics])
    normalized_found_3 = linear_normalize([row[6] for row in heuristics])
    normalized_rand_index = linear_normalize([row[7] for row in heuristics])

    final_scores = []

    # Calculate scores
    for i in range(len(heuristics)):
        # Get the ground truth prediction score

        precision = (normalized_2[i] + normalized_3[i]) / 2
        recall = (normalized_found_2[i] + normalized_found_3[i]) / 2
        low_tolerance = (normalized_1[i] + normalized_found_1[i]) / 2

        # take the average between ground truth prediction score and rand index
        final_scores.append([heuristics[i][0], precision, recall, low_tolerance, normalized_rand_index[i], (precision + recall + low_tolerance + normalized_rand_index[i]) / 4])

    with open("final_algorithm_scores.csv", mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        header = ['Algorithm Name', 'Precision', 'Recall', 'Low Tolerance', 'Rand Index', 'Overall Score (Average)']
        csv_writer.writerow(header)
        for row in final_scores:
            csv_writer.writerow(row)

def create_evaluation_csvs():
    try:
        os.mkdir('algorithm_evaluations')
    except FileExistsError:
      print('algorithm_evaluations exists')


    with open("compiled_evaluation_outputs.csv", mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["All Evaluation Data"])

    evaluation_heuristics = []

    #MASTER LOOP
    for folder in os.scandir("outputs"):
        print(folder.name)
        csv_path = "algorithm_evaluations/" + folder.name + ".csv"

        song_count = 0
        rand_index_sum = 0
        nearest_any_beat_sum = 0
        nearest_downbeats_sum = 0
        nearest_gt_segments_sum = 0
        nearest_any_beat_ps_sum = 0
        nearest_downbeats_ps_sum = 0
        nearest_gt_segments_ps_sum = 0
        gt_boundaries_1_sum = 0
        gt_boundaries_found_1_sum = 0
        gt_boundaries_2_sum = 0
        gt_boundaries_found_2_sum = 0
        gt_boundaries_3_sum = 0
        gt_boundaries_found_3_sum = 0


        with open(csv_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([folder.name])



        for song in os.scandir(folder.path):
            songNameSubstring = song.name.split("_")[0]

            anno_beats_path = "ground_truth/Beats_Downbeats/" + songNameSubstring + "_Beats.txt"
            anno_segments_path = "ground_truth/Segments/" + songNameSubstring + "_Segments.txt"
            anno_beats = beat_intake(anno_beats_path)
            anno_segments = segment_intake(anno_segments_path)

            algo_segments, labels = T2__parse_algo_beats_txt_to_tuples(song.path)
            nearest_beats, nearest_beats_distance = nearest_beat_finder(algo_segments, anno_beats)
            nearest_segments, nearest_segments_distance = nearest_segment_finder(algo_segments, anno_segments)

            #rand_index
            rand_index_score = calculate_rand_index(anno_segments_path, song.path)
            song_count += 1
            rand_index_sum += rand_index_score

            #Write to the csv for specific set of outputs for the specific song
            nearest_any_beat, nearest_downbeats, nearest_gt_segments, nearest_any_beat_ps, nearest_downbeats_ps, nearest_gt_segments_ps, gt_boundaries_1, gt_boundaries_found_1, gt_boundaries_2, gt_boundaries_found_2, gt_boundaries_3, gt_boundaries_found_3 = write_csv(csv_path, song.name, labels, anno_beats, anno_segments, algo_segments, nearest_beats, nearest_beats_distance, nearest_segments, nearest_segments_distance, rand_index_score)

            #Add to the sums
            nearest_any_beat_sum += nearest_any_beat
            nearest_downbeats_sum += nearest_downbeats
            nearest_gt_segments_sum += nearest_gt_segments
            nearest_any_beat_ps_sum += nearest_any_beat_ps
            nearest_downbeats_ps_sum += nearest_downbeats_ps
            nearest_gt_segments_ps_sum += nearest_gt_segments_ps
            gt_boundaries_1_sum += gt_boundaries_1
            gt_boundaries_found_1_sum += gt_boundaries_found_1
            gt_boundaries_2_sum += gt_boundaries_2
            gt_boundaries_found_2_sum += gt_boundaries_found_2
            gt_boundaries_3_sum += gt_boundaries_3
            gt_boundaries_found_3_sum += gt_boundaries_found_3

        #Add to the end of csv (after all songs)
        with open(csv_path, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([])
            csv_writer.writerow(['Average Distance to Nearest Beat (Average)', float(nearest_any_beat_sum) / float(song_count)])
            csv_writer.writerow(['Average Distance to Nearest Beat (Proximity Score)', float(nearest_any_beat_ps_sum) / float(song_count)])
            csv_writer.writerow(['Average Distance to Nearest Downbeat (Average)', float(nearest_downbeats_sum) / float(song_count)])
            csv_writer.writerow(['Average Distance to Nearest Downbeat (Proximity Score)', float(nearest_downbeats_ps_sum) / float(song_count)])
            csv_writer.writerow(['Average Distance to Nearest GT Segment (Average)', float(nearest_gt_segments_sum) / float(song_count)])
            csv_writer.writerow(['Average Distance to Nearest GT Segment (Proximity Score)', float(nearest_gt_segments_ps_sum) / float(song_count)])

            csv_writer.writerow(['Average Percent of Ground Truth Boundaries (0.5)', float(gt_boundaries_1_sum) / float(song_count)])
            csv_writer.writerow(['Average Percent of Ground Truth Boundaries Found (0.5)', float(gt_boundaries_found_1_sum) / float(song_count)])
            csv_writer.writerow(['Average Percent of Ground Truth Boundaries (3)', float(gt_boundaries_2_sum) / float(song_count)])
            csv_writer.writerow(['Average Percent of Ground Truth Boundaries Found (3)', float(gt_boundaries_found_2_sum) / float(song_count)])
            csv_writer.writerow(['Average Percent of Ground Truth Boundaries (2 beats)', float(gt_boundaries_3_sum) / float(song_count)])
            csv_writer.writerow(['Average Percent of Ground Truth Boundaries Found (2 beats)', float(gt_boundaries_found_3_sum) / float(song_count)])

            csv_writer.writerow(['Average Rand Index Score', float(rand_index_sum) / float(song_count)])

        # compiled output csv
        with open("compiled_evaluation_outputs.csv", mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([])
            csv_writer.writerow([folder.name])
            csv_writer.writerow(['Average Distance to Nearest Beat (Average)', float(nearest_any_beat_sum) / float(song_count)])
            csv_writer.writerow(['Average Distance to Nearest Beat (Proximity Score)', float(nearest_any_beat_ps_sum) / float(song_count)])
            csv_writer.writerow(['Average Distance to Nearest Downbeat (Average)', float(nearest_downbeats_sum) / float(song_count)])
            csv_writer.writerow(['Average Distance to Nearest Downbeat (Proximity Score)', float(nearest_downbeats_ps_sum) / float(song_count)])
            csv_writer.writerow(['Average Distance to Nearest GT Segment (Average)', float(nearest_gt_segments_sum) / float(song_count)])
            csv_writer.writerow(['Average Distance to Nearest GT Segment (Proximity Score)', float(nearest_gt_segments_ps_sum) / float(song_count)])

            csv_writer.writerow(['Average Percent of Ground Truth Boundaries (0.5)', float(gt_boundaries_1_sum) / float(song_count)])
            csv_writer.writerow(['Average Percent of Ground Truth Boundaries Found (0.5)', float(gt_boundaries_found_1_sum) / float(song_count)])
            csv_writer.writerow(['Average Percent of Ground Truth Boundaries (3)', float(gt_boundaries_2_sum) / float(song_count)])
            csv_writer.writerow(['Average Percent of Ground Truth Boundaries Found (3)', float(gt_boundaries_found_2_sum) / float(song_count)])
            csv_writer.writerow(['Average Percent of Ground Truth Boundaries (2 beats)', float(gt_boundaries_3_sum) / float(song_count)])
            csv_writer.writerow(['Average Percent of Ground Truth Boundaries Found (2 beats)', float(gt_boundaries_found_3_sum) / float(song_count)])

            csv_writer.writerow(['Average Rand Index Score', float(rand_index_sum) / float(song_count)])

        # For final heuristic calculations
        evaluation_heuristics.append([folder.name, float(gt_boundaries_1_sum) / float(song_count), float(gt_boundaries_found_1_sum) / float(song_count), float(gt_boundaries_2_sum) / float(song_count), float(gt_boundaries_found_2_sum) / float(song_count), float(gt_boundaries_3_sum) / float(song_count), float(gt_boundaries_found_3_sum) / float(song_count), float(rand_index_sum) / float(song_count)])

    #Create the final CSV
    calculate_final_scores(evaluation_heuristics)


create_evaluation_csvs()


print("ran successfullyy?")
