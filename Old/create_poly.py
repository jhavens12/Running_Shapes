import json
import fiona
import pandas as pd
from shapely.geometry import LineString, mapping
import shapefile as shp
import matplotlib.pyplot as plt
from io import BytesIO
import datetime


test_polyline = 'u}pnGt_c}LjBuQuAoBgCiBwBpHoBhA}IoFkDhRyBtBgCaC}C~@{FzOzLiBrI_GdFNT`DqEbGcFzC}GZoB~DbLtKrVfd@jGqGvGdKtE|Bt@mFrN}ZjKe]qKkOgGsCs@uHiCoBfAcFWoFhJ}M{BaBgCpCgFcDqB\\oGwFgJhDmRwMwDx@yDzPb@lGbStOvD[dCqHjDrA`C_J~B`@dArGqGpHi@tMpAfI_FbNjFcMc@{D'

def decode_polyline(polyline_str):
    '''Pass a Google Maps encoded polyline string; returns list of lat/lon pairs'''
    index, lat, lng = 0, 0, 0
    coordinates = []
    changes = {'latitude': 0, 'longitude': 0}

    # Coordinates have variable length when encoded, so just keep
    # track of whether we've hit the end of the string. In each
    # while loop iteration, a single coordinate is decoded.
    while index < len(polyline_str):
        # Gather lat/lon changes, store them in a dictionary to apply them later
        for unit in ['latitude', 'longitude']:
            shift, result = 0, 0

            while True:
                byte = ord(polyline_str[index]) - 63
                index+=1
                result |= (byte & 0x1f) << shift
                shift += 5
                if not byte >= 0x20:
                    break

            if (result & 1):
                changes[unit] = ~(result >> 1)
            else:
                changes[unit] = (result >> 1)

        lat += changes['latitude']
        lng += changes['longitude']

        coordinates.append((lng / 100000.0, lat / 100000.0))

    return coordinates

def save_shapefile(Linestring_object):
    driver = 'ESRI Shapefile'
    crs = {'no_defs': True,
            'ellps': 'WGS84',
            'datum': 'WGS84',
            'proj': 'longlat'}
    schema = {'geometry': 'LineString', 'properties': {'route': 'str'}}

    #with fiona.open('test_poly.shp', 'w', driver=driver, crs=crs, schema=schema) as layer:
    with fiona.open('./temp/poly1.shp', 'w', driver=driver, schema=schema) as layer:
        layer.write({'geometry': mapping(Linestring_object),
                        'properties': {'route': 'test'}
                        })

def run_and_graph(polyline_input):
    #FEED IN POLYLINE STRING

    #demo_polyline = input("Paste polyline ") #input polyline
    #demo_LS = LineString(decode_polyline(demo_polyline)) # gets linestring object from polyline

    decoded_polyline = decode_polyline(polyline_input) #decodes polyline to list of lat/long
    LSObject = LineString(decoded_polyline) #gets LS object from decided polyline

    save_shapefile(LSObject) #saves the .shp file
    sf = shp.Reader("./temp/poly1.shp") #opens the .shp file

    plt.figure()
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        plt.plot(x,y,linewidth=5,color="white")

    plt.axis('off')
    #plt.figure(figsize=(10,10))
    #plt.linewidth=200
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1,
                wspace=None, hspace=None)

    date = str(datetime.datetime.now())
    filename = './shapes/'+date+'.png'
    plt.savefig(filename, bbox_inches='tight', transparent='True')
    return filename
