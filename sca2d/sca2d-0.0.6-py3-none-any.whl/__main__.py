'''The entry point for SCA2D. This file runs when you run `sca2d` in terminal'''

import os
import sys
import argparse
from sca2d import Analyser

def parse_args():
    """
    This sets up the argumant parsing using the argparse module. It will automatically
    create a help message describing all options. Run `sca2d -h` in your terminal to see
    this description.
    """
    parser = argparse.ArgumentParser(description="SCA2D - A static code analyser for OpenSCAD.")
    parser.add_argument("file_or_dir_name",
                        metavar="<file_or_dir_name>",
                        type=str,
                        help="The .scad file to analyse or the directory to analyse.")
    parser.add_argument("--output-tree",
                        help="Output the parse tree to output.sca2d",
                        action="store_true")
    parser.add_argument("--colour",
                        help=("Use colour when outputting the warning messages."
                              "May not work as expected in all terminals."),
                        action="store_true")
    parser.add_argument("--verbose",
                        help=("Put SCA2D into verbose mode."),
                        action="store_true")
    return parser.parse_args()

def main():
    '''
    creates a sca2d analyser and then analyses the input file. Printing
    analysis to the screen
    '''
    args = parse_args()
    analyser = Analyser(verbose=args.verbose)
    if os.path.isfile(args.file_or_dir_name):
        
        parsed = analyser.analyse_file(args.file_or_dir_name,
                                    output_tree=args.output_tree,
                                    colour=args.colour)
    elif os.path.isdir(args.file_or_dir_name):
        parsed = True
        for root, dirs, files in os.walk(args.file_or_dir_name):
            for name in files:
                if name.endswith('.scad'):
                    scad_filename = os.path.join(root, name)
                    file_parsed = analyser.analyse_file(scad_filename,
                                  output_tree=args.output_tree,
                                  colour=args.colour)
                    parsed = parsed and file_parsed
        
    else:
        print("Cannot find file or directory!")
        sys.exit(-1)

    if parsed:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
