import json
from collections import Counter

import fire
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud


def get_email_data(file_path):
    with open("./email_concepts_data.json", "r") as file:
        data = json.load(file)

    term_counter = Counter()
    for terms in data.values():
        term_counter.update(terms)

    df_terms = pd.DataFrame(term_counter.items(), columns=["Term", "Frequency"])
    df_terms_sorted = df_terms.sort_values(by="Frequency", ascending=False)
    return df_terms_sorted


def create_bar_plot(df):
    plt.figure(figsize=(14, 10))
    bars = plt.barh(df["Term"], df["Frequency"])

    plt.xlabel("Frequency", fontsize=14)
    plt.ylabel("Terms", fontsize=14)
    plt.title("Terms Frequency", fontsize=18, fontweight="bold")

    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.gca().invert_yaxis()
    plt.grid(axis="x", linestyle="--", alpha=0.7)

    for bar in bars:
        plt.text(
            bar.get_width(),
            bar.get_y() + bar.get_height() / 2,
            f"{bar.get_width()}",
            va="center",
            ha="left",
            fontsize=12,
        )

    plt.tight_layout()
    plt.savefig("terms_frequency_bar_chart.png", dpi=600)


def create_visualizations(file_path):
    df = get_email_data(file_path)
    create_bar_plot(df)


def main():
    fire.Fire(create_visualizations)


if __name__ == "__main__":
    main()
