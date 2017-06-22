import json
import calendar
from datetime import datetime

# Path where the input file is located
path_input_file = 'calificaciones.JSON'

# Read input file
print ("Reading input file...")

with open(path_input_file,"r") as input_file:
    data = json.load(input_file)

# Filter JSON data
print("Filtering JSON data...")


result = {}
result['type'] = data['type']
result['crs'] = data['crs']
result['features'] = []

for feature in data['features']:
    if feature['properties']['califi'] == "EDA" and feature['properties']['uso'] == "SJL":
        result['features'].append(feature)
    elif feature['properties']['califi'] == "PID":
        result['features'].append(feature)
    elif feature['properties']['califi'] == "GTR" and feature['properties']['tipoca'] == "4":
        result['features'].append(feature)
    elif feature['properties']['califi'] == "GSP" and (feature['properties']['tipoca'] == "4" or feature['properties']['tipoca'] == "3"):
        result['features'].append(feature)
    elif feature['properties']['califi'] == "TER" and feature['properties']['tipoca'] == "3":
        result['features'].append(feature)
    elif feature['properties']['califi'] == "CHP" and feature['properties']['tipoca'] == "134":
        result['features'].append(feature)
    elif feature['properties']['califi'] == "E/SP" and feature['properties']['tipoca'] == "1P":
        result['features'].append(feature)

# Write output file
print('Writting output file...')

date = str(datetime.now())
date = date.replace("-", "")
date = date.replace(":", "")
date = date.replace(".", "")
date = date.replace(" ", "")

path_output_file = 'calificaciones_'+date+'.JSON'

with open(path_output_file, "w") as output_file:
    json.dump((result), output_file, indent = 4)

# Ready
print("Ready")
    
