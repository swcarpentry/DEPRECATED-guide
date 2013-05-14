import sys
import requests
import json

URL = 'http://climatedataapi.worldbank.org/climateweb/rest/v1/country/cru/tas/year/%s.JSON'

def main(args):
    first_country = 'AUS'
    second_country = 'CAN'
    if len(args) > 0:
        first_country = args[0]
    if len(args) > 1:
        second_country = args[1]

    result = ratios(first_country, second_country)
    display(result)

def display(values):
    '''Show dictionary entries in sorted order.'''
    keys = values.keys()
    keys.sort()
    for k in keys:
        print k, values[k]

def ratios(first, second):
    '''Calculate ratio of average temperatures for two countries over time.'''
    first = get_temps(first)
    second = get_temps(second)
    assert len(first) == len(second), 'Length mis-match in results'
    result = {}
    for (i, first_entry) in enumerate(first):
        year = first_entry['year']
        second_entry = second[i]
        assert second_entry['year'] == year, 'Year mis-match'
        result[year] = first_entry['data'] / second_entry['data']
    return result

def get_temps(country_code):
    '''Get annual temperatures for a country.'''
    response = requests.get(URL % country_code)
    assert response.status_code == 200, \
           'Failed to get data for %s' % country_code
    result = json.loads(response.text)
    for entry in result:
        entry['data'] = kelvin(entry['data'])
    return result

def kelvin(celsius):
    '''Convert degrees C to degrees K.'''
    return celsius + 273.15

if __name__ == '__main__':
    main(sys.argv[1:])
