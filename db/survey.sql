-- Back story: expeditions in the Pacific to sample sea water to check
-- on lingering effects of nuclear tests.  Easy to use data to show
-- how to do Boolean tests in "where" clauses, how to aggregate using
-- "group by", how to do simple "join" statements, etc.  The tables
-- and data are also set up to motivate discussion of:
-- * handling missing data
-- * data inconsistencies and cleanup
-- * re-designing tables to make things simpler

-- Voyages into the unknown, keyed by name of ship and launch date.
-- * Will later come back and give each Expedition entry an "ident"
--   field so that "Crew" entries can have simpler foreign keys.
-- * Some "Reading" entries will be found to have dates that aren't
--   within the (start, end) of the expedition (look for these as part
--   of the data cleanup discussion).
-- * Some "ended" entries are null (duration of expedition has to be
--   inferred from date of final reading associated with it, but that
--   is hard to do, and not reliable).
-- * Explain use of "YYYY-MM-DD" strings for dates in SQLite, and that
--   "grown-up" databases have real date and duration types.
create table Expedition(
       vessel   text not null,
       started  text not null, -- "YYYY-MM-DD"
       ended    text,          -- "YYYY-MM-DD"
       primary key(vessel, started)
);
insert into Expedition values('Miskatonic 1927',  '1927-03-08', '1928-09-15');
insert into Expedition values('Miskatonic 1929',  '1929-04-15', NULL);
insert into Expedition values('Pabodie',          '1930-09-26', '1931-05-27');
insert into Expedition values('Derby Foundation', '1931-09-04', NULL);

-- Where have measurements been taken?
-- * Will motivate one-to-many joins (all measurements from a site)
-- * Should we start by having lat/long in the "Reading" table, then
--   separate it so that identifying mistakes in data entry is easier?
create table Site(
       ident text not null,
       lat   real not null, -- signed decimal degrees
       long  real not null, -- signed decimal degrees
       primary key(ident)
);
insert into Site values('RL-1', -47.15, -126.716667);
insert into Site values('RL-2', -49.85, -128.566667);
insert into Site values('PoI',  -48.876667, -123.393333);

-- Who has taken measurements?
-- * Explain need for "ident" field by having two surveyors with
--   the same personal/family names.
-- * Include box on why "personal" and "family" rather than "first"
--   and "last" (cultural differences).
-- * Can also test "who didn't go on any expeditions?"
create table Surveyor(
       ident    text not null,
       personal text not null,
       family   text not null,
       primary key(ident)
);
insert into Surveyor values('danforth.j', 'James', 'Danforth');
insert into Surveyor values('danforth.c', 'Charles', 'Danforth');
insert into Surveyor values('deroure', 'Elspeth', 'De Roure');
insert into Surveyor values('dyer', 'William', 'Dyer');
insert into Surveyor values('lake', 'Anderson', 'Lake');
insert into Surveyor values('pabodie', 'Frank', 'Pabodie');
insert into Surveyor values('roe', 'Valentina', 'Roerich');
insert into Surveyor values('zymmer', 'Nikolai', 'Zymantsev');

-- Who was part of which expedition?
-- * This is a classic "join table" for representing a many-to-many
--   relationship.
-- * Complexity of two-part foreign key into "Expedition" table will
--   motivate having explicit identifiers for "Expedition" entries.
create table Crew(
       vessel   text not null,
       started  text not null, -- "YYYY-MM-DD"
       person   text not null,
       foreign key(vessel, started)
               references Expedition(vessel, started),
       unique(vessel, started, person)
);
insert into Crew values('Miskatonic 1927',  '1927-03-08', 'dyer');
insert into Crew values('Miskatonic 1927',  '1927-03-08', 'pabodie');
insert into Crew values('Miskatonic 1929',  '1929-04-15', 'danforth.j');
insert into Crew values('Miskatonic 1929',  '1929-04-15', 'danforth.c');
insert into Crew values('Miskatonic 1929',  '1929-04-15', 'pabodie');
insert into Crew values('Pabodie',          '1930-09-26', 'pabodie');
insert into Crew values('Pabodie',          '1930-09-26', 'dyer');
insert into Crew values('Pabodie',          '1930-09-26', 'lake');
insert into Crew values('Derby Foundation', '1931-09-04', 'roerich');

-- What units are used for various measurements?
-- * Explain that explicit metadata increases longevity of data
--   (without it, can't know if temperatures are C or F).  Compare
--   with lack of units for elevation in "Site" table.
-- * Include units for several measures (e.g., "pressure") that
--   aren't actually used.
create table Units(
       measure  text not null,
       unitname text not null,
       primary key(measure)
);
insert into Units values('temp',  'C');
insert into Units values('tempF', 'F');
insert into Units values('sal',   'pct');
insert into Units values('rad',   'mBq/l');
insert into Units values('pres',  'psi');

-- Temperature, salinity, and radioactivity measurements.
-- * "measure" is supposed to be one of "temp", "sal", "rad", but have
--   at least one entry that is misspelled.
-- * Often don't know who took a reading (so have null for "person").
-- * Expedition is not explicitly recorded; should be possible to infer
--   by comparing date of reading to dates of expeditions, but since
--   some expeditions overlap, need to use information about person as
--   well.  (This may be too advanced for our lesson.)
create table Reading(
       taken    text not null, -- "YYYY-MM-DD"
       place    text not null, -- a site identifier
       person   text,          -- a person or NULL
       measure  text not null, -- one of {"temp", "sal", "rad"}
       amount   real not null, -- actual reading
       primary key(place, taken, measure),
       foreign key(person)
               references Surveyor(ident),
       foreign key(place)
               references Site(ident),
       foreign key(measure)
               references Units(measure)
);
-- FIXME: need to introduce some NULLs for person, and some invalid measurements
insert into Reading values('1928-02-10', 'RL-1', 'dyer',       'temp',  -3.59);
insert into Reading values('1928-02-10', 'RL-1', 'pabodie',    'rad',  785.65);
insert into Reading values('1928-02-11', 'RL-1', 'dyer',       'sal',    3.40);
insert into Reading values('1928-02-12', 'RL-1', 'dyer',       'temp',  -6.63);
insert into Reading values('1928-02-12', 'RL-1', 'pabodie',    'rad',  997.68);
insert into Reading values('1928-02-12', 'RL-1', 'pabodie',    'sal',    4.28);
insert into Reading values('1929-11-11', 'RL-1', 'danforth.c', 'sal',    4.36);
insert into Reading values('1929-11-14', 'RL-1', 'danforth.j', 'sal',    3.07);
insert into Reading values('1929-11-15', 'RL-1', 'pabodie',    'rad',  153.94);
insert into Reading values('1930-01-02', 'RL-2', 'danforth.j', 'rad',  500.14);
insert into Reading values('1930-01-05', 'RL-2', 'danforth.j', 'temp',  -0.34);
insert into Reading values('1930-12-27', 'PoI',  'dyer',       'rad',  417.61);
insert into Reading values('1930-12-27', 'PoI',  'lake',       'temp',   8.47);
insert into Reading values('1930-12-28', 'PoI',  'lake',       'sal',    3.10);
insert into Reading values('1930-12-28', 'PoI',  'lake',       'temp',  10.98);
insert into Reading values('1931-01-06', 'RL-2', 'pabodie',    'temp',  -4.48);
insert into Reading values('1931-01-07', 'RL-2', 'pabodie',    'sal',    3.27);
insert into Reading values('1931-01-08', 'RL-2', 'dyer',       'sal',    4.78);
insert into Reading values('1931-01-09', 'RL-2', 'dyer',       'sal',    4.72);
insert into Reading values('1931-01-09', 'RL-2', 'lake',       'temp',  13.77);
insert into Reading values('1931-01-10', 'RL-2', 'dyer',       'rad',  574.64);
insert into Reading values('1931-01-10', 'RL-2', 'lake',       'sal',    4.62);
insert into Reading values('1931-01-10', 'RL-2', 'pabodie',    'temp',   7.69);
insert into Reading values('1931-12-20', 'PoI',  'roerich',    'rad',  894.42);
insert into Reading values('1931-12-20', 'PoI',  'roerich',    'sal',    3.24);
insert into Reading values('1932-01-03', 'RL-2', 'roerich',    'rad',  673.88);
insert into Reading values('1932-01-04', 'RL-2', 'roerich',    'rad',  599.66);
insert into Reading values('1932-01-04', 'RL-2', 'roerich',    'temp',   4.34);
insert into Reading values('1932-01-30', 'RL-1', 'roerich',    'temp',  12.21);
insert into Reading values('1932-02-02', 'RL-1', 'roerich',    'sal',    4.43);
