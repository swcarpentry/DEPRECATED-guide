-- The `person` table is used to explain the most basic queries.
-- Note that `danforth` has no measurements.
create table person(
	ident    text,
	personal text,
	family	 text
);

insert into person values('dyer',     'William',   'Dyer');
insert into person values('pb',       'Frank',     'Pabodie');
insert into person values('lake',     'Anderson',  'Lake');
insert into person values('roe',      'Valentina', 'Roerich');
insert into person values('danforth', 'James',     'Danforth');

-- The `site` table is equally simple.  Use it to explain the
-- difference between databases and spreadsheets: in a spreadsheet,
-- the lat/long of measurements would probably be duplicated.
create table site(
	name text,
	lat  real,
	long real
);

insert into site values('DR-1', -49.85, -128.57);
insert into site values('DR-3', -47.15, -126.72);
insert into site values('MS-4', -48.87, -123.40);

-- `visited` is an enhanced `join` table: it connects to the lat/long
-- of specific measurements, and also provides their dates.
-- Note that #752 is missing a date; we use this to talk about NULL.
create table visited(
	ident integer,
	site  text,
	dated text
);

insert into visited values(619, 'DR-1', '1927-02-08');
insert into visited values(622, 'DR-1', '1927-02-10');
insert into visited values(734, 'DR-3', '1939-01-07');
insert into visited values(735, 'DR-3', '1930-01-12');
insert into visited values(751, 'DR-3', '1930-02-26');
insert into visited values(752, 'DR-3', NULL);
insert into visited values(837, 'MS-4', '1932-01-14');
insert into visited values(844, 'DR-1', '1932-03-22');

-- The `survey` table is the actual readings.  Join it with `site` to
-- get lat/long, and with `visited` to get dates (except for #752).
-- Note that Roerich's salinity measurements are an order of magnitude
-- too large (use this to talk about data cleanup).  Note also that
-- there are two cases where we don't know who took the measurement,
-- and that in most cases we don't have an entry (NULL or not) for the
-- temperature.
create table survey(
	taken   integer,
	person  text,
	quant   real,
	reading real
);

insert into survey values(619, 'dyer', 'rad',    9.82);
insert into survey values(619, 'dyer', 'sal',    0.13);
insert into survey values(622, 'dyer', 'rad',    7.80);
insert into survey values(622, 'dyer', 'sal',    0.09);
insert into survey values(734, 'pb',   'rad',    8.41);
insert into survey values(734, 'lake', 'sal',    0.05);
insert into survey values(734, 'pb',   'temp', -21.50);
insert into survey values(735, 'pb',   'rad',    7.22);
insert into survey values(735, NULL,   'sal',    0.06);
insert into survey values(735, NULL,   'temp', -26.00);
insert into survey values(751, 'pb',   'rad',    4.35);
insert into survey values(751, 'pb',   'temp', -18.50);
insert into survey values(751, 'lake', 'sal',    0.10);
insert into survey values(752, 'lake', 'rad',    2.19);
insert into survey values(752, 'lake', 'sal',    0.09);
insert into survey values(752, 'lake', 'temp', -16.00);
insert into survey values(752, 'roe',  'sal',   41.60);
insert into survey values(837, 'lake', 'rad',    1.46);
insert into survey values(837, 'lake', 'sal',    0.21);
insert into survey values(837, 'roe',  'sal',   22.50);
insert into survey values(844, 'roe',  'rad',   11.25);

select '----------------------------------------';
select 'Selecting';

select '----------------------------------------';
select 'get scientist names';
select family, personal from person;

select '----------------------------------------';
select 'commands are case insensitive';
SeLeCt famILY, PERSonal frOM PERson;

select '----------------------------------------';
select 'we control column order';
select personal, family from person;

select '----------------------------------------';
select 'repeat columns';
select ident, ident, ident from person;

select '----------------------------------------';
select 'use * for wildcard';
select * from person;

select '----------------------------------------';
select 'Removing Duplicates';

select '----------------------------------------';
select 'show data in survey table';
select * from survey;

select '----------------------------------------';
select 'unique quantity names';
select distinct quant from survey;

select '----------------------------------------';
select 'tuple uniqueness';
select distinct taken, quant from survey;

select '----------------------------------------';
select 'Filtering';

select '----------------------------------------';
select 'when a particular site was visited';
select * from visited where site='DR-1';

select '----------------------------------------';
select 'when a particular site was visited after 1930';
select * from visited where site='DR-1' and dated>='1930-00-00';

select '----------------------------------------';
select 'using "or" instead of "and"';
select * from survey where person in ('lake', 'roe');

select '----------------------------------------';
select 'using "in" instead of "or"';
select * from survey where person='lake' or person='roe';

select '----------------------------------------';
select 'using distinct with "in"';
select distinct person, quant from survey where person='lake' or person='roe';

select '----------------------------------------';
select 'Calculating New Values';

select '----------------------------------------';
select 'correct radiation readings';
select 1.05 * reading from survey where quant='rad';

select '----------------------------------------';
select 'convert temperatures to Celsius';
select taken, round(5*(reading-32)/9, 2) from survey where quant='temp';

select '----------------------------------------';
select 'Ordering Results';

select '----------------------------------------';
select 'ascending is the default';
select reading from survey where quant='rad' order by reading;

select '----------------------------------------';
select 'order descending';
select reading from survey where quant='rad' order by reading desc;

select '----------------------------------------';
select 'ordering and sub-ordering';
select taken, person from survey order by taken, person;

select '----------------------------------------';
select 'removing duplicates';
select distinct taken, person from survey order by taken, person;

select '----------------------------------------';
select 'Missing Data';

select '----------------------------------------';
select 'visits before 1930';
select * from visited where dated<'1930-00-00';

select '----------------------------------------';
select 'visits after 1930';
select * from visited where dated>='1930-00-00';

select '----------------------------------------';
select 'visits with unknown dates (wrong)';
select * from visited where dated=NULL;

select '----------------------------------------';
select 'visits with unknown dates (right)';
select * from visited where dated is NULL;

select '----------------------------------------';
select 'visits with known dates';
select * from visited where dated is not NULL;

select '----------------------------------------';
select 'Combining Data';

select '----------------------------------------';
select 'combine "site" with "visited"';
select * from site join visited;

select '----------------------------------------';
select 'filter where sites match';
select * from site join visited where site.name=visited.site;

select '----------------------------------------';
select 'get latitude, longitude, and date';
select site.lat, site.long, visited.dated
from   site join visited
where  site.name=visited.site;

select '----------------------------------------';
select 'get all radiation readings from DR-1';
select visited.dated, survey.reading
from   survey join visited
where  survey.taken=visited.ident
  and  visited.site='DR-1'
  and survey.quant='rad';

select '----------------------------------------';
select 'get all radiation readings since 1930';
select 'but notice that #752 is missing (NULL)...';
select survey.reading
from   survey join visited
where  survey.taken=visited.ident
  and  survey.quant='rad'
  and  visited.dated>='1930-00-00';

select '----------------------------------------';
select 'Self-Join';

select '----------------------------------------';
select 'who has worked together?';
select 'start by joining "survey" with itself';
select count(*)
from   survey X join survey Y;

select '----------------------------------------';
select 'now keep rows where the two "person" values are different';
select count(*)
from   survey X join survey Y
where  X.person!=Y.person;

select '----------------------------------------';
select 'now keep distinct values';
select distinct X.person, Y.person
from   survey X join survey Y
where  X.person!=Y.person;

select '----------------------------------------';
select 'and finally eliminate mirrored duplicates';
select distinct X.person, Y.person
from   survey X join survey Y
where  X.person>Y.person;

select '----------------------------------------';
select 'Aggregation';

select '----------------------------------------';
select 'date range';
select min(dated) from visited;
select max(dated) from visited;
select min(dated), max(dated) from visited;

select '----------------------------------------';
select 'averaging';
select avg(reading) from survey where quant='sal';

select 'averaging sensible values';
select avg(reading) from survey
where quant='sal'
  and reading<10.0;

select 'counting';
select count(reading) from survey
where quant='sal'
  and reading<10.0;

select 'can count anything';
select count(*) from survey
where quant='sal'
  and reading<10.0;

select 'unaggregated with aggregated takes arbitrary';
select person, count(*) from survey
where quant='sal'
  and reading<10.0;

select '----------------------------------------';
select 'Grouping';

select '----------------------------------------';
select   'grouping visited by site only keeps arbitrary';
select   * from visited
group by site;

select '----------------------------------------';
select 'get date ranges for sites';
select   site, min(dated), max(dated) from visited
group by site;

select '----------------------------------------';
select 'radiation readings by person';
select   person, count(reading), round(avg(reading), 2)
from     survey
where    survey.quant='rad'
group by survey.person;

select '----------------------------------------';
select 'radiation readings by site';
select   visited.site, count(survey.reading), round(avg(survey.reading), 2)
from     visited join survey
where    visited.ident=survey.taken
  and    survey.quant='rad'
group by visited.site;

select '----------------------------------------';
select 'Sub-Queries';

select '----------------------------------------';
select 'what measurements do we have with temperatures?';
select * from survey
 where taken in
       (select taken from survey where quant='temp');

select '----------------------------------------';
select 'who took no measurements (incorrect: not filtering null)?';
select *
from   person
where  person.ident not in
       (select distinct(person)
        from survey);

select '----------------------------------------';
select 'who took no measurements (correct: not filtering null)?';
select *
from   person
where  person.ident not in
       (select distinct(person)
        from survey
        where person is not NULL);
