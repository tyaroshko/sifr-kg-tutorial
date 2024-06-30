import os
from concurrent.futures import ProcessPoolExecutor

import fire
import tqdm


def write_dataset(dataset_info):
    input_folder, output_folder, files, start_index, end_index, dataset_filename = (
        dataset_info
    )
    with open(dataset_filename, "w") as dataset_file:
        for j in range(start_index, end_index):
            with open(os.path.join(input_folder, files[j]), "r") as file:
                dataset_file.write(file.read())
    return f"Dataset created: {dataset_filename} containing {end_index - start_index} files"


def generate_datasets(input_folder, increment_size, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    files = [f for f in sorted(os.listdir(input_folder)) if f.endswith(".txt")]
    total_files = len(files)
    num_datasets = (total_files + increment_size - 1) // increment_size

    tasks = []
    for i in tqdm.tqdm(range(num_datasets)):
        start_index = i * increment_size
        end_index = min((i + 1) * increment_size, total_files)
        dataset_filename = os.path.join(output_folder, f"D{i:06d}.txt")
        tasks.append(
            (
                input_folder,
                output_folder,
                files,
                start_index,
                end_index,
                dataset_filename,
            )
        )

    with ProcessPoolExecutor() as executor:
        results = list(executor.map(write_dataset, tasks))
    for result in results:
        print(result)


def main():
    fire.Fire(generate_datasets)


if __name__ == "__main__":
    main()
