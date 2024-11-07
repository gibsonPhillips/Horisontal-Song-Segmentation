import csv
from Annotated_Intake import *
from Data_Intake import *

### config data
Acceptable_threshold = 3



noID_segment_boundaries = [
    0.000000,
    24.751687,
    67.408604,
    110.077125,
    134.074542,
    176.754667
]


# outputs tuples as timestamps (boundary, nearest beat, nearest downbeat), distance(seconds)
def nearest_beat_finder(algo_boundary, anno_beats):
    nearest_beats = []

    beat_times = [beat[0] for beat in anno_beats]
    downbeat_times = [beat[0] for beat in anno_beats if beat[1] == 1]

    for boundary in algo_boundary:

        # I know
        # innifficiantly checked every timestamp every time
        nearest_beat = (min(beat_times, key=lambda x: abs(x - boundary)))
        nearest_downbeat = (min(downbeat_times, key=lambda x: abs(x-boundary)))

        nearest_beats.append((boundary, nearest_beat, nearest_downbeat))
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

def make_csv_tuple(raw_data):
    boundaries, nearest_beats, nearest_beats_distance, nearest_segments, nearest_segments_distance = raw_data

    csv_tuples = []

    # 0th indexed id numbers
    i = 0
    for boundary, nearest_beat, nearest_beat_distance, nearest_segment, nearest_segment_distance in zip(
            boundaries, nearest_beats, nearest_beats_distance, nearest_segments, nearest_segments_distance):


        csv_tuples.append((
            i,  # Segment index
            boundary,
            nearest_beat[1], # timestamp of nearest beat
            nearest_beat_distance[0], # distance from beat
            nearest_beat[2], # timestamp of nearest downbeat
            nearest_beat_distance[1], # distance from downbeat
            nearest_segment[1],
            nearest_segment_distance
        ))
        i += 1

    return csv_tuples


# write distances to a CSV file
def write_csv(raw_data):
    data = make_csv_tuple(raw_data)

    with open('segment_boundary_distances.csv', mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # !!! update headers
        # headers
        csv_writer.writerow(['Segment', 'Start_Time', 'Nearest_Beat', 'Dist_to_Nearest_Beat',
                             'Nearest_Downbeat', 'Dist_to_Nearest_Downbeat', "Nearest_GT_Segment", "Dist_to_Nearest_GT_Segment"])

        for tuple in data:
            csv_writer.writerow(tuple)
    return




# def main():
anno_beats_txt = "Baseline/Beats_Downbeats/0094_fireflies.txt"
anno_beats = beat_intake(anno_beats_txt)

anno_segments_txt = "Baseline/Segments/0094_fireflies.txt"
anno_segments = segment_intake(anno_segments_txt)

algo_segments_txt = "outputs/Librosa Kmeans CQT Cluster 4/0094Owl City  Fireflies Official Music Video Output.csv"
algo_segments = T2__parse_algo_beats_txt_to_tuples(algo_segments_txt)

## ((boundary, nearest beat timestamp, nearest downbeat timestamp)), ((boundary - nearest_beat, boundary - nearest_downbeat))
nearest_beats, nearest_beats_distance = nearest_beat_finder(algo_segments, anno_beats)
nearest_segments, nearest_segments_distance = nearest_segment_finder(algo_segments, anno_segments)
## ((boundary, nearest_segment)), ((boundary - nearest_segment))

raw = [algo_segments, nearest_beats, nearest_beats_distance, nearest_segments, nearest_segments_distance]
write_csv(raw)






# type 0 parses the vex stuff (idk ask giobspn)
# (timestamp, beat, measure)

# type 1 parses the msaf style
# either [timestamps] or [(timestamp)] haven't figured it out yet

# type 2 parses the librosa style
# (id,start,end,label) with banner
# no actually (start, end, label)


# type 3?

print("ran successfullyy?")
