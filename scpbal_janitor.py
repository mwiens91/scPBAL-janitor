#!/usr/bin/env python

from __future__ import print_function
import argparse
import logging
import os
import re
import sys


# Relative path to the config file
CONFIG_PATH = 'config.yaml'


def parse_runtime_arguments():
    """Parse runtime arguments using argparse.

    Returns:
        An object of type 'argparse.Namespace' containing the runtime
        arguments as attributes. See argparse documentation for more
        details.
    """
    pass


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
    pass


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
    pass


if __name__ == '__main__':
    main()
