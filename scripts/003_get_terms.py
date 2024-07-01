import configparser
import json
import os
import re
import time
from concurrent.futures import ProcessPoolExecutor

import fire
import jsonlines
import psutil
import tqdm

import ate_lib.ate as ate


def process_file(
    in_dataset_file,
    config,
    in_dir_dataset,
    out_dir_terms,
    stopwords,
    min_term_words,
    min_term_length,
    term_patterns,
    trace,
    log_file_path,
):
    t2 = time.time()
    in_dataset = os.path.join(in_dir_dataset, in_dataset_file)

    def log(msg):
        s = json.dumps(msg)
        print(s)
        f = open(log_file_path, "a")
        f.write(s)
        f.write("\n")
        f.close()

    log(in_dataset)
    if not os.path.isfile(in_dataset):
        return

    with open(in_dataset, "r") as fp:
        doc_txt = fp.read()

    doc_txt = doc_txt.replace("\ufffd", "_")
    doc_txt = re.sub(r"et +al\.", "et al", doc_txt)
    doc_txt = re.split(r"[\r\n]", doc_txt)

    term_extractor = ate.TermExtractor(
        stopwords=stopwords,
        term_patterns=term_patterns,
        min_term_words=min_term_words,
        min_term_length=min_term_length,
    )
    terms = term_extractor.extract_terms(doc_txt, trace=trace)
    log("len(terms)=" + str(len(terms)))
    if trace:
        log("Term extraction finished")

    c_values = term_extractor.c_values(terms, trace=trace)

    out_terms_file = os.path.join(out_dir_terms, "T" + in_dataset_file[1:])
    with jsonlines.open(out_terms_file, mode="w") as writer:
        for cv in c_values:
            writer.write(cv)
    t1 = time.time()
    log(
        (
            "time",
            t1 - t2,
        )
    )


def do_get_terms(
    config=None, in_dir_dataset=None, out_dir_terms=None, stopwords=None, trace=0
):
    t0 = time.time()

    conf = configparser.ConfigParser()
    conf.read_file(open(config))

    data_dir = conf.get("main", "data_dir")
    log_file_name = "015_ate_get_terms.log"
    log_file_path = os.path.join(data_dir, log_file_name)

    if not os.path.isdir(out_dir_terms):
        os.mkdir(out_dir_terms)

    min_term_words = int(conf.get("ate", "min_term_words"))
    min_term_length = int(conf.get("ate", "min_term_length"))
    term_patterns = json.loads(conf.get("ate", "term_patterns"))
    trace = int(trace) == 1

    with open(stopwords, "r") as f_stopwords:
        stopwords = [r.strip() for r in f_stopwords.readlines() if len(r.strip()) > 0]

    in_dataset_files = sorted(
        [f for f in os.listdir(in_dir_dataset) if f.lower().endswith(".txt")]
    )

    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(
                process_file,
                in_dataset_file,
                config,
                in_dir_dataset,
                out_dir_terms,
                stopwords,
                min_term_words,
                min_term_length,
                term_patterns,
                trace,
                log_file_path,
            )
            for in_dataset_file in in_dataset_files
        ]
        for future in tqdm.tqdm(futures):
            future.result()

    t1 = time.time()
    process = psutil.Process(os.getpid())
    # log(
    #     {
    #         "time": t1 - t0,
    #         "used RAM(bytes)": process.memory_info().rss  # in bytes
    #     }
    # )
    print("Finished processing")


if __name__ == "__main__":
    fire.Fire(do_get_terms)
