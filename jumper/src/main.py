"""Entrypoint for the refactored project.

For now this runs the existing `jumper.py` so behavior is unchanged.
Run with: `python3 -m src.main` from the project root.
"""
import runpy
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
JUMPER_PATH = os.path.join(ROOT, 'jumper.py')

if __name__ == '__main__':
    if not os.path.isfile(JUMPER_PATH):
        print('jumper.py not found at', JUMPER_PATH)
        sys.exit(1)
    runpy.run_path(JUMPER_PATH, run_name='__main__')
