import pandas as pd
from pathlib import Path
import argparse
import os
import logging
import pycountry
import re


def remove_first_trailing_zero(s):
    s = str(s)
    if s[0] == "0":
        s = s[1:]
    return s


def split_street_number(s):
    s = re.split(
        r"^(\d*[\w\d '\/\\\-\.]+?)[,\s]+((?:\d+)\s*(?:[\w\d\/]*(?:\s*[-+]\s*[\w\d\-+\/]*)?))$",
        s,
    )
    s = list(filter(None, s))
    street = s[0]
    number = " ".join(s[1:])
    return pd.Series([street, number])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Converts Bandcamp CSV to Hermes CSV")
    parser.add_argument("--file", required=True)
    args = parser.parse_args()

    filename = Path(args.file)

    if not os.path.exists(filename):
        raise Exception(f"File {filename} does not exist!")
    df = pd.read_csv(filename, encoding="utf-16", dtype=str)
    logging.info(f"Imported file {filename}")

    hermes_df = pd.DataFrame(
        columns=[
            "First Name",
            "Last Name",
            "Additional Info",
            "Street",
            "Number",
            "Zip",
            "City",
            "Area",
            "Country",
            "Phone Pre",
            "Phone",
            "Email",
        ]
    )

    hermes_df["City"] = df["ship to city"]
    hermes_df["Zip"] = df["ship to zip"]
    hermes_df["Country"] = df["ship to country"].apply(
        lambda row: pycountry.countries.search_fuzzy(row)[0].alpha_3
    )
    hermes_df[["Street", "Number"]] = df["ship to street"].apply(
        lambda row: split_street_number(row)
    )
    hermes_df["Phone Pre"] = (
        df["buyer phone"]
        .str.split(pat=" ", expand=True)
        .iloc[:, 0]
        .apply(lambda row: row.replace("+", "00"))
    )
    hermes_df["Phone"] = (
        df["buyer phone"]
        .str.split(pat=" ", expand=True)
        .iloc[:, 1]
        .apply(lambda row: remove_first_trailing_zero(row))
    )
    hermes_df["Email"] = df["buyer email"]

    hermes_df["First Name"] = (
        df["ship to name"].str.split(pat=" ", expand=True).iloc[:, 0]
    )
    hermes_df["Last Name"] = (
        df["ship to name"].str.split(pat=" ", expand=True).iloc[:, 1]
    )

    logging.info(f"Converted File of {hermes_df.shape[0]} lines")

    new_filename = Path(filename.parent, f"{filename.stem}_hermes{filename.suffix}")
    hermes_df.to_csv(
        new_filename, encoding="utf-16", index=False, header=False, sep=";"
    )

    logging.info(f"Saved new file to {str(new_filename)}")
