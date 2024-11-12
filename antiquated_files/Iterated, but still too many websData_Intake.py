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
# either [timestamps] or [(timestamp)] haven't figured it out yet
def T1__parse_algo_beats_txt_to_tuples(url):
    algo_beats = []
    with open(url, "r") as file:
        for line in file:
            parts = line.strip().split()

            algo_beats.append(float(parts[0]))

    return algo_beats


# type 2 parses the librosa style
# (id,start,end,label) with banner
# no actually (start, end, label)
def T2__parse_algo_beats_txt_to_tuples(url):
    algo_beats = []
    with open(url, "r") as file:
        for line in file:
            parts = line.strip().split()

            start = float(parts[1])
            end = float(parts[2])
            label = float(parts[2])
            algo_beats.append((start, end, label))

    return algo_beats

