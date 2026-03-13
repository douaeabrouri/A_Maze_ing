#!/usr/bin/env python3
import sys



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
    for line_num, line in lines[:]:
        line = line.strip()
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
    """step 4: valiate each value  """
    for key, value in raw[:]:
        if value == "WIDTH" and key < 0:
            print("Error the WIDTH must be positive number!!!")
            return None
        if value == 