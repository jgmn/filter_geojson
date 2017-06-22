import json
import calendar
from datetime import datetime
from shapely.geometry import Polygon

# Path where the input file is located
path_input_file = 'calificaciones.JSON'

# Read input file
print ("Reading input file...")

with open(path_input_file,"r") as input_file:
    data = json.load(input_file)

# Filter JSON data and calculating Polygons centroid
print("Filtering JSON data...")
print("Calculating Polygons centroid...")

result = {}
result['type'] = data['type']
result['crs'] = data['crs']
result['features'] = []

temp = []

for feature in data['features']:
    if ((feature['properties']['califi'] == "EDA" and  feature['properties']['uso'] == "SJL")
        or (feature['properties']['califi'] == "PID")
        or (feature['properties']['califi'] == "GTR"  and  feature['properties']['tipoca'] == "4")
        or (feature['properties']['califi'] == "GSP"  and (feature['properties']['tipoca'] == "4" or feature['properties']['tipoca'] == "3"))
        or (feature['properties']['califi'] == "TER"  and  feature['properties']['tipoca'] == "3")
        or (feature['properties']['califi'] == "CHP"  and  feature['properties']['tipoca'] == "134")
        or (feature['properties']['califi'] == "E/SP" and  feature['properties']['tipoca'] == "1P")):
        feature['geometry']['type'] = "Point"
        for coordinate in feature['geometry']['coordinates'][0]:
            temp.append(tuple(coordinate))
        polygon = Polygon(temp)
        point = polygon.envelope.centroid
        feature['geometry']['coordinates'] = [point.x, point.y]
        result['features'].append(feature)
        del temp[:]

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
    
