#!/usr/bin/env python

"""
Compile book pages into readable form.
"""

#----------------------------------------

import sys
import os
import re
import jinja2

#----------------------------------------

TITLE_RE = re.compile(r'<meta\s+name="title"\s+content="([^"]*)"\s*/>')

CONTACT_EMAIL   = 'info@software-carpentry.org'
FACEBOOK_URL    = 'https://www.facebook.com/SoftwareCarpentry'
GOOGLE_PLUS_URL = 'https://plus.google.com/u/0/114244759874490019250/posts'
TWITTER_NAME    = '@swcarpentry'
TWITTER_URL     = 'https://twitter.com/swcarpentry'

STANDARD = {
    'contact_email'   : CONTACT_EMAIL,
    'facebook_url'    : FACEBOOK_URL,
    'google_plus_url' : GOOGLE_PLUS_URL,
    'root_path'       : '.',
    'twitter_name'    : TWITTER_NAME,
    'twitter_url'     : TWITTER_URL
}

#----------------------------------------

def main(out_dir, source_files):
    '''Compile web pages.'''

    loader = jinja2.FileSystemLoader(['.'])
    environment = jinja2.Environment(loader=loader)
    for (i, f) in enumerate(source_files):
        title = get_title(f)
        template = environment.get_template(f)
        page = {
            'title'           : title,
            'prev'            : get_prev(source_files, i),
            'next'            : get_next(source_files, i),
            'uplink'          : 'index.html'
        }
        result = template.render(page=page, **STANDARD)
        with open(os.path.join(out_dir, f), 'w') as writer:
            writer.write(result)

#----------------------------------------

def get_title(filename):
    '''Extract title from Jinja2 file.'''

    with open(filename, 'r') as reader:
        data = reader.read()
    match = TITLE_RE.search(data)
    assert match, 'No title found in %s' % filename
    return match.group(1)

#----------------------------------------

def get_prev(filenames, here):
    '''Get the previous entry for linking.'''

    if here == 0:
        return None
    else:
        return os.path.splitext(filenames[here-1])[0]

#----------------------------------------

def get_next(filenames, here):
    '''Get the next entry for linking.'''

    if here == len(filenames)-1:
        return None
    else:
        return os.path.splitext(filenames[here+1])[0]

#----------------------------------------

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
