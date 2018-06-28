#!/usr/bin/env python

from __future__ import print_function
import argparse
import logging
import os.path
import re
import yaml


NAME = 'scPBAL janitor'
DESCRIPTION = 'moves and renames scPBAL data directories to a common directory'
VERSION = '0.0.0'
CONFIG_PATH = 'config.yaml'
LOGLEVEL_CHOICES = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
LOGLEVEL_DICT = {'CRITICAL': logging.CRITICAL,
                 'ERROR': logging.ERROR,
                 'WARNING': logging.WARNING,
                 'INFO': logging.INFO,
                 'DEBUG': logging.DEBUG,}


def parse_runtime_arguments():
    """Parse runtime arguments using argparse.

    Returns:
        An object of type 'argparse.Namespace' containing the runtime
        arguments as attributes. See argparse documentation for more
        details.
    """
    parser = argparse.ArgumentParser(
        prog=NAME,
        description="%(prog)s - " + DESCRIPTION,)
    parser.add_argument(
        "directories",
        nargs='*',
        help="The directories to process and move",)
    parser.add_argument(
        "--loglevel",
        default="INFO",
        choices=LOGLEVEL_CHOICES,
        help="The logging loglevel",)
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + VERSION,)

    return parser.parse_args()


def parse_directory_name(directory_name):
    """Parses a directory name and returns a feature dictionary.

    Arg:
        directory_name: A string containing the name (not full path!) of
            a directory.
    Returns:
        A dictionary with keys 'id', 'date', 'extra' where the values
        are strings (in the case of no appropriate value for a key, an
        empty string will be used instead of None).
    """
    return dict()


def move_directory(source_path, destination_path):
    """Moves a directory.

    Args:
        source_path: A string containing the path to the directory to
            move.
        destination_path: A string containing the path of where to move
            the above directory.
    """
    pass


def main():
    """Main function for scPBAL janitor."""
    # Parse runtime args
    args = parse_runtime_arguments()

    # Set up the logger
    logging.basicConfig(format='%(levelname)s:%(message)s',
                        level=LOGLEVEL_DICT[args.loglevel])

    # Parse YAML config file in the same directory as this script
    logging.debug("loading YAML config file %s", CONFIG_PATH)

    script_directory_path = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_directory_path, CONFIG_PATH)

    with open(config_file_path, 'r') as yamlfile:
        config = yaml.load(yamlfile)

    # Process each directory passed in
    for path in args.directories:
        logging.debug("processing %s", path)

        # Validate that the path is in fact a directory
        logging.debug("validating that %s is a directory", path)

        if not os.path.isdir(path):
            # Not a directory. Move on to next directory.
            logging.error("%s is not a directory!", path)
            continue

        # Process the directory name
        old_directory_name = os.path.basename(path.rstrip('/'))

        logging.debug("parsing name %s", old_directory_name)
        name_features = parse_directory_name(old_directory_name)

        # Form the new path of the directory

        # Move the directory
        #logging.debug("moving %s to %s", path


if __name__ == '__main__':
    # Run the script
    main()
