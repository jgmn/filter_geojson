import json
import calendar
from datetime import datetime
from shapely.geometry import Polygon
from pyproj import Proj, transform

# Path where the input file is located
path_input_file = 'calificaciones.JSON'

# Input and output coordinates format
inpProj = Proj(init='epsg:25830')
outProj = Proj(init='epsg:4326')

# Read input file
print ("Reading input file...")

with open(path_input_file,"r") as input_file:
    data = json.load(input_file)

# Filter JSON data
# Calculate polygons centroid
# Transform coordinates format
print("Filtering JSON data...")
print("Calculating polygons centroid...")
print("Transforming coordinates format...")

result = {}
result['type'] = data['type']
result['crs'] = data['crs']
result['features'] = []

for feature in data['features']:
    if ((feature['properties']['califi'] == "EDA" and  feature['properties']['uso'] == "SJL")
        or (feature['properties']['califi'] == "PID")
        or (feature['properties']['califi'] == "GTR"  and  feature['properties']['tipoca'] == "4")
        or (feature['properties']['califi'] == "GSP"  and (feature['properties']['tipoca'] == "4" or feature['properties']['tipoca'] == "3"))
        or (feature['properties']['califi'] == "TER"  and  feature['properties']['tipoca'] == "3")
        or (feature['properties']['califi'] == "CHP"  and  feature['properties']['tipoca'] == "134")
        or (feature['properties']['califi'] == "E/SP" and  feature['properties']['tipoca'] == "1P")):
        feature['geometry']['type'] = "Point"
        polygon = Polygon(feature['geometry']['coordinates'][0])
        point = polygon.envelope.centroid # Calculate polygon centroid
        x1, y1 = point.x, point.y
        x2, y2 = transform(inpProj, outProj, x1, y1) # Transform coordinates format
        feature['geometry']['coordinates'] = [x2, y2]
        result['features'].append(feature)

# Change CRS to indicate the new coordinates format 
result['crs']['properties']['name'] = "urn:ogc:def:crs:EPSG::4326" 

# Write output file
print('Writting output file...')

date = str(datetime.now())
date = date.replace("-", "")
date = date.replace(":", "")
date = date.replace(".", "")
date = date.replace(" ", "")

path_output_file = 'calificaciones_'+date+'.JSON'

with open(path_output_file, "w") as output_file:
    json.dump((result), output_file, indent = 3)

# Ready
print("Ready")

    
