import json
birthdays = {'Curie' : 1867, 'Hopper' : 1906, 'Franklin' : 1920}
as_string = json.dumps(birthdays)
print as_string
print type(as_string)
