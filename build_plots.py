import os
import pandas as pd
import matplotlib.pyplot as plt
from chardet import detect as detect_encoding

WORKING_DIRECTORY = r"data"
INPUT_FILENAMES = [
    "british_english_tts_lexicalset_formants.Table",
    "british_english_tts_hvd_formants.Table",
    "gl_vowels_formants.Table",
    "jf_hvd_formants.Table",
    "jf_lexicalset_formants.Table",
]
CHART_FILENAMES = [
    "british_english_tts_lexicalset_vowels.png",
    "british_english_tts_hvd_vowels.png",
    "gl_vowels.png",
    "jf_hvd_vowels.png",
    "jf_lexicalset_vowels.png",
]
CHART_TITLES = [
    "British English TTS Lexical Set Vowels",
    "British English TTS HVD Vowels",
    "Geoff Lindsey Synthetic Vowels",
    "JF HVD Vowels",
    "JF Lexical Set Vowels",
]
Y_SCALE = (200, 1000)
X_SCALE = (500, 2500)
FIGURE_SIZE = (20, 8)


def main() -> None:

    # Sanity check on user inputs
    if (len(INPUT_FILENAMES) != len(CHART_FILENAMES)) or (
        len(INPUT_FILENAMES) != len(CHART_TITLES)
    ):
        raise ValueError(
            "The number of items in INPUT_FILENAMES, CHART_FILENAMES and CHART_TITLES does not match"
        )

    # Plot all files specified by user
    for i in range(0, len(INPUT_FILENAMES)):
        # Paths
        print(f"Processing {INPUT_FILENAMES[i]}")
        input_path = os.path.join(WORKING_DIRECTORY, INPUT_FILENAMES[i])
        output_path = os.path.join(WORKING_DIRECTORY, CHART_FILENAMES[i])
        chart_title = CHART_TITLES[i]

        # Re-encode file to force utf-8
        reencode_as_utf8(input_path)

        # Plot data
        build_plot(input_path, output_path, chart_title, X_SCALE, Y_SCALE, FIGURE_SIZE)


def build_plot(
    input_path: str,
    output_path: str,
    chart_title: str,
    x_scale: tuple[int, int],
    y_scale: tuple[int, int],
    fig_size: tuple[int, int],
) -> None:
    # Load the data from the CSV file
    df = pd.read_csv(input_path)

    # Create a 3-sample rolling average
    df["F1s"] = df.groupby("vowel")["F1"].transform(lambda x: x.rolling(3, min_periods=1).mean())
    df["F2s"] = df.groupby("vowel")["F2"].transform(lambda x: x.rolling(3, min_periods=1).mean())

    # Filter the data to exclude start and end points
    df_plot = df[(df["time_index"] > 1) & (df["time_index"] < 10)].copy()

    # Make another data frame of just the trajectory start points
    df_startpt = df[df["time_index"] == 2].copy()

    # Init plot and set theme
    plt.figure(figsize=fig_size, dpi=600)
    plt.style.use("seaborn-v0_8-whitegrid")

    # Plot each vowel series separately to preserve order
    for grouping, group in df_plot.groupby("vowel"):

        label_text = str(grouping).strip()
        if label_text == "" or label_text == "None":
            continue

        group = group.sort_values(by="time_index")
        plt.plot(group["F2s"], group["F1s"], linewidth=3, label=label_text)

    # Add labels at the start points
    for i in range(len(df_startpt)):

        label_text = str(df_startpt["vowel"].iloc[i]).strip()
        if label_text == "" or label_text == "None":
            continue

        plt.text(
            df_startpt["F2s"].iloc[i],
            df_startpt["F1s"].iloc[i],
            label_text,
            verticalalignment="bottom",
            horizontalalignment="right",
            fontweight="bold",
        )

    # Reverse the x and y axes and set scales
    plt.gca().invert_xaxis()
    plt.gca().invert_yaxis()

    plt.xlim(x_scale[1], x_scale[0])
    plt.ylim(y_scale[1], y_scale[0])
    plt.gca().set_aspect("equal")

    # Add labels and title
    plt.xlabel("F2 (Hz)")
    plt.ylabel("F1 (Hz)")
    plt.title(chart_title)

    plt.legend(loc="upper left")

    plt.savefig(output_path, bbox_inches="tight")


def reencode_as_utf8(input_path: str):
    # Based upon https://stackoverflow.com/questions/191359/how-to-convert-a-file-to-utf-8-in-python

    def get_encoding_type(file):
        with open(file, "rb") as f:
            rawdata = f.read()
        return detect_encoding(rawdata)["encoding"]

    temp_path = input_path + ".utf8"

    # Re-encode
    input_encoding = get_encoding_type(input_path)
    with open(input_path, "r", encoding=input_encoding) as f, open(
        temp_path, "w", encoding="utf-8"
    ) as e:
        text = f.read()
        e.write(text)

    # Replace old file with new
    os.remove(input_path)
    os.rename(temp_path, input_path)


if __name__ == "__main__":
    main()
