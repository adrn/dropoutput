# Drop IPython notebook output

Remove cell numbers and output from IPython notebooks when adding to a git repository.

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

# Acknowledgements

This code was inspired by [this blogpost](http://pascalbugnion.net/blog/ipython-notebooks-and-git.html).
