import configparser
import json
import os
import time

import fire
import psutil

import ate_lib.cleartxt as cleartxt


def do_clear_txt(config=None, rawtxtdir=None, cleartxtdir=None):
    t0 = time.time()

    # read configuration file
    conf = configparser.ConfigParser()
    conf.read_file(open(config))

    data_dir = conf.get("main", "data_dir")
    log_file_name = "ate_clear_txts.log"
    log_file_path = os.path.join(data_dir, log_file_name)

    def log(msg):
        s = json.dumps(msg)
        print(s)
        f = open(log_file_path, "a")
        f.write(s)
        f.write("\n")
        f.close()

    # =====================================================
    # place to store extracted texts
    if cleartxtdir:
        clear_txt_dir = cleartxtdir
    else:
        clear_txt_dir = f"{data_dir}/clear_txts"

    if not os.path.isdir(clear_txt_dir):
        log(f"pdf dir {clear_txt_dir} not found. Creating")
        os.mkdir(clear_txt_dir)

    log(("clear_txt_dir", clear_txt_dir))

    # place to read raw texts
    if rawtxtdir:
        raw_txt_dir = rawtxtdir
    else:
        raw_txt_dir = f"{data_dir}/txts"
    log(("raw_txt_dir", raw_txt_dir))

    # read raw txt files
    raw_txt_files = sorted(
        [
            (raw_txt_dir, f)
            for f in os.listdir(raw_txt_dir)
            if os.path.isfile(os.path.join(raw_txt_dir, f))
            and f.lower().endswith(".txt")
        ]
    )
    log(raw_txt_files)
    for f in raw_txt_files:
        fpath_out = os.path.join(clear_txt_dir, f[1][:-4] + ".txt")
        log((raw_txt_dir, "/", f[1], "=>", fpath_out))
        ftxt = open(fpath_out, "w")
        try:
            file_content = cleartxt.clean_text(os.path.join(f[0], f[1]))
            ftxt.write(file_content)
        except TypeError as e:
            log(("error writing file ", fpath_out))
            log(str(e))
            log("\n\n")
        ftxt.close()
    t1 = time.time()
    log("finished")
    log(
        (
            "time",
            t1 - t0,
        )
    )
    process = psutil.Process(os.getpid())
    log(("used RAM(bytes)=", process.memory_info().rss))  # in bytes


if __name__ == "__main__":

    fire.Fire(do_clear_txt)
