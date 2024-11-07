


def beat_intake(url):
    beats = []
    with open(url, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                timestamp = float(parts[0])
                beat_number = int(parts[1])
                measure_number = int(parts[2])

                beats.append((timestamp, beat_number, measure_number))

            else:
                print("Annotated_Intake error, beat line error: ", line)
    return beats


def segment_intake(url):
    segments = []
    with open(url, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                segment_timestamp = float(parts[0])
                # segment_id = str(parts[1])

                # segments.append((segment_timestamp, segment_id))
                segments.append(segment_timestamp)
            else:
                print("Annotated_intake error, segment line error", line)
    return segments

