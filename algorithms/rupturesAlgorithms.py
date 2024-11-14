

# %%
import matplotlib.pyplot as plt
import librosa
import numpy as np
import os
from IPython.display import Audio, display

import ruptures as rpt  # our package

librosa.util.list_examples()


# %%


def runSegmentation(song_name, algorithm, numSegments):

    def fig_ax(figsize=(15, 5), dpi=150):
        """Return a (matplotlib) figure and ax objects with given size."""
        return plt.subplots(figsize=figsize, dpi=dpi)



    duration = 300  # in seconds
    filename = "C:\\Users\\sethb\\OneDrive - Worcester Polytechnic Institute (wpi.edu)\\gr-MQP-MLSongMap\\General\\Songs and Annotations\\Songs\\" + song_name
    #filename = librosa.ex("brahms")
    signal, sampling_rate = librosa.load(filename, duration=duration)

    # listen to the music
    display(Audio(data=signal, rate=sampling_rate))

    # look at the envelope
    fig, ax = fig_ax()
    ax.plot(np.arange(signal.size) / sampling_rate, signal)
    ax.set_xlim(0, signal.size / sampling_rate)
    ax.set_xlabel("Time (s)")
    _ = ax.set(title="Sound envelope")


    # Compute the onset strength
    hop_length_tempo = 256
    oenv = librosa.onset.onset_strength(
        y=signal, sr=sampling_rate, hop_length=hop_length_tempo
    )
    # Compute the tempogram
    tempogram = librosa.feature.tempogram(
        onset_envelope=oenv,
        sr=sampling_rate,
        hop_length=hop_length_tempo,
    )
    # Display the tempogram
    fig, ax = fig_ax()
    _ = librosa.display.specshow(
        tempogram,
        ax=ax,
        hop_length=hop_length_tempo,
        sr=sampling_rate,
        x_axis="s",
        y_axis="tempo",
    )



    # Choose detection method
    if(algorithm == "KernalCPD"):
        algo = rpt.KernelCPD(kernel="linear").fit(tempogram.T)
    elif(algorithm == "Window"):
        algo = rpt.Window().fit(tempogram.T)

    # Choose the number of changes (elbow heuristic)
    n_bkps_max = 20  # K_max
    # Start by computing the segmentation with most changes.
    # After start, all segmentations with 1, 2,..., K_max-1 changes are also available for free.
    _ = algo.predict(n_bkps_max)

    array_of_n_bkps = np.arange(1, n_bkps_max + 1)


    def get_sum_of_cost(algo, n_bkps) -> float:
        """Return the sum of costs for the change points `bkps`"""
        bkps = algo.predict(n_bkps=n_bkps)
        return algo.cost.sum_of_costs(bkps)


    fig, ax = fig_ax((7, 4))
    ax.plot(
        array_of_n_bkps,
        [get_sum_of_cost(algo=algo, n_bkps=n_bkps) for n_bkps in array_of_n_bkps],
        "-*",
        alpha=0.5,
    )
    ax.set_xticks(array_of_n_bkps)
    ax.set_xlabel("Number of change points")
    ax.set_title("Sum of costs")
    ax.grid(axis="x")
    ax.set_xlim(0, n_bkps_max + 1)

    # Visually we choose n_bkps=5 (highlighted in red on the elbow plot)
    n_bkps = numSegments
    _ = ax.scatter([numSegments], [get_sum_of_cost(algo=algo, n_bkps=numSegments)], color="r", s=100)


    # Segmentation
    bkps = algo.predict(n_bkps=n_bkps)
    # Convert the estimated change points (frame counts) to actual timestamps
    bkps_times = librosa.frames_to_time(bkps, sr=sampling_rate, hop_length=hop_length_tempo)

    # Displaying results
    fig, ax = fig_ax()
    _ = librosa.display.specshow(
        tempogram,
        ax=ax,
        x_axis="s",
        y_axis="tempo",
        hop_length=hop_length_tempo,
        sr=sampling_rate,
    )

    for b in bkps_times[:-1]:
        ax.axvline(b, ls="--", color="white", lw=4)


    # Compute change points corresponding indexes in original signal
    bkps_time_indexes = (sampling_rate * bkps_times).astype(int).tolist()

    for segment_number, (start, end) in enumerate(
        rpt.utils.pairwise([0] + bkps_time_indexes), start=1
    ):
        segment = signal[start:end]
        print(f"Segment n°{segment_number} (duration: {segment.size/sampling_rate:.2f} s)")
        print(f"Playing segment {segment_number} from {start/sampling_rate} to {end/sampling_rate} seconds")
        display(Audio(data=segment, rate=sampling_rate))


    # Output timestamps to csv
    bkps_time_indexes = (sampling_rate * bkps_times).astype(int).tolist()
    i = 1
    with open(song_name + " Output.csv", "w") as file:
        file.write("id,start,end,label\n")

        for segment_number, (start, end) in enumerate(
            rpt.utils.pairwise([0] + bkps_time_indexes), start=1
        ):
            segment = signal[start:end]
            file.write(f"{segment_number},{start/sampling_rate},{end/sampling_rate}\n")
            i = i+1
    
dir_path = "C:\\Users\\sethb\\OneDrive - Worcester Polytechnic Institute (wpi.edu)\\gr-MQP-MLSongMap\\General\\Songs and Annotations\\Songs"

# for song in os.scandir(dir_path):
#     runSegmentation(song.name, "KernalCPD", 5)

for song in os.scandir(dir_path):
    runSegmentation(song.name, "Window", 5)
# %%
