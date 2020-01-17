import matplotlib.pyplot as plt
strava_orange="#fc4c02"
from pprint import pprint
import datetime
import photos #for ios

def decode_polyline(polyline_str):
    print("Decoding...")
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

def run_and_graph(filename,polyline_input):
    print("Graphing...")
    lines = decode_polyline(polyline_input)
    lat=[]
    lon=[]
    for line in lines:
        lon.append(line[0])
        lat.append(line[1])
    fig,ax=plt.subplots()
    ax.plot(lon,lat,color=strava_orange,linewidth=5)
    ax.set_axis_off()
    plt.subplots_adjust(left=0, bottom=0, right=1, top=1,
                    wspace=None, hspace=None)

    f_name = './Render/'+str(filename)+'.png'
    print("Saving...")
    fig.savefig(f_name, bbox_inches='tight', transparent='True')
    photos.create_image_asset(f_name) #ios
