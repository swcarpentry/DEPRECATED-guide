import sys
import random
import datetime

Measures = {
    'temp' : (-9.0,   14.0),
    'sal'  : ( 3.0,    5.0),
    'rad'  : ( 1.0, 1000.0)
}

Expeditions = {
    'Miskatonic 1927'  : [['RL-1', '1928-02-10', '1928-02-13']],
    'Miskatonic 1929'  : [['RL-1', '1929-11-07', '1929-11-19'],
                          ['RL-2', '1930-01-02', '1930-01-08']],
    'Pabodie'          : [['PoI',  '1930-12-27', '1930-12-29'],
                          ['RL-2', '1931-01-05', '1931-01-11']],
    'Derby Foundation' : [['PoI',  '1931-12-19', '1931-12-21'],
                          ['RL-2', '1932-01-02', '1932-01-05'],
                          ['RL-1', '1932-01-29', '1932-02-03']]
}

People = {
    'Miskatonic 1927'  : ['dyer', 'pabodie'],
    'Miskatonic 1929'  : ['danforth.j', 'danforth.c', 'pabodie'],
    'Pabodie'          : ['pabodie', 'dyer', 'lake'],
    'Derby Foundation' : ['roerich']
}

Format = "insert into Reading values(%s %s %s %s %s);"

def rand_date(start, end):
    start = datetime.datetime(*[int(x) for x in start.split('-')])
    end = datetime.datetime(*[int(x) for x in end.split('-')])
    delta = end - start
    offset = datetime.timedelta(days=random.randrange(delta.days))
    actual = str(start + offset).split()[0]
    return actual

seen = set()
for i in range(int(sys.argv[1])):
    exp = random.choice(Expeditions.keys())
    person = random.choice(People[exp])
    site, start, end = random.choice(Expeditions[exp])
    when = rand_date(start, end)
    measure = random.choice(['temp', 'sal', 'rad'])
    if (site, when, measure) in seen:
        continue
    seen.add((site, when, measure))
    amount = random.uniform(*Measures[measure])
    when = "'%s'," % when
    site = ("'%s'," % site).ljust(7)
    person = ("'%s'," % person).ljust(13)
    measure = ("'%s'," % measure).ljust(7)
    amount = ("%.2f" % amount).rjust(6)
    print Format % (when, site, person, measure, amount)
