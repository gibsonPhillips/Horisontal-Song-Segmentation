def parse_algo_beats_txt_to_tuples(data_str):
    data_tuples = []

    # Split the data by lines
    lines = data_str.strip().splitlines()

    for line in lines:
        parts = line.split()

        time = float(parts[0])
        beat = int(parts[1])
        measure = int(parts[2])
        data_tuples.append((time, beat, measure))

    return data_tuples

def anno_beats_str(filepath):
    with open(filepath, "r") as file:
        content = file.read()
    return content

# test
data_str = anno_beats_str("")

data_tuples = parse_algo_beats_txt_to_tuples(data_str)
print(data_tuples)
