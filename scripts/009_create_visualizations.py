import json
import os
from collections import Counter

import fire
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from wordcloud import WordCloud


def get_email_data(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    term_counter = Counter()
    for terms in data.values():
        term_counter.update(terms)

    df_terms = pd.DataFrame(term_counter.items(), columns=["Term", "Frequency"])
    df_terms_sorted = df_terms.sort_values(by="Frequency", ascending=False)
    return term_counter, df_terms_sorted


def create_bar_plot(df, output_dir):
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
    plt.savefig(f"{output_dir}/terms_frequency_bar_chart.png", dpi=600)


def create_word_cloud(term_counter, output_dir):
    wordcloud = WordCloud(
        width=800, height=400, background_color="white"
    ).generate_from_frequencies(term_counter)

    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Terms Word Cloud")
    plt.savefig(f"{output_dir}/terms_word_cloud.png", dpi=600)


def create_bubble_chart(df, output_dir):
    plt.figure(figsize=(14, 10))

    np.random.seed(42)
    x = np.random.rand(len(df)) * 100
    y = np.random.rand(len(df)) * 100

    plt.scatter(x, y, s=df["Frequency"] * 10, alpha=0.5, edgecolors="w", linewidth=0.5)

    for i, (term, freq) in enumerate(zip(df["Term"], df["Frequency"])):
        plt.text(x[i], y[i], term, ha="center", va="center", fontsize=10)

    plt.axis("off")
    plt.title("Terms Bubble Chart", fontsize=18, fontweight="bold")
    plt.savefig(f"{output_dir}/terms_bubble_chart.png", dpi=600)


def create_visualizations(input_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    term_counter, df = get_email_data(input_file)
    create_bar_plot(df, output_dir)
    create_word_cloud(term_counter, output_dir)
    create_bubble_chart(df, output_dir)


def main():
    fire.Fire(create_visualizations)


if __name__ == "__main__":
    main()
