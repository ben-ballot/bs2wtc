#!/usr/bin/env python3

#
# Author: Benjamin Allot
#

import argparse
import logging
import sys

import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)


def configure_logging(args):
    """Configure the logging.

    :param :py:class:argparse.ArgumentParser args: Arguments provided
    """

    def check_log_level(log_level):
        """Check that the logleve is a valid one."""
        log_level_attr = getattr(logging, log_level.upper(), None)
        if not isinstance(log_level_attr, int):
            raise ValueError("Invalid log-level level: {0}".format(log_level))
        return log_level_attr

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    logger.setLevel(logging.DEBUG)
    log_level = check_log_level(args.log_level)

    # Configure console handler only if we're in a tty
    if sys.stdout.isatty():
        console = logging.StreamHandler()
        console.setLevel(log_level)
        console.setFormatter(formatter)
        logger.addHandler(console)
    else:
        if not args.log_file:
            print("Not in a tty and no log file configured. Are you kidding me ?")
            sys.exit(1)
    if args.log_file:
        log_file_level = check_log_level(args.log_file_level)
        logfile_handler = logging.FileHandler(args.log_file)
        logfile_handler.setLevel(log_file_level)
        logfile_handler.setFormatter(formatter)
        logger.addHandler(logfile_handler)


def parse_args():
    """Parse the arguments provided to the CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-level", action="store", help="Logging level", default="WARNING")
    parser.add_argument("--log-file", action="store", help="Log file")
    parser.add_argument("--log-file-level", action="store", help="File logging level", default="INFO")
    parser.add_argument("--dry-run", action="store_true", default=False,
                        help="Do not execute any action that change behavior")

    parser.add_argument("-r", "--roster", action="store", help="Battlescribe Roster file")
    return parser.parse_args()


def open_roster(roster_file_path: str) -> None:
    """Open the roster file and display WTC list."""

    with open(roster_file_path) as roster:
        roster_content = roster.read()

    ns = {"bs": "http://www.battlescribe.net/schema/rosterSchema"}
    root = ET.fromstring(roster_content)
    print(root.tag, root.attrib)
    print(root.findall("./bs:costs", ns))
    print(root.findall("./bs:costLimits", ns))
    print(root.findall("./bs:forces", ns))

    return root


def display_header(root):
    """Display the header."""

    tmpl = """
+++++++++++++++++++++++++++++++++++++++++++++++
+ PLAYER : {player}
+ ARMY MAIN FACTION : {faction}
+ TOTAL COMMAND POINTS : {total_cp}
+ TOTAL ARMY POINTS : {army_points}
+ TOTAL PL POINTS : {army_pl}
+ TOTAL CABAL POINTS : {cabal_points}
+ ARMY FACTIONS USED : {factions_used}
+ TOTAL REINFORCEMENT POINTS : {reinforcement_points}
+++++++++++++++++++++++++++++++++++++++++++++++"""

    #faction = root.findall("./forces/force[@catalogueName]")
    faction = root.findall("./forces/")
    print(faction)
    # print(faction.get("catalogueName"))


if __name__ == "__main__":
    args = parse_args()
    configure_logging(args)
    root = open_roster(args.roster)
    display_header(root)
