#!/usr/bin/env python
from threading import Thread
from PIL import ImageFont, ImageDraw, Image
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import requests, ast, time, datetime, sys

times = []

def get_train_times():

    def run_get_times():

        while True:

            global times

            r = requests.get("https://train-sign.herokuapp.com/Q04S")

            text = r.text

            times = ast.literal_eval(text)

            time.sleep(30)

    thread = Thread(target=run_get_times)

    thread.start()

# get_train_times()

def initialize_matrix(brightness):

    options = RGBMatrixOptions()

    options.rows = 32

    options.cols = 64

    options.chain_length = 2

    options.parallel = 1

    options.brightness = brightness
    
    options.show_refresh_rate = 0

    options.hardware_mapping = 'adafruit-hat-pwm'  # If you have an Adafruit HAT: 'adafruit-hat'

    matrix = RGBMatrix(options = options)

    return matrix

def delete_zeros():

    global times

    zeros = []

    for i in range(len(times)):

        if i[0] == '00' or i[0] == '0':

            zeros.append(i)

    if len(zeros) > 0:

        del times[0:len(zeros)]

    else:

        pass

    return times

def run():
    get_train_times()

    starttime = time.time()

    while True:

        global times

        logos = []

        images = []

        # times = strip_zeros()

        for i in times:

            #Get the train letter/number
            train_id = i[1]

            #Strip leading zeros and double zeros

            minutes = i[0]

            # minutes = minutes.lstrip('0')

            #Get proper train logo
            train_id = train_id.lower()

            #Set font
            font = ImageFont.truetype('../fonts/piboto/Piboto-Light.ttf',13)
            #Create blank image
            image = Image.new("RGB", (128, 16))  # Can be larger than matrix if wanted!!

            draw = ImageDraw.Draw(image)  # Declare Draw instance before prims


            #Set logo based on train_id above
            imagePath = '../images/%slogo.jpg' % train_id

            logo = Image.open(imagePath).convert('RGB')

            logo.thumbnail((13,13), Image.ANTIALIAS)



            draw.text((25,-3),'Brooklyn',font=font,fill='#239600')
            ##FFD302

            if times.index(i) < 2:

                #Get width of minutes text
                timewidth = draw.textsize(minutes)[0]

                draw.text((103-timewidth,-3),minutes,font=font,fill='#ff2a00')

            else:

                timewidth = draw.textsize(minutes)[0]

                draw.text((103-timewidth,-3),minutes,font=font,fill='#ff6600')

            draw.text((105,-3),'min',font=font,fill='#239600')

            logos.append(logo)

            images.append(image)

        matrix = initialize_matrix(brightness_arg)

        matrix.Clear()

        if len(images) < 3:

            pos = 0

            for i in range(len(images)):

                matrix.SetImage(images[i], 0, (pos*14)+3)

                matrix.SetImage(logos[i], 3, (pos*15)+2)

                pos += 1

            time.sleep(interval_arg - ((time.time() - starttime) % interval_arg))


        else:

            matrix.SetImage(images[0], 0,3)

            matrix.SetImage(logos[0], 3,2)

            images = images[1:]

            logos = logos[1:]

            count = 0

            while count <= interval_arg/display_time_arg:

                matrix.SetImage(images[(count%len(images))], 0,17)

                matrix.SetImage(logos[(count%len(images))], 3,17)

                #print 'count % len(images) = ' + str(count%len(images))

                count += 1

                time.sleep(display_time_arg)

def print_times():

    def run():

        global times

        while True:

            print(sorted(times))

            time.sleep(30)

    t = Thread(target=run())
    t.start()

# time.sleep(1)
# print_times()



if __name__ == '__main__':

    if len(sys.argv[1:]) != 3:

        print('must include 3 arguments: brightness, refresh interval, and display time interval')

    else:

        brightness_arg = int(sys.argv[1])

        interval_arg = float(sys.argv[2])

        display_time_arg = float(sys.argv[3])

        # print brightness_arg, interval_arg, display_time_arg

        # get_train_times()
        get_train_times()
        time.sleep(1)
        run()









