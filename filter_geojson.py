# -*- coding: utf-8 -*-
"""
@author: J. Gerardo Moreno N.
"""
import json
from datetime import datetime
from shapely.geometry import Polygon
from pyproj import Proj, transform

# Path where the input file is located
path_input_file = 'calificaciones.json'

# Input and output coordinates format
inpProj = Proj(init='epsg:25830')
outProj = Proj(init='epsg:4326')

# Read input file
print ("Reading input file...")

with open(path_input_file,"r") as input_file:
    data = json.load(input_file)

# Process JSON data
print("Processing JSON data...")

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
        # or (feature['properties']['califi'] == "CHP"  and  feature['properties']['tipoca'] == "134")
        or (feature['properties']['califi'] == "E/SP" and  feature['properties']['tipoca'] == "1P")):
        # Change the geometry to Point and add properties
        feature['geometry']['type'] = "Point"
        feature['properties']['poblacion'] = 0
        feature['properties']['tweets'] = 0
        feature['properties']['trafico'] = 0
        feature['properties']['tiempo'] = 0
        feature['properties']['nombre'] = ""
        # Delete data that we don't need
        del feature['properties']['clase']
        del feature['properties']['tipouso']
        del feature['properties']['origen']
        del feature['properties']['ficha_es']
        del feature['properties']['ficha_va']
        polygon = Polygon(feature['geometry']['coordinates'][0])
        # Calculate polygon centroid
        point = polygon.envelope.centroid 
        x1, y1 = point.x, point.y
        # Transform coordinates format
        x2, y2 = transform(inpProj, outProj, x1, y1) 
        feature['geometry']['coordinates'] = [x2, y2]
        # Save the feature
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

path_output_file = 'calificaciones_'+date+'.json'

with open(path_output_file, "w") as output_file:
    json.dump((result), output_file, indent = 3)

# Ready
print("Ready")
