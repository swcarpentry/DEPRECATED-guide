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

-- Where have measurements been taken?
-- * Will motivate one-to-many joins (all measurements from a site)
-- * Should we start by having lat/long/elev in the "Reading" table,
--   then separate it so that identifying mistakes in data entry is
--   easier?
create table Site(
       ident text not null,
       lat   real not null, -- signed decimal degrees
       long  real not null, -- signed decimal degrees
       elev  real not null, -- units not provided (discuss why this is bad)
       primary key(ident)
);

-- Who has taken measurements?
-- * Explain need for "ident" field by having two surveyors with
--   the same personal/family names.
-- * Include box on why "personal" and "family" rather than "first"
--   and "last" (cultural differences).
create table Surveyor(
       ident    text not null,
       personal text not null,
       family   text not null,
       primary key(ident)
);

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

-- Temperature, salinity, and radioactivity measurements.
-- * "measure" is supposed to be one of "temp", "sal", "rad", but have
--   at least one entry that is misspelled.
-- * Often don't know who took a reading (so have null for "person").
-- * Expedition is not explicitly recorded; should be possible to infer
--   by comparing date of reading to dates of expeditions, but since
--   some expeditions overlap, need to use information about person as
--   well.  (This may be too advanced for our lesson.)
create table Reading(
       place    text not null,
       person   text,
       taken    text not null, -- "YYYY-MM-DD"
       measure  text not null, -- one of {"temp", "sal", "rad"}
       amount   real not null, -- actual reading
       primary key(place, taken),
       foreign key(person)
               references Surveyor(ident),
       foreign key(place)
               references Site(ident),
       foreign key(measure)
               references Units(measure)
);
