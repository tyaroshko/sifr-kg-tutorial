import os
import re
from datetime import datetime
from email.parser import Parser

import fire
import tqdm
from nltk.tokenize import sent_tokenize


def get_email_data(input_file):
    with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
        data = f.read()
    return data


def extract_emails(data):
    emails = re.split(r"From [^\s]+@[^\s]+ ", data)
    return emails[1:]


def preprocess_email(email):
    lines = email.split("\n")
    date_str = lines[0].strip()
    datetime_object = datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y")

    body = "\n".join(lines[1:])  # Exclude the date line
    sentences = sent_tokenize(body)
    formatted_body = "\n".join(sentences)

    return {
        "content": "Date: " + date_str + "\n" + formatted_body,
        "date": datetime_object,
    }


def save_emails(emails, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    emails.sort(key=lambda x: x["date"])

    for index, email in tqdm.tqdm(enumerate(emails, start=1)):
        filename = f"email_{index:04d}.txt"
        filepath = os.path.join(output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(email["content"])


def process_data(input_file, output_dir):
    email_data = get_email_data(input_file)
    emails = extract_emails(email_data)
    processed_emails = [preprocess_email(email) for email in emails]
    save_emails(processed_emails, output_dir)


def main():
    fire.Fire(process_data)


if __name__ == "__main__":
    main()
