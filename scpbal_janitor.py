#!/usr/bin/env python

from __future__ import print_function
import argparse
import logging
import os.path
import re
import shutil
import sys
import yaml


# Program info
NAME = 'scPBAL janitor'
DESCRIPTION = 'moves and renames scPBAL data directories to a common directory'
VERSION = '0.0.0'

# Relative path to config file
CONFIG_PATH = 'config.yaml'

# Logging stuff
LOGLEVEL_CHOICES = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
LOGLEVEL_DICT = {'CRITICAL': logging.CRITICAL,
                 'ERROR': logging.ERROR,
                 'WARNING': logging.WARNING,
                 'INFO': logging.INFO,
                 'DEBUG': logging.DEBUG,}

# Regex to match features of a directory name: this is based on the
# directory names I've encountered so far, so it's as complicated and
# exhausted as it needs to be, but not more than that.
ID_REGEX = r'(?:^|[-_])(px\d{4,})(?:$|[-_])'
DATE_REGEX = r'(?:^|[-_])(\d{8})(?:$|[-_])'


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
        help="the directories to process and move",)
    parser.add_argument(
        "--directories-files",
        nargs='*',
        default=[],
        help="files containing directory paths to read from",)
    parser.add_argument(
        "--loglevel",
        default="INFO",
        choices=LOGLEVEL_CHOICES,
        help="the logging loglevel",)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="run the script but don't move any files")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s " + VERSION,)

    return parser.parse_args()


def read_lines_from_file(file_path):
    """Reads lines from a file, skipping lines that start with #.

    Arg:
        file_path: A string containing the path of the file to read.
    Returns:
        A list of strings containing the lines from the file, except the
        lines that start with '#'.
    """
    with open(file_path) as f:
        stripped_lines = [line.strip() for line in f]

    return [line for line in stripped_lines
            if len(line) and not line.startswith('#')]


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
    name_feature_dict = {'id': '', 'date': '', 'extra': ''}

    # Find the ID and date
    try:
        id_ = re.search(ID_REGEX, directory_name, flags=re.I).group(1)
        name_feature_dict['id'] = id_.lower()
    except AttributeError:
        id_ = ''

    try:
        date = re.search(DATE_REGEX, directory_name, flags=re.I).group(1)
        name_feature_dict['date'] = date
    except AttributeError:
        date = ''

    # Put the remaining stuff in extra, stripping away any outlying
    # useless characters and doubled boundary characters
    extra = directory_name.replace(id_, '').replace(date, '')
    extra = extra.strip(r'_-').replace('__', '_').replace('--', '-')
    name_feature_dict['extra'] = extra

    return name_feature_dict


def move_directory(source_path, destination_path):
    """Moves a directory.

    Args:
        source_path: A string containing the path to the directory to
            move.
        destination_path: A string containing the path of where to move
            the above directory.
    """
    shutil.move(source_path, destination_path)


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

    # Get a list of directories to process
    logging.debug("collecting directories to process")

    directory_paths = args.directories

    for directories_file in args.directories_files:
        logging.debug("collecting directories from file %s", directories_file)
        directory_paths += read_lines_from_file(directories_file)

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

        logging.debug("parsing directory name %s", old_directory_name)
        name_features = parse_directory_name(old_directory_name)

        if not name_features['id']:
            logging.error("failed to parse ID from directory %s",
                          old_directory_name)
            continue

        # Form the new path of the directory, which is, provided the
        # features exist, {id}_{date}_{extra}
        new_directory_name = name_features['id']

        if name_features['date']:
            new_directory_name += '_' + name_features['date']

        if name_features['extra']:
            new_directory_name += '_' + name_features['extra']

        try:
            new_directory_path = os.path.join(
                config['home_scpbal_directory'],
                new_directory_name,)
        except KeyError:
            logging.critical("'home_scpbal_directory' not defined in config")
            logging.critical("aborting now")
            sys.exit(1)

        # Move the directory
        logging.debug("moving %s to %s", path, new_directory_path)

        if os.path.exists(new_directory_path):
            # The path we want to move to already exists!
            logging.error("%s already exists", new_directory_path)
            continue

        if not args.dry_run:
            move_directory(path, new_directory_path)


if __name__ == '__main__':
    # Run the script
    main()
