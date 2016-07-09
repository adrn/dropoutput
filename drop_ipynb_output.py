#!/usr/bin/env python

"""
Suppress output and prompt numbers for IPython notebooks included in git
repositories.

By default, this script will tell git to ignore prompt numbers and
cell output when adding ipynb files to git repositories. Note that the
notebook files themselves are *not* changed, this script just filters
out the outputs before adding and committing with git.

This default behavior can be changed either on a notebook-by-notebook
basis, or for entire paths. To include output for a single notebook, modify
the metadata of the notebook (Edit -> Edit Notebook Metadata in the menu bar)
and add this:

    "git" : { "suppress_output" : false }

to include output from that notebook. To include output for notebooks that
match a given glob pattern (e.g., for an entire path), you can create and
add paths to the file: ~/.config/git/clean_ipynb_ignore. For example, to
include output for all notebooks in ~/projects/notebooks that start with
"demo", add a line to the ignore file with:

    ~/projects/notebooks/demo*

See README.md for instructions on how to install this script.

"""

# Path to the ignore file
CLEAN_IPYNB_IGNORE_PATH = "~/.config/git/clean_ipynb_ignore"

# Standard library imports
import os
import sys
import json
import fnmatch

def dumpit(json_in):
    json.dump(json_in, sys.stdout, sort_keys=True, indent=1, separators=(",",": "))

# the git smudge filter will "cat" the notebook file contents and pip in to this script
nb = sys.stdin.read()
json_in = json.loads(nb)

# we use the clean filter to pass the name of the file in to this script as a command-line argument
nb_filename = os.path.abspath(sys.argv[1])

if os.path.exists(CLEAN_IPYNB_IGNORE_PATH): # if the clean_ipynb_ignore file exists
    with open(os.path.expanduser(CLEAN_IPYNB_IGNORE_PATH), "r") as f:
        for line in f.readlines():
            if line.strip(): # make sure the line is not empty
                if fnmatch.fnmatch(nb_filename, line) or \
                    os.path.samefile(os.path.dirname(nb_filename, line)):
                    # check if the nb filename matches any of the glob patterns
                    #   or is in an ignored directory
                    dumpit(json_in)
                    sys.exit(0)

# get the metadata block of the notebook
metadata = json_in.get("metadata", dict())

# by default, suppress output and line numbers
suppress_output = True
if "git" in metadata:
    if "suppress_outputs" in metadata["git"] and not metadata["git"]["suppress_outputs"]:
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

for cell in json_in["cells"]:
    clean(cell)

dumpit(json_in)
