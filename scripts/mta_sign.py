from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions

from google.transit import gtfs_realtime_pb2
import requests
import datetime
import time as tm
import sys

#Q line feed id = 16
                            
def get_train_times():

    feed_id = [16,21,31,36]

    train_list=[]

    for ID in feed_id:

        while True:

            try:

                ##############################################################################################################

                feed = gtfs_realtime_pb2.FeedMessage()

                response = requests.get('http://datamine.mta.info/mta_esi.php?key=bb36bf7be031fc82f356395d2f08ad4e&feed_id=%s'% ID)

                #############PARSE#FEED#######################################################################################
                # While loop tries to parse feed until no error is raise#

                feed.ParseFromString(response.content)

                #print('ID')

            except:

                pass

            break

            ##############################################################################################################

                #Create empty list that will contain Train ID and Train times

                #train_list = []

        for i in feed.entity:

            for n in i.trip_update.stop_time_update:

                # Only get trains going to 86th Street Southbound

                if 'Q04S' in n.stop_id:

                    # Get time of train arrival
                    UTCtime = int(n.arrival.time)

                    # Get current time
                    UTCNow = int(tm.time())

                    # Calculate minutes until train arrives at station
                    UTCResult = UTCtime - UTCNow

                    # Convert minutes to string
                    if UTCResult < 0:

                        minutes = '0'

                    else:

                        minutes = datetime.datetime.fromtimestamp(UTCResult).strftime('%M')

                    # Append train id and train ETA in minute
                    train_list.append(minutes + "." + i.trip_update.trip.route_id)

        # Sort list by times instead of by train id
        train_list.sort()

        # print(train_list)

        #print(train_list)
    
    return train_list              

    



def listCheck():

    print('getting trains...')

    train_list = get_train_times()


    if len(train_list) < 1 or train_list == None:

        print('list is empty')

        while len(train_list) < 1 or train_list == None:

            print('trying again...')

            tm.sleep(1)

            train_list = get_train_times()

            print(train_list)
            
        else:

            print('success!')


            return train_list

            

    else:

        print('list acquired')

        return train_list




def listCheckTest():

    train_list = ['1.M','3.N','4.J','03.W','10.Q','15.B','30.R']

    return train_list





def displayTrainTimes():

    print('begin program')

    # Configuration for the matrix
    options = RGBMatrixOptions()

    options.rows = 32

    options.cols = 64

    options.chain_length = 2

    options.parallel = 1

    options.brightness = brightness_arg
    
    options.show_refresh_rate = 0

    options.hardware_mapping = 'adafruit-hat-pwm'  # If you have an Adafruit HAT: 'adafruit-hat'

    matrix = RGBMatrix(options = options)

    #Get time at start of program
    interval = interval_arg #Interval in seconds the program is run

    display_time = display_time_arg #Seconds each time is displayed
    
    starttime = tm.time()

    print('matrix settings initialized')

    

    while True:

        if int(tm.strftime('%H',tm.localtime())) > 22 or int(tm.strftime('%H',tm.localtime())) < 6:

            interval = interval_arg*2

            #print 'interval = ' + str(interval)

        else:

            interval = interval_arg

        train_times = listCheck()

        
        print(str(len(train_times)) + ' train(s) found at ' + tm.strftime('%H:%M',tm.localtime()))

        print(train_times)

        #########################################

        logos = []

        images = []

        minutesList = []

        zeros = []

        for i in range(len(train_times)):

            if str(train_times[i].split('.')[0]) == '00' or str(train_times[i].split('.')[0]) == '0':

                zeros.append(i)

        if len(zeros) > 0:

            del train_times[0:len(zeros)]

        else:

            pass



        #print(train_times)


        for i in range(len(train_times)):

            #Get the train letter/number
            train_id = train_times[i].split('.')[1]

            #Strip leading zeros and double zeros

            minutes = train_times[i].split('.')[0]


            minutes = minutes.lstrip('0')

            minutesList.append(minutes)


            #Get proper train logo
            train_id = train_id.lower()


            if  str(train_id) == 'q':

                pass

            elif str(train_id)!= 'r':

                pass

            elif str(train_id)!= 'n':

                pass

            elif str(train_id)!= 'w':

                pass

            elif str(train_id)!= 'm':

                pass
            elif str(train_id)!= 'b':

                pass
            elif str(train_id)!= 'd':

                pass
            elif str(train_id)!= 'f':

                pass
            elif str(train_id)!= 'j':

                pass
            elif str(train_id)!= 'z':

                pass

            else:

                train_id = 'q'


            #Set font
            font = ImageFont.truetype('/usr/share/fonts/truetype/piboto/Piboto-Light.ttf',13)

            fontEcho = ImageFont.truetype('/usr/share/fonts/truetype/piboto/Piboto-Light.ttf',10)



            #Create blank image
            image = Image.new("RGB", (128, 16))  # Can be larger than matrix if wanted!!

            draw = ImageDraw.Draw(image)  # Declare Draw instance before prims


            #Set logo based on train_id above
            imagePath = '/home/pi/rpi-rgb-led-matrix/bindings/python/images/%slogo.jpg' % train_id

            logo = Image.open(imagePath).convert('RGB')

            logo.thumbnail((13,13), Image.ANTIALIAS)



            draw.text((25,-3),'Brooklyn',font=font,fill='#239600')
            ##FFD302

            if i < 2:

                #Get width of minutes text
                timewidth = draw.textsize(minutes)[0]

                draw.text((103-timewidth,-3),minutes,font=font,fill='#ff2a00')

            else:

                timewidth = draw.textsize(minutes)[0]

                draw.text((103-timewidth,-3),minutes,font=font,fill='#ff6600')



            draw.text((105,-3),'min',font=font,fill='#239600')



            logos.append(logo)

            images.append(image)


        matrix.Clear()


        if len(images) < 3:

            pos = 0

            for i in range(len(images)):

                matrix.SetImage(images[i], 0, (pos*14)+3)

                matrix.SetImage(logos[i], 3, (pos*15)+2)

                pos += 1

            tm.sleep(interval - ((tm.time() - starttime) % interval))


        else:

                matrix.SetImage(images[0], 0,3)

                matrix.SetImage(logos[0], 3,2)

                images = images[1:]

                logos = logos[1:]

                count = 0

                while count <=interval/display_time:

                    matrix.SetImage(images[(count%len(images))], 0,17)

                    matrix.SetImage(logos[(count%len(images))], 3,17)

                    #print 'count % len(images) = ' + str(count%len(images))

                    count += 1

                    time.sleep(display_time)



if __name__ == '__main__':

    if len(sys.argv[1:]) != 3:

        print('must include 3 arguments: brightness, refresh interval, and display time interval')

    else:


        brightness_arg = int(sys.argv[1])

        interval_arg = float(sys.argv[2])

        display_time_arg = float(sys.argv[3])

        print(brightness_arg, interval_arg, display_time_arg)
       
        displayTrainTimes()