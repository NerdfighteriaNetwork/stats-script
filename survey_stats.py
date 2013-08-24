#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
import copy

KEYS = [
          'timestamp',
          'first',
          'frequency',
          'referrer',
          'channels',
          'BNC',
          'registered',
          'vHost',
          'gender',
          'age',
          'continent',
          'welcomed',
          'ops',
          'uncomfortable',
          'conflict',
          'kicked',
          'banned',
          'why',
          'haveintroduced'
          'havebrought',
          'mightintroduce',
          'approachableboard',
          'unapproachable-why',
          'mod-sat',
          'mod-sat-why',
          'voted',
          'run',
          'terms',
          'how-we-vote',
          'op-guidelines',
          'suggested',
          'would-suggest',
          'important',
          'best',
          'worst',
          'improve',
          'how-doing',
          'comments',
         ]

SOURCES = (
           'Reddit',
           'The Ning',
           'Social Media',
           'Search engine (Google, Yahoo, etc.)',
           'Nerdfighter Gathering',
           'Friends / Family',
           'Found by accident',
           'other',
          )

#Keys, mapped to acceptable values
# '_other' is a special value for custom fields
VALUES = {
    'referrer': SOURCES,
    'age': ('13-17', '18-21', '22-30', '31-40', '41+', '_other'),
    'gender': ('Male', 'Female', '_other'),
    'channels': ('YourPants', 'Tech', 'Sexytimes', 'Minecraft', 'Adult',
        'YourPants-nl', 'DnD', 'Gaming', 'Peersupport', 'Radio', 'Spoonies',
        '_other'),
    'continent': ('North America', 'South America', 'Europe', 'Africa', 'Asia',
                    'Oceania'),
    'why': ('Friends', 'Chatting about fandoms', 'Chatting about Nerdfighteria',
        'Chatting about general things', 'Meeting new people', 'Trolling'),
    'first': ('Within this week', 'Within this month',
        'Within the last 6 months', 'Within the last 12 months',
        'I’ve been around for longer than a year'),
    'frequency': ('There’s a log out button?', 'Daily', 'Weekly', '_other'),
    }

def main(argv=sys.argv):
    data = []
    with open(argv[1]) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=KEYS)
        reader.next()  # throw away column headers
        #Read the whole file, so we can go over it a few times
        for row in reader:
            for key in VALUES:
                if row[key] not in VALUES[key]:
                    row[key] = '_other'
            data.append(row)

    tables = (
        mapper('age', 'referrer', 'Age vs. source'),
        mapper('gender', 'referrer', 'Gender vs. source'),
        mapper('channels', 'referrer', 'Channel vs. source'),
        mapper('continent', 'referrer', 'Location vs. source'),
#        mapper('reason', 'referrer', 'Reason vs. source'),
#        mapper('age', 'reason', 'Age vs. reason'),
        )

    for row in data:
        for table in tables:
            increment(table, row)

    for table in tables:
        print
        printout(table)


def printout(table):
    mapping, xs, ys, name = table
    xs = VALUES[xs]
    ys = VALUES[ys]
    print name + ',' + ','.join('"'+x+'"' for x in xs)
    for y in ys:
        print '"' + y + '",' + ','.join(str(mapping[y][x]) for x in xs)

def mapper(xs, ys, name):
    x_counts = {x: 0 for x in VALUES[xs]}
    d = {y: copy.deepcopy(x_counts) for y in VALUES[ys]}
    return (d, xs, ys, name)


def increment(table, row):
    mapping, xs, ys, _ = table
    for y in VALUES[ys]:
        for x in VALUES[xs]:
            if x in row[xs] and y in row[ys]:
                mapping[y][x] += 1

if __name__ == '__main__':
    main()
