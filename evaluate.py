import csv
import os

# import numpy as np

from Annotated_Intake import *
from Data_Intake import *

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

def boundariesGroundTruth(distToGTBounds, totalBounds):
    gtBoundsNum = 0
    for distGTBound in distToGTBounds:
        if abs(distGTBound) < ACCEPTABLE_THRESHOLD_2:
            gtBoundsNum += 1
    return gtBoundsNum/totalBounds

def groundTruthBoundariesFound(distToGTBounds, nearestGTBounds, gtBounds):
    gtBoundsFound = set()
    for i in range(len(nearestGTBounds)):
        gtBound = nearestGTBounds[i]
        distGTBound = distToGTBounds[i]
        if abs(distGTBound) < ACCEPTABLE_THRESHOLD_2 and gtBound not in gtBoundsFound:
            gtBoundsFound.add(gtBound)
    return len(gtBoundsFound)/len(gtBounds)




def make_csv_tuple(boundaries, nearest_beats, nearest_beats_distance, nearest_segments, nearest_segments_distance):
    # boundaries, nearest_beats, nearest_beats_distance, nearest_segments, nearest_segments_distance = raw_data

    csv_tuples = []

    # 1th indexed id numbers
    i = 1
    for boundary, nearest_beat, nearest_beat_distance, nearest_segment, nearest_segment_distance in zip(boundaries, nearest_beats, nearest_beats_distance, nearest_segments, nearest_segments_distance):

        if(i != 1):
            csv_tuples.append((
                i,  # Segment index
                boundary,
                nearest_beat[1], # timestamp of nearest beat
                nearest_beat[3],
                nearest_beat_distance[0], # distance from beat
                nearest_beat[2], # timestamp of nearest downbeat
                nearest_beat_distance[1], # distance from downbeat
                nearest_segment[1],
                nearest_segment_distance
            ))
        else:
            csv_tuples.append((i,boundary,'NA','NA','NA','NA','NA','NA','NA'))
        i += 1

    tuple = csv_tuples[i-2]
    csv_tuples.pop(i-2)
    csv_tuples.append((tuple[0], tuple[1],'NA','NA','NA','NA','NA','NA','NA'))
    return csv_tuples


# write distances to a CSV file
def write_csv(csv_name, song_name, anno_beats, anno_segments, boundaries, nearest_beats, nearest_beats_distance, nearest_segments, nearest_segments_distance):
    data = make_csv_tuple(boundaries,
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
        csv_writer.writerow(['Boundary', 'Start_Time', 'Nearest_Beat', 'Nearest_Beat_Number', 'Dist_to_Nearest_Beat',
                             'Nearest_Downbeat', 'Dist_to_Nearest_Downbeat', "Nearest_GT_Segment", "Dist_to_Nearest_GT_Segment"])

        for tuple in data:
            csv_writer.writerow(tuple)

# anal headers
        csv_writer.writerow(["Averages", "", "", "", averager(AbVa([i[0] for i in nearest_beats_distance])), "", averager(AbVa([i[1] for i in nearest_beats_distance])), "", averager(AbVa(nearest_segments_distance))])
        csv_writer.writerow(["Proximity Scores", "", "", "", averager(AbVa([i[0] for i in nearest_beats_distance])) / averageTimeBetweenBeats, "", averager(AbVa([i[1] for i in nearest_beats_distance])) / averageTimeBetweenBeats, "", averager(AbVa(nearest_segments_distance)) / averageTimeBetweenBeats])
        csv_writer.writerow(["Percent of ground truth boundaries", boundariesGroundTruth(nearest_segments_distance, len(data))])
        csv_writer.writerow(["Percent of ground truth boundaries found", groundTruthBoundariesFound(nearest_segments_distance, nearest_segments, anno_segments)])
        csv_writer.writerow(["Average time between beats", averageTimeBetweenBeats])
    return




# def main():
anno_beats_txt = "ground_truth/Beats_Downbeats/0094_fireflies.txt"
anno_beats = beat_intake(anno_beats_txt)

anno_segments_txt = "ground_truth/Segments/0094_fireflies.txt"
anno_segments = segment_intake(anno_segments_txt)

for folder in os.scandir("outputs"):
    print(folder.name)
    csv_name = folder.name + ".csv"
    with open(csv_name, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([folder.name])
    for song in os.scandir(folder.path):
        algo_segments = T2__parse_algo_beats_txt_to_tuples(song.path)
        nearest_beats, nearest_beats_distance = nearest_beat_finder(algo_segments, anno_beats)
        nearest_segments, nearest_segments_distance = nearest_segment_finder(algo_segments, anno_segments)
        write_csv(csv_name, song.name, anno_beats, anno_segments, algo_segments, nearest_beats, nearest_beats_distance, nearest_segments, nearest_segments_distance)






# type 0 parses the vex stuff (idk ask giobspn)
# (timestamp, beat, measure)

# type 1 parses the msaf style
# either [timestamps] or [(timestamp)] haven't figured it out yet

# type 2 parses the librosa style
# (id,start,end,label) with banner
# no actually (start, end, label)


# type 3?

print("ran successfullyy?")
