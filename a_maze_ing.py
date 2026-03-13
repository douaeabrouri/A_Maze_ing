#!/usr/bin/env python3
import sys
from typing import Optional

def parsing(filepath: str) -> None:
    raw: dict = {}
    requierd_keys: list = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"]
    """step 1 : open the file"""

    try:
        lines: list = []
        with open("config.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError as e:
        print(f"ERROR: config file '{filepath}' not found.")
        return None
    except OSError as e:
        print(f"Error reading config file: {e}")
    """step 2 : parse lines"""
    
    for line_num, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            print(f"Error: line {line_num} is invalid (no '=' found): '{line}'")
            return None
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if not key or not value:
            print(f"Error: line {line_num} has an empty key or value.")
            return None
        raw[key] = value
    """step 3: check requierd keys"""

    for key in requierd_keys:
        if key not in raw:
            print(f"Error: missing required key '{key}' in config file.")
            return None
    """step 4: valiate each value"""

    check_requierd: dict = {}
    try:
       check_requierd["WIDTH"] = int(raw("WIDTH"))
       if check_requierd["WIDTH"] <= 0:
           raise ValueError
    except ValueError as e:
        print(f"ERROR: {e}")
        
    try:
        check_requierd["HEIGHT"] = int(raw("HEIGHT"))
        if check_requierd["HEIGHT"] <= 0:
            raise ValueError
    except ValueError as e:
        print(f"ERROR: {e}")

    try:
        i, j = raw("ENTRY").split(',')
        check_requierd["ENTRY"] = (int(i.strip()), int(j.strip()))
    except ValueError as e:
        print(f"ERROR: {e}")
    if not (0 <= check_requierd["ENTRY"][0] < check_requierd["WIDTH"] and
            0 <= check_requierd["ENTRY"][1] < check_requierd["HEIGHT"]):
            print(f"ERROR: The value of ENTRY that take false")
            return None
    
    try:
        x, y = raw("EXIT").split(',')
        check_requierd["EXIT"] = (int(x.strip()), int(y.strip()))
    except ValueError as e:
        print(f"ERROR: {e}")
    if not (0 <= check_requierd["EXIT"][0] < check_requierd["WIDTH"] and
            0 <= check_requierd["EXIT"][1] < check_requierd["HEIGHT"]):
            print(f"ERROR: The value of EXIT that take false")
            return None
 
    if check_requierd["EXIT"] == check_requierd["ENTRY"]:
       print("Error: ENTRY and EXIT must be different cells.")
       return None

    check_requierd["OUTPUT_FILE"] = raw["OUTPUT_FILE"]
    if not check_requierd["OUTPUT_FILE"]:
        print("Error: OUTPUT_FILE cannot be empty.")
        return None

    if "SEED" in raw:
        try:
            check_requierd["SEED"] = int(raw["SEED"])
        except ValueError as e:
            print(f"Error: SEED must be an integer, got '{raw['SEED']}'.")
            return None
    else:
        check_requierd["SEED"] = None
    
if __name__ == "__main__":
    parsing("config.txt")