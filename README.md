# Clear Jupyter notebook output on commit

Removes cell numbers and output from IPython notebooks added to a git repository,
but leaves the files unchanged.

__Note: this only works for notebook versions >= 3__

# Install

1. Clone or download this repository. Let's assume you clone it to:

        ~/.config/git/dropoutput/

2. Make sure the `drop_ipynb_output.py` script is executable, e.g.:

        chmod a+x ~/.config/git/dropoutput/drop_ipynb_output.py

3. Add a [git filter](https://git-scm.com/book/en/v2/Customizing-Git-Git-Attributes) for
files with .ipynb extensions. Add this to your git attributes file (usually located in
`~/.config/git/attributes`):

        *.ipynb  filter=clean_ipynb

4. Connect the `drop_ipynb_output.py` script to the filter:

        git config --global filter.clean_ipynb.clean "~/.config/git/dropoutput/drop_ipynb_output.py %f"
        git config --global filter.clean_ipynb.smudge cat

# Configuration

By default, this script will tell git to ignore prompt numbers and
cell output when adding any .ipynb file to a git repositorie. Note that the
notebook files themselves are *not* changed, this script just filters
out the outputs before adding and committing with git.

This default behavior can be changed either on a notebook-by-notebook
basis, or for entire paths. To include output for a single notebook, modify
the metadata of the notebook (Edit -> Edit Notebook Metadata in the menu bar)
and add this line to the metadata:

    "git" : { "clear_outputs" : false }

To include output for any notebook that matches a given glob pattern (e.g.,
for an entire path), you can create and add paths to the file:
~/.config/git/clean_ipynb_ignore. For example, to include output for all
notebooks in ~/projects/notebooks that start with "demo", add a line to
the ignore file with:

    ~/projects/notebooks/demo*

# Acknowledgements

This code was inspired by [this blog post](http://pascalbugnion.net/blog/ipython-notebooks-and-git.html).
