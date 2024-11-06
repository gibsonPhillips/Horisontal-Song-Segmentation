def parse_data_to_tuples(data_str):
    data_tuples = []

    # Split the data by lines
    lines = data_str.strip().splitlines()

    for line in lines:
        # Split each line by whitespace
        parts = line.split()

        # Convert values to the appropriate types and add to the list as a tuple
        time = float(parts[0])
        beat = int(parts[1])
        measure = int(parts[2])
        data_tuples.append((time, beat, measure))

    return data_tuples

def grab_data_str(filepath):
    with open(filepath, "r") as file:
        content = file.read()
    return content

# test
data_str = grab_data_str("")

data_tuples = parse_data_to_tuples(data_str)
print(data_tuples)
