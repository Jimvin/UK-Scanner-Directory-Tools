# UK-Scanner-Directory-Tools
Tools for making the UK scanner directory from http://ukscanningdirectory.co.uk/ machine readable

## main2json.py
This parses the main frequency directory text file and converts the records into JSON format.

`./main2json.py <source_filename>`

It creates 3 output files:
* source_filename.freq.json - records indexed by frequency
* source_filename.airports.json - records indexed by airport code
* source_filename.reject - records that don't match a known format
