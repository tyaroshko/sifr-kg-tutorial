import json
import os

import fire
import tqdm


def load_concepts(file_path):
    with open(file_path, "r") as f:
        concepts = f.readlines()
    return [concept.strip() for concept in concepts]


def find_concepts_in_email(email_text, concepts):
    email_text = email_text.lower()
    return [concept for concept in concepts if concept.lower() in email_text]


def process_emails(concepts_file, input_dir, output_file):
    concepts = load_concepts(concepts_file)
    result = {}

    for filename in tqdm.tqdm(os.listdir(input_dir)):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            found_concepts = find_concepts_in_email(text, concepts)
            result[filename] = found_concepts

    result = dict(sorted(result.items()))

    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)

    print(f"Results have been written to {output_file}")


def main():
    fire.Fire(process_emails)


if __name__ == "__main__":
    main()

# concepts_file = "./conceptualization.txt"
# email_directory = "./data/clear_txts"
# output_file = "email_concepts_data.json"
# process_emails(concepts_file, email_directory, output_file)
