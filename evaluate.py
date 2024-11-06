import csv

# temp data
segment_boundaries = [
    (0.000000, 24.751687, 'N1'),
    (24.751687, 67.408604, 'A'),
    (67.408604, 110.077125, 'A'),
    (110.077125, 134.074542, 'N2'),
    (134.074542, 176.754667, 'A'),
    (176.754667, 231.862854, 'N3')
]

# Define beat interval in seconds
beat_interval = 0.66665

# returns distance to beat and distance to downbeat
def calculate_distances(time, beat_interval):
    nearest_beat = round(time / beat_interval) * beat_interval
    dist_to_nearest_beat = abs(time - nearest_beat)
    # Assuming downbeats occur every 4 beats (4 * beat_interval)
    nearest_downbeat = round(time / (4 * beat_interval)) * (4 * beat_interval)
    dist_to_nearest_downbeat = abs(time - nearest_downbeat)
    return dist_to_nearest_beat, dist_to_nearest_downbeat

# write distances to a CSV file
with open('segment_boundary_distances.csv', mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Segment', 'Start_Time', 'End_Time', 'Dist_Start_to_Nearest_Beat', 
                         'Dist_Start_to_Nearest_Downbeat', 'Dist_End_to_Nearest_Beat', 
                         'Dist_End_to_Nearest_Downbeat'])

    for start_time, end_time, segment_name in segment_boundaries:
        # Calculate distances for start and end times
        dist_start_to_beat, dist_start_to_downbeat = calculate_distances(start_time, beat_interval)
        dist_end_to_beat, dist_end_to_downbeat = calculate_distances(end_time, beat_interval)

        # Write each row to the CSV
        csv_writer.writerow([segment_name, start_time, end_time, dist_start_to_beat, 
                             dist_start_to_downbeat, dist_end_to_beat, dist_end_to_downbeat])

print("ran successfullyy")
