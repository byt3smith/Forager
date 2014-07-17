#!/usr/bin/env python
__author__ = 'pendrak0n'
#
# Main
#

import argparse
import os
import hunt
from feeds import FeedModules
from tools import extract
from sys import exit
from threading import Thread


def run_modules():
    x = FeedModules()

    for i in dir(x):
        if i.startswith('_'):
            pass
        elif callable:
            mod=getattr(x, i)
            t = Thread(target=mod)
            t.start()
        else:
            pass


def ensure_dir():
    folder = 'intel'
    if not os.path.exists(folder):
        os.makedirs(folder)
        print '[+] Created new directory: intel'


def main():
    feedmods = FeedModules()
    ensure_dir()
    os.chdir('intel')
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--feeds", type=str, choices=['list', 'update'], help="Manipulates intelligence feeds\n\
    List - Show list of current feeds to update individually\n\
    Update - Update all feeds")
    parser.add_argument('--hunt', action="store_true", help='Searches through the intel dir for matches')
    parser.add_argument('-s', type=str, nargs='?', help="Accepts a single IP address")
    parser.add_argument('-f', type=str, nargs='?', help="Receives a file of indicators to search through.")
    parser.add_argument("--extract", type=str, nargs=1, help="Extracts indicators from a given file")

    args = parser.parse_args()

    if args.hunt:
        if args.s:
            hunt.single_search(args.s)
        elif args.f:
            hunt.search_intel(args.f)

    elif args.feeds == 'update':
        print '[*] Updating all feeds'
        run_modules()

    elif args.feeds == 'list':
        print '[*] Please select feed to update:'
        feed_list = dir(FeedModules)
        newlist = []
        feedcount = 1
        for feed in feed_list:
            if "_update" in feed:
                newlist.append(feed)
                print str(feedcount)+'. '+feed
                feedcount += 1
            else:
                pass

        print '\n'
        choice = raw_input('Select feed by numerical ID (1-%d)\n> ' % (len(newlist)))
        if int(choice) in range(1, len(newlist) + 1):  # condition to check if proper feed was selected.
            mod = newlist[int(choice) - 1]   # Using choice number to locate item in the feed list
            methodToCall = getattr(feedmods, mod)  # saving function to call with newlist item as variable
            methodToCall()
        else:
            print '[-] Invalid option. Exiting...'
            exit(0)

    elif args.extract:
        os.chdir('../')
        filename = args.extract[0]
        print '[*] Extracting indicators from %s' % filename
        extract(filename)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
