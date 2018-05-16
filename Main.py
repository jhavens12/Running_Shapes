import create_poly_easy as create_poly
import get_data
import get_time
import calc
import os
import sys
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFont
from PIL import ImageDraw


def current_period():
    main_dict = {}
    dict_1 = master_dict.copy()

    #filter out old runs (older than monday)
    for key in master_dict:
        if key < get_time.LM(3):
            del dict_1[key]
        # if key > get_time.LS(0):
        #     del dict_1[key]

    return_dict = {}
    for n,key in enumerate(dict_1):
        if n == 0 or n == 1 or n == 2 or n == 4 or n == 5:
            return_dict[key] = dict_1[key]

    return return_dict

master_dict = get_data.my_filtered_activities()
current_dict = current_period()

def import_photo():
    try:
        img = Image.open(sys.argv[1])
    except:
        img = Image.open('./resources/test_image.jpg')
    w,h = img.size
    print("H: "+str(h)+", W: "+str(w))
    img2 = img.crop((0, 0, w, w))
    brightness = ImageEnhance.Brightness(img2)
    img3 = brightness.enhance(.2)

    return img3
    #img2.save("./done/img2.jpg")

    #result.save(os.path.expanduser('./done/image.png'))

def generate_badges(activity):

    #for activity in sorted(current_dict):
    line1 = (str(activity['distance_miles'])+"m")
    line2 = (str(activity['weekday_short_date']))
    line3 = str(activity['total_elevation_feet'])+"ft"

    img1 = Image.open("./resources/Badge_Background.png")
    #img = Image.new("RGBA", (600, 400))
    img = img1.resize((600,400))
    img_w, img_h = img.size
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("./resources/font1.ttf", 70)

    line1_w, line1_h = draw.textsize(line1, font=font)
    line2_w, line2_h = draw.textsize(line2, font=font)
    line3_w, line3_h = draw.textsize(line3, font=font)

    buffer = line3_h + 20

    #print("text height: "+str(line3_h))

    mountain = Image.open("./resources/mountain.png")
    resized_mountain = mountain.resize((line3_h+10,line3_h+10)) #resize polys to quarter of screen
    mountain_w, mountain_h = resized_mountain.size

    text_h = (line1_h) + (buffer*2)
    text_start = int((img_h/2) - (text_h/2))

    draw.text((((img_w-line1_w)/2),text_start), line1, font=font, fill='white') #fill="black")
    draw.text((((img_w-line2_w)/2),text_start+(buffer)), line2, font=font, fill='white') #fill="black")
    draw.text((((img_w-line3_w)/2),text_start+(buffer*2)), line3, font=font, fill='white') #fill="black")

    mountain_x = int(((img_w-line3_w)/2) - 10 - mountain_w)
    mountain_y = text_start+(buffer*2)

    img.paste(resized_mountain, (mountain_x, mountain_y), resized_mountain)

    return img

def generate_poly(img2):
    the_dict = {}
    for n,activity in enumerate(sorted(current_dict)):
        filename = create_poly.run_and_graph(current_dict[activity]['map']['summary_polyline'])
        badge = generate_badges(current_dict[activity])
        the_dict[n] = {}
        the_dict[n]['poly'] = filename
        the_dict[n]['badge'] = badge

    result = img2
    result_h, result_w = result.size

    run_count = len(the_dict)
    print("There are "+str(run_count)+" runs this period")
    if run_count % 2 == 1:
        print("there are an odd number of runs")
        odd_runs = True

    for index, entry in enumerate(the_dict):
        path = os.path.expanduser(the_dict[entry]['poly']) #finds poly file
        pre_badge = the_dict[entry]['badge'] #finds page file
        badge_w, badge_h = pre_badge.size #finds badge size
        img = Image.open(path) #open poly file
        if run_count <= 4: #if there are 4 or less runs
            badge = pre_badge.resize((int(result_h/4),int(result_w/4))) #resize badge
            resized_image = img.resize((int(result_h/2),int(result_w/2))) #resize polys to quarter of screen
        if run_count >= 5: #if there are 5 or more runs
            badge = pre_badge.resize((int(result_h/4),int(result_w/4))) #resize badge
            resized_image = img.resize((int(result_h/2),int(result_w/2.5))) #resize
        badge_w, badge_h = badge.size #find new badge size
        w, h = resized_image.size #resized poly size

        #XXXXX
        if run_count > 4: #everything but 5th run
            x = (index % 2 * int(result_w/2)) + (int(result_w/4) - int(w/2))  #since poly is not quarter of screen, need to move over
        else:
            x = index % 2 * int(result_w/2) #image x -

        #center X
        if run_count == 3 and index == 2 or run_count == 5 and index == 4: #can change this to detect odd runs
            x = int(result_w/2) - int(w/2) #put in middle of image

        #YYYYYY
        if run_count > 4:
            y = index // 2 * int(result_h/3.75) #image y #position images every 3
        else:
            y = index // 2 * int(result_h/2) #image y

        print('pos {0},{1} size {2},{3}'.format(x, y, w, h))
        result.paste(resized_image, (x, y, x + w, y + h), resized_image)
        #Badge position is based upon poly size
        badge_x = int(x + (w/2)-(badge_w/2) ) #where poly is (x), half the width, minus half badge width to center
        badge_y = int(y + (h/2)-(badge_h/2) )
        result.paste(badge, (badge_x,badge_y), badge)

    result.save(os.path.expanduser('./done/image4.png'))
    result.show()

img2 = import_photo()
generate_poly(img2)
