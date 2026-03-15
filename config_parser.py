#!/usr/bin/env python3
from typing import Optional
import sys


def parsing(filepath: str) -> Optional[dict]:
    raw: dict = {}
    required_keys: list = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    # Step 1: open the file
    try:
        with open(filepath, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: config file '{filepath}' not found.")
        return None
    except OSError as e:
        print(f"Error reading config file: {e}")
        return None

    # Step 2: parse lines
    for line_num, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            print(f"Error: line {line_num} invalid (no '=' found): '{line}'")
            return None
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if not key or not value:
            print(f"Error: line {line_num} has an empty key or value.")
            return None
        raw[key] = value
    # Step 3: check required keys
    for key in required_keys:
        if key not in raw:
            print(f"Error: missing required key '{key}' in config file.")
            return None
    # Step 4: validate each value
    config: dict = {}
    try:
        config["WIDTH"] = int(raw["WIDTH"])
        if config["WIDTH"] <= 0:
            raise ValueError
    except ValueError:
        print(f"Error: WIDTH must be a positive integer, got '{raw['WIDTH']}'.")
        return None
    try:
        config["HEIGHT"] = int(raw["HEIGHT"])
        if config["HEIGHT"] <= 0:
            raise ValueError
    except ValueError:
        print(f"Error: HEIGHT must be positive integer, got '{raw['HEIGHT']}'.")
        return None
    try:
        i, j = raw["ENTRY"].split(",")
        config["ENTRY"] = (int(i.strip()), int(j.strip()))
    except ValueError:
        print(f"Error: ENTRY must be 'x,y' format, got '{raw['ENTRY']}'.")
        return None
    if not (
        0 <= config["ENTRY"][0] < config["WIDTH"]
        and 0 <= config["ENTRY"][1] < config["HEIGHT"]
    ):
        print(f"Error: ENTRY {config['ENTRY']} is outside maze bounds.")
        return None
    try:
        x, y = raw["EXIT"].split(",")
        config["EXIT"] = (int(x.strip()), int(y.strip()))
    except ValueError:
        print(f"Error: EXIT must be 'x,y' format, got '{raw['EXIT']}'.")
        return None
    if not (
        0 <= config["EXIT"][0] < config["WIDTH"]
        and 0 <= config["EXIT"][1] < config["HEIGHT"]
    ):
        print(f"Error: EXIT {config['EXIT']} is outside maze bounds.")
        return None
    if config["ENTRY"] == config["EXIT"]:
        print("Error: ENTRY and EXIT must be different cells.")
        return None
    config["OUTPUT_FILE"] = raw["OUTPUT_FILE"]
    if not config["OUTPUT_FILE"]:
        print("Error: OUTPUT_FILE cannot be empty.")
        return None
    if raw["PERFECT"].lower() == "true":
        config["PERFECT"] = True
    elif raw["PERFECT"].lower() == "false":
        config["PERFECT"] = False
    else:
        print(f"Error: PERFECT must be True or False, got '{raw['PERFECT']}'.")
        return None
    if "SEED" in raw:
        try:
            config["SEED"] = int(raw["SEED"])
        except ValueError:
            print(f"Error: SEED must be an integer, got '{raw['SEED']}'.")
            return None
    else:
        config["SEED"] = None
    return config


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 config_parser.py config.txt")
        sys.exit(1)
    result = parsing(sys.argv[1])
    if result:
        print("Config loaded successfully!")
        for k, v in result.items():
            print(f"  {k} = {v}")
    else:
        sys.exit(1)
