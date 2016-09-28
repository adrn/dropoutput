#!/usr/bin/env python

""" See README.md for instructions on how to install this script. """

# Standard library imports
import os
import sys
import json
import fnmatch

# Path to the ignore file
CLEAN_IPYNB_IGNORE_PATH = "~/.config/git/clean_ipynb_ignore"
CLEAN_IPYNB_IGNORE_PATH = os.path.expanduser(CLEAN_IPYNB_IGNORE_PATH)

def dumpit(json_in):
    json.dump(json_in, sys.stdout, sort_keys=True, indent=1, separators=(",",": "))

# the git smudge filter will "cat" the notebook file contents and pipe in to this script
nb = sys.stdin.read()
json_in = json.loads(nb)

# we use the clean filter to pass the name of the file in to this script as a command-line argument
nb_filename = os.path.abspath(sys.argv[1])

# by default, suppress output and line numbers
suppress_output = True

if os.path.isfile(CLEAN_IPYNB_IGNORE_PATH): # if the clean_ipynb_ignore file exists
    with open(os.path.expanduser(CLEAN_IPYNB_IGNORE_PATH), "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line: # make sure the line is not empty
                line = os.path.abspath(os.path.expanduser(line))
                if fnmatch.fnmatch(nb_filename, line):
                    # check if the nb filename matches any of the glob patterns
                    #   or is in an ignored directory
                    suppress_output = False
                    break

# get the metadata block of the notebook
metadata = json_in.get("metadata", dict())

if "git" in metadata:
    # 2nd bit in 'or' is for backwards compatibility
    for name in ["clear_outputs", "drop_outputs", "suppress_outputs"]:
        if name in metadata['git'] and not metadata['git'][name]:
            suppress_output = False

# exit early and return the file as-is if we shouldn't filter output cells
if not suppress_output:
    sys.stdout.write(nb)
    sys.exit(0)

def clean(cell):
    """ Remove the output from a cell and clear the execution count. """
    if "outputs" in cell:
        cell["outputs"] = []

    if "execution_count" in cell:
        cell["execution_count"] = None

try:
    for cell in json_in["cells"]:
        clean(cell)
except:
    # probably an old-style notebook
    pass

dumpit(json_in)
