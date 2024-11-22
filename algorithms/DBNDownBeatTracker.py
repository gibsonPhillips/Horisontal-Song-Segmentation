from madmom.features import (DBNDownBeatTrackingProcessor,
                             RNNDownBeatProcessor)
import os

def downBeatTracker(input_file):
    """DBNDownBeatTracker"""

    config = {
        "fps": 100,                           # Set frames per second
        "beats_per_bar": [3, 4],              # Possible beats per bar
        "max_bpm": 200,                       # Maximum BPM expected
    }

    # Input processor
    in_processor = RNNDownBeatProcessor()

    # Output processor (DBN for tracking beats/downbeats)
    dbn_processor = DBNDownBeatTrackingProcessor(beats_per_bar=config["beats_per_bar"],
                                                 max_bpm=config["max_bpm"],
                                                 fps=config["fps"])

    # Process the audio file
    rnn_result = in_processor(input_file)
    result = dbn_processor(rnn_result)

    return result


def main():
    for song in os.scandir("songs"):
        result = downBeatTracker("songs/" + song.name)
        # Output timestamps and labels to csv
        with open(song.name + "Output.csv", "w") as file:
            file.write("timestamp,beat\n")
            i = 1
            for timestamp, beat in result:
                file.write(f"{timestamp:.2f},{beat}\n")

main()
