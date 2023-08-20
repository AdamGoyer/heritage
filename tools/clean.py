#!/usr/bin/env python

import nbformat
from nbdev.export import *
from nbdev.clean import *
from fastcore.all import *

# Regular expressions to match header cells, clean cells, and questionnaire sections
_re_header = re.compile(r'^#+\s+\S+')
_re_clean = re.compile(r'^\s*#\s*clean\s*')
_re_questionnaire = re.compile(r'^#+\s+Questionnaire')

# Check if the given cell is a header cell
def is_header_cell(cell): return _re_header.search(cell['source']) is not None

# Check if the given cell is a clean cell
def is_clean_cell(cell): return _re_clean.search(cell['source']) is not None

# Find the index of the questionnaire section in the notebook cells
def get_stop_idx(cells):
    i = 0
    while i < len(cells) and _re_questionnaire.search(cells[i]['source']) is None: i += 1
    return i

# Remove specific tags from the cell source (e.g., id, caption, etc.)
def clean_tags(cell):
    if is_header_cell(cell): return cell
    for attr in ["id", "caption", "alt", "width", "hide_input", "hide_output", "clean"]:
        cell["source"] = re.sub(r'#\s*' + attr + r'.*?($|\n)', '', cell["source"])
    return cell

# Process a given notebook file, cleaning tags and filtering cells
def proc_nb(fname, dest):
    nb = read_nb(fname)
    i = get_stop_idx(nb['cells'])
    nb['cells'] = [clean_tags(c) for j, c in enumerate(nb['cells']) if
                   c['cell_type'] == 'code' or is_header_cell(c) or is_clean_cell(c) or j >= i]
    clean_nb(nb, clear_all=True)
    with open(dest / fname.name, 'w') as f: nbformat.write(nb, f, version=4)

# Process all notebook files in the specified path
def proc_all(path='.', dest_path='clean'):
    path, dest_path = Path(path), Path(dest_path)
    fns = [f for f in path.iterdir() if f.suffix == '.ipynb' and not f.name.startswith('_')]
    for fn in fns: proc_nb(fn, dest=dest_path)

# Main entry point: process all notebooks in the current directory
if __name__ == '__main__': proc_all()
