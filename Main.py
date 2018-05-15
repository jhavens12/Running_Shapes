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
        if key < get_time.LM(1):
            del dict_1[key]
        if key > get_time.LS(0):
            del dict_1[key]

    return dict_1

master_dict = get_data.my_filtered_activities()
current_dict = current_period()

def import_photo():
    try:
        img = Image.open(sys.argv[1])
    except:
        img = Image.open('./test_image.jpg')
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
    #print()

    img1 = Image.open("./Badge_Background.png")
    #img = Image.new("RGBA", (600, 400))
    img = img1.resize((600,400))
    img_w, img_h = img.size
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("./font1.ttf", 70)


    line1_w, line1_h = draw.textsize(line1, font=font)
    line2_w, line2_h = draw.textsize(line2, font=font)
    line3_w, line3_h = draw.textsize(line3, font=font)

    buffer = line3_h + 20

    print("text height: "+str(line3_h))

    mountain = Image.open("mountain.png")
    resized_mountain = mountain.resize((line3_h+10,line3_h+10)) #resize polys to quarter of screen
    mountain_w, mountain_h = resized_mountain.size

    #text_h = line1_h + line2_h + line3_h + (buffer*2)
    text_h = (line1_h) + (buffer*2)
    text_start = int((img_h/2) - (text_h/2))
    #
    # draw.text((((img_w-line1_w)/2),text_start), line1, font=font, fill='white') #fill="black")
    # draw.text((((img_w-line2_w)/2),text_start+line1_h+buffer), line2, font=font, fill='white') #fill="black")
    # draw.text((((img_w-line3_w)/2),text_start+line1_h+buffer+line2_h+buffer+buffer), line3, font=font, fill='white') #fill="black")

    draw.text((((img_w-line1_w)/2),text_start), line1, font=font, fill='white') #fill="black")
    draw.text((((img_w-line2_w)/2),text_start+(buffer)), line2, font=font, fill='white') #fill="black")
    draw.text((((img_w-line3_w)/2),text_start+(buffer*2)), line3, font=font, fill='white') #fill="black")


    #mountain_x = int(((img_w-line3_w)/2) - buffer - mountain_w)
    #mountain_y = text_start+line1_h+buffer+line2_h+buffer
    mountain_x = int(((img_w-line3_w)/2) - 10 - mountain_w)
    mountain_y = text_start+(buffer*2)

    img.paste(resized_mountain, (mountain_x, mountain_y), resized_mountain)

    return img

def generate_poly(img2):
    image_list = []
    for activity in sorted(current_dict):
        #print(current_dict[activity]['map']['summary_polyline'])
        filename = create_poly.run_and_graph(current_dict[activity]['map']['summary_polyline'])
        image_list.append(filename)

    #result = Image.new("RGBA", (1080, 1080))
    result = img2
    image_count = len(image_list)
    for index, file in enumerate(image_list):
        path = os.path.expanduser(file)
        img = Image.open(path)

        result_w,result_h = result.size

        new_h = int(result_h/image_count) + image_count*20# make thumbnails proportional to screen

        img.thumbnail((new_h, new_h), Image.ANTIALIAS)#, Image.ANTIALIAS)
        resized_img = img.resize((new_h, new_h))
        w, h = resized_img.size

        x = 0
        y = index * (h - (image_count*20))

        print('pos {0},{1} size {2},{3}'.format(x, y, w, h))
        result.paste(resized_img, (x, y), resized_img)

    result.save(os.path.expanduser('./done/image3.png'))

def generate_poly2(img2):
    image_list = []
    badge_list = []
    the_dict = {}
    for n,activity in enumerate(sorted(current_dict)):
        #print(current_dict[activity]['map']['summary_polyline'])
        filename = create_poly.run_and_graph(current_dict[activity]['map']['summary_polyline'])
        badge = generate_badges(current_dict[activity])
        badge_list.append(badge)
        image_list.append(filename)
        the_dict[n] = {}
        the_dict[n]['poly'] = filename
        the_dict[n]['badge'] = badge

    result = img2
    result_h, result_w = result.size

    #for index, file in enumerate(image_list):
    for index, entry in enumerate(the_dict):

        #path = os.path.expanduser(file)
        path = os.path.expanduser(the_dict[entry]['poly'])
        badge = the_dict[entry]['badge']
        badge_w, badge_h = badge.size

        img = Image.open(path)
        resized_image = img.resize((int(result_h/2),int(result_w/2))) #resize polys to quarter of screen
        x = index // 2 * int(result_w/2) #image x
        y = index % 2 * int(result_h/2) #image y
        w, h = resized_image.size
        print('pos {0},{1} size {2},{3}'.format(x, y, w, h))
        result.paste(resized_image, (x, y, x + w, y + h), resized_image)

        #badge_x = int( ((x+w)/2) - (badge_w/2) )
        badge_x = int(x + (w/2)-(badge_w/2) )

        #badge_y = int( ((y+h)/2) - (badge_h/2) )
        badge_y = int(y + (h/2)-(badge_h/2) )

        result.paste(badge, (badge_x,badge_y), badge)

    result.save(os.path.expanduser('./done/image4.png'))
    result.show()

img2 = import_photo()
generate_poly2(img2)
