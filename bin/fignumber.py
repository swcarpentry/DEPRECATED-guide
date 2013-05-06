#!/usr/bin/env python

import sys
import re

#----------------------------------------

DEF_P = re.compile(r'<figure id="(f:[^"]+)">(\s+)<img\s+src="(.+)"\s+alt="(.+)"\s*/>(\s+)<figcaption>.+</figcaption>(\s+)</figure>',
                   re.MULTILINE)
DEF_T = '<figure id="%(id)s">%(ws_1)s<img src="%(src)s" alt="%(caption)s" />%(ws_2)s<figcaption>Figure %(num)s: %(caption)s</figcaption>%(ws_3)s</figure>'
REF_P = re.compile(r'<a href="#(f:[^"]+)">[^<]+</a>')
REF_T = '<a href="#%(id)s">Figure %(num)d</a>'

#----------------------------------------

def main(reader, writer):
    original = reader.read()
    values = get_defs(original)
    temp = subber(original, values, DEF_P, DEF_T)
    final = subber(temp, values, REF_P, REF_T)
    writer.write(final)

#----------------------------------------

def get_defs(original):
    matches = DEF_P.findall(original)
    result = {}
    for (num, m) in enumerate(matches):
        result[m[0]] = {
            'num'     : num+1,
            'id'      : m[0],
            'ws_1'    : m[1],
            'src'     : m[2],
            'caption' : m[3],
            'ws_2'    : m[4],
            'ws_3'    : m[5]
        }
    return result

#----------------------------------------

def subber(original, values, pattern, template):

    def swap(m):
        fig_id = m.group(1)
        return template % values[fig_id]

    return pattern.sub(swap, original)

#----------------------------------------

if __name__ == '__main__':
    if len(sys.argv) == 1:
        main(sys.stdin, sys.stdout)
    elif len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as reader:
            main(reader, sys.stdout)
    elif len(sys.argv) == 3:
        with open(sys.argv[1], 'r') as reader:
            with open(sys.argv[2], 'w') as writer:
                main(reader, writer)
    else:
        print >> sys.stderr, 'Usage: fignumber.py [infile [outfile]]'
        sys.exit(1)
