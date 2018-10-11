#!/usr/bin/python
import sys
import re
import json

def strip_tabs(record):
    while "\t" in record:
        pos = record.find("\t")
        spaces = 8 - (pos % 8)
        record = record.replace("\t", " " * spaces, 1)
    return record

def process_dual_freq(record):
    # 1-24 Frequency, either single or start end
    # 25-64 Description
    # 65-83 Location
    # 84-88 Modulation (may encroach on location field)
    # 89-101 reporter
    # 102-109 date of report
    # 110- optional notes field
    frequencies = record[0:24]
    match = re.match("^([0-9]+\.[0-9]+)\s+([0-9]+\.[0-9]+)", frequencies)
    start_freq = match.group(1)
    end_freq = match.group(2)
    return process_record(record, start_freq, end_freq)

def process_single_freq(record):
    # 1-24 Frequency, either single or start end
    # 25-64 Description
    # 65-83 Location
    # 84-88 Modulation (may encroach on location field)
    # 89-101 reporter
    # 102-109 date of report
    # 110- optional notes field
    frequencies = record[0:24]
    match = re.match("^([0-9]+\.[0-9]+)\s*", frequencies)
    start_freq = match.group(1)
    end_freq = ""
    return process_record(record, start_freq, end_freq)

def process_record(record, start_freq, end_freq):
    description = record[24:64].rstrip()
    match = re.match("^(.*)\s+(\S+)\s*$", record[64:88])
    location = match.group(1).rstrip()
    modulation = match.group(2)
    reporter = record[88:101].rstrip()
    date = record[101:109]

    if len(record) > 109:
        notes = record[109:].lstrip()
    else:
        notes = ""
    return {"start_freq": start_freq, "end_freq": end_freq, "description": description, "location": location,
            "modulation": modulation, "reporter": reporter, "date": date, "notes": notes}

def process_airport(record):
    # 1-8 Airport code
    # 9-24 Airport name
    # 25-48 Purpose
    # 49-58 Frequency
    # 59-63 Modulation
    # 64-72 Reporter
    airport_code = record[0:8].rstrip()
    airport_name = record[8:24].rstrip()
    purpose = record[24:48].rstrip()
    frequency = record[48:58].rstrip()
    modulation = record[58:63].rstrip()
    reporter = record[63:72].rstrip()
    return {"airport_code": airport_code, "airport_name": airport_name, "purpose": purpose, "frequency": frequency,
            "modulation": modulation, "reporter": reporter}

# Compile the regular expressions we will use
single_freq_re = re.compile("^[0-9]+\.[0-9]+\s*")
dual_freq_re = re.compile("^[0-9]+\.[0-9]+\s+[0-9]+\.[0-9]+\s*")
airport_re = re.compile("^EG[A-Z]{2}\s+")

filename = sys.argv[1]

# Open files for output and reject
reject_file = open(filename + ".reject", "w")
freq_file = open(filename + ".freq.json", "w")
airport_file = open(filename + ".airport.json", "w")


with  open(filename,"r") as raw_file:
    for line in raw_file:
        line = line.rstrip()

        # Translate tabs in to spaces to create fixed-width fields
        if "\t" in line:
            line = strip_tabs(line)

        # Use regex to match the record type or reject the line
        if dual_freq_re.match(line[0:24]):
            freq_file.write(json.dumps(process_dual_freq(line)) + "\n")
        elif single_freq_re.match(line[0:24]):
            freq_file.write(json.dumps(process_single_freq(line)) + "\n")
        elif airport_re.match(line):
            airport_file.write(json.dumps(process_airport(line)) + "\n")
        else:
            reject_file.write(line + "\n")

# Close the output file handles
reject_file.close()
freq_file.close()
airport_file.close()
