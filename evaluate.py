import csv


### config data
Acceptable_threshold = 3
Input_Data = "MSAF"





# temp data 1
segment_boundaries = [
    (0.000000, 24.751687, 'N1'),
    (24.751687, 67.408604, 'A'),
    (67.408604, 110.077125, 'A'),
    (110.077125, 134.074542, 'N2'),
    (134.074542, 176.754667, 'A'),
    (176.754667, 231.862854, 'N3')
]

noID_segment_boundaries = [
    0.000000,
    24.751687,
    67.408604,
    110.077125,
    134.074542,
    176.754667
]


def nearest_downbeat(algo_boundary, anno_beats):
    results = []

    beat_times = [beat[0] for beat in anno_beats]
    downbeat_times = [beat[0] for beat in anno_beats if beat[1] == 1]

    for boundary in algo_boundary:

        # I know
        # innifficiantly checked every timestamp every time
        nearest_beat = min(beat_times, key=lambda x: abs(x - boundary))
        nearest_downbeat = min(downbeat_times, key=lambda x: abs(x-boundary))
        results.append((boundary, nearest_beat, nearest_downbeat))
    return results


# write distances to a CSV file
def write_csv(data):

    with open('segment_boundary_distances.csv', mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # headers
        csv_writer.writerow(['Segment', 'Start_Time', 'End_Time', 'Dist_Start_to_Nearest_Beat',
                             'Dist_Start_to_Nearest_Downbeat', 'Dist_End_to_Nearest_Beat',
                             'Dist_End_to_Nearest_Downbeat'])

        for tuple in data:
            csv_writer.writerow(tuple)
    return




# def main():


print("ran successfullyy")
