# type 0 parses the vex stuff (idk ask giobspn)
# (timestamp, beat, measure)
def T0__parse_algo_beats_txt_to_tuples(url):
    algo_beats = []
    with open(url, "r") as file:
        for line in file:
            parts = line.strip().split()

            timestamp = float(parts[0])
            beat = int(parts[1])
            measure = int(parts[2])
            algo_beats.append((timestamp, beat, measure))

    return algo_beats


# type 1 parses the msaf style
# [timestamps]
def T1__parse_algo_beats_txt_to_tuples(url):
    algo_beats = []
    with open(url, "r") as file:
        for line in file:
            parts = line.strip().split()

            algo_beats.append(float(parts[0]))

    return algo_beats


# type 2 parses the librosa style
# (id,start,end,label) with banner
def T2__parse_algo_beats_txt_to_tuples(url):
    algo_beats = []
    labels = []
    with open(url, "r") as file:
        for line in file:
            if (line.strip() == "id,start,end,label"):
                pass
            else:

                parts = line.strip().split(",")
                start = float(parts[1])

                algo_beats.append(start)
                labels.append(parts[3])

    return algo_beats, labels

# parses the csv outputs for downbeats in timestamp, beat style
def parse_downbeats_to_tuples(url):
    downbeats = []
    with open(url, "r") as file:
        for line in file:
            if (line.strip() == "timestamp,beat"):
                pass
            else:
                downbeats.append(line.strip().split(","))


    return downbeats

# Takes a file location for exported label outputs for beat tracking and returns a list of the timestamps
def parse_timestamps_to_list(filename):
    third_items = []

    try:
        with open(filename, 'r') as file:
            for line in file:
                items = line.split()
                if len(items) == 3:

                    third_items.append(float(items[2]))
                else:
                    print("something's wrong, I can feel it")
    except FileNotFoundError:
        print(f"Whoopsies: '{filename}' was not found.")
    except ValueError:
        print(f"Whoopsies: A line in the file could not be converted to float.")
    except Exception as e:
        print(f"Whoopsies: {e}")

    return third_items


print("wait")