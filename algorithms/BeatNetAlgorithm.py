from BeatNet.BeatNet import BeatNet
import os

estimator = BeatNet(1, mode='offline', inference_model='DBN', plot=[], thread=False)

Output = estimator.process("C:\\Users\\sethb\\OneDrive - Worcester Polytechnic Institute (wpi.edu)\\gr-MQP-MLSongMap\\General\\Songs and Annotations\\Songs\\0094Owl City  Fireflies Official Music Video.wav")

def main():
    for song in os.scandir("songs"):
        result = estimator.process("songs/" + song.name)
        # Output timestamps and labels to csv
        with open(song.name + "Output.csv", "w") as file:
            file.write("timestamp,beat\n")
            for timestamp, beat in result:
                file.write(f"{timestamp:.2f},{beat}\n")

main()
