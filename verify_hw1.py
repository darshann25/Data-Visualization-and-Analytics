#!/usr/bin/env python

""" verify_hw1.py - Confirm the zip file structure for a HW1 submission

Version: 0.1.2
Author: Jason Graffius

(c) 2019 Jason Graffius - All rights reserved

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import print_function
import zipfile as zf
import os.path as path

CORRECT_STRUCTURE = '''
HW1-{GT username}/
    Q1/
        movie_ID_name.csv
        movie_ID_sim_movie_ID.csv
        graph.png / graph.svg
        graph_explanation.txt
        metrics.txt
        script.py
    Q2/
        movie-cast.txt
        movie-name-score.txt
        movie-overview.txt
        Q2.SQL.txt
    Q3/
        index.html
        d3/
            d3.v3.min.js
    Q4/
        properties_clean.csv
        changes.json
        Q4Observations.txt
'''


def indent_level(line, indent_char=None):
    level = 0

    for char in line:
        if not char.isspace():
            return level, indent_char
        if indent_char is None:
            if char == ' ':
                indent_char = ' '
            elif char == '\t':
                indent_char = '\t'
            else:
                raise ValueError('Indent must be either space or tab')
        if char == indent_char:
            level += 1
        else:
            raise ValueError('Do not mix spaces and tabs')

    return level, indent_char


def checklist_entry(parents, line):
    entry = ''

    for _, name in parents:
        entry += name

    alternates = tuple(entry + alt.strip() for alt in line.split('/') if alt.strip() != '')
    return alternates


def pop_parents(parents, indent):
    while len(parents) > 0:
        parent_indent, name = parents.pop()

        if parent_indent < indent:
            raise ValueError('Indent was reduced, but not equal to or less than previous!')
        elif parent_indent > indent:
            continue
        else:
            return


def build_checklist(structure):
    """Build a list of file paths from the correct structure"""
    current_indent = None
    indent_char = None
    last = None
    parents = []
    checklist = list()

    for line in structure.splitlines():
        if not line.split():
            continue

        if current_indent is None:
            current_indent, indent_char = indent_level(line)

        indent, _ = indent_level(line, indent_char)
        line = line[indent:].rstrip()

        if indent > current_indent:
            parents.append(last)
            checklist.append(checklist_entry(parents, line))
        elif indent < current_indent:
            pop_parents(parents, indent)
            checklist.append(checklist_entry(parents, line))
        else:
            checklist.append(checklist_entry(parents, line))

        current_indent = indent
        last = indent, line

    return checklist


class ZipNode:
    def __init__(self, name, parent=None):
        self.parent = parent
        self.name = name
        self.children = list()

    def path(self):
        reverse_path = list()

        node = self
        while node:
            reverse_path.append(node.name)
            node = node.parent

        while '' in reverse_path:
            reverse_path.remove('')

        return reverse_path[::-1]

    def __repr__(self):
        return "<ZipNode '{}' with '{}' children>".format(
            self.name,
            len(self.children)
        )


def tree_to_ziplist(node):
    ziplist = list()
    frontier = [node]

    while frontier:
        node = frontier.pop()
        frontier.extend(node.children[::-1])

        fullpath = '/'.join(node.path())
        if fullpath:
            ziplist.append(fullpath)

    return ziplist


def build_ziptree(filepath):
    root = ZipNode('')

    with zf.ZipFile(filepath, mode='r') as archive:
        for name in archive.namelist():
            parts = name.split('/')
            parent = root
            for part in parts:
                if not part:
                    continue

                for sibling in parent.children:
                    if part == sibling.name:
                        parent = sibling
                        break
                else:
                    node = ZipNode(part, parent)
                    parent.children.append(node)
                    parent = node

    return root


def build_ziplist(filepath):
    return tree_to_ziplist(build_ziptree(filepath))


def find_in_ziplist(entry, ziplist):
    other_locations = list()
    for alternate in entry:
        alt_basename = alternate.split('/')[-1]
        for zipfile in ziplist:
            if zipfile == alternate:
                return True, None
            
            zip_basename = zipfile.split('/')[-1]
            if zip_basename == alt_basename:
                other_locations.append(zipfile)
    
    return False, other_locations


def check_checklist(checklist, ziplist):
    missing = list()
    wrong_locations = dict()
    for entry in checklist:
        found, other_locations = find_in_ziplist(entry, ziplist)
        if not found:
            missing.append(entry)
            if other_locations:
                wrong_locations[entry] = other_locations
    
    return missing, wrong_locations


def main(args):
    if len(args) != 2:
        print('Usage: python verify_hw1.py <gt-username> <file-path>')
        exit(1)

    username, filepath = args
    print()

    base = path.basename(filepath)
    if base != 'HW1-{gt_username}.zip'.format(gt_username=username):
        print('Zip file name is not correct! Should be of the form HW1-{GT username}.zip')
        print()
        exit(1)

    checklist = list()
    try:
        checklist = build_checklist(CORRECT_STRUCTURE)
    except ValueError as e:
        print('Error in folder structure template:')
        print('    ' + str(e) + '!')
        print()
        exit(1)

    ziplist = list()
    try:
        ziplist = build_ziplist(filepath)
    except FileNotFoundError:
        print('Could not find the zip file! Check the path given:')
        print('    ' + filepath)
        print()
        exit(1)

    checklist = [tuple(alt.format(**{'GT username': username}) for alt in entry) for entry in checklist]
    
    missing, wrong_locations = check_checklist(checklist, ziplist)
    
    if missing:
        print('Missing or mislocated files from {}:'.format(filepath))
        
        for entry in missing:
            if len(entry) == 1:
                print('  - /' + entry[0])
            else:
                print('  - /' + entry[0] + ' OR')
                for alt in entry[1:-1]:
                    print('    ' + alt + ' OR')
                print('    /' + entry[-1])
            
            if entry in wrong_locations:
                print('     + Found in another location:')
                for wrong_location in wrong_locations[entry]:
                  print('       - /{}'.format(wrong_location))
    
    else:
        print('Zip file contains all necessary files!')
    
    print()


if __name__ == '__main__':
    import sys

    main(sys.argv[1:])
