import os
import os.path
import shutil
import errno
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


'''
EXIF Data Program below taken from ..... (Find the website)
'''

def get_exif_data(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    return exif_data


def _get_if_exist(data, key):
    if key in data:
        return data[key]

    return None


def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)


def get_lat_lon(exif_data):
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
    lat = None
    lon = None

    if "GPSInfo" in exif_data:
        gps_info = exif_data["GPSInfo"]

        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":
                lat = 0 - lat

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon

    return lat, lon

'''
Programming Below was Created by John
'''

def pulling_metadata_date(image_name):
    image = Image.open(image_name)
    exif_data = get_exif_data(image)
    return exif_data['DateTimeOriginal']


def File_Date_Organiser(absolute_path):


    os.chdir(absolute_path)
    print(os.listdir('.'), os.path.abspath(os.curdir))
    for number, file in enumerate(os.listdir()):
        if os.path.isfile(file):
            print (number,':',file)
            if file.upper().endswith('.JPG') or file.endswith('.TIF') or file.endswith('.WAV'):

                try:
                    date_formatted = pulling_metadata_date(file)
                except KeyError as KError:
                    print('Images Do not Contain Date Information in their METADATA')
                    continue
                try:
                    folder_name = (str(date_formatted[:4])+'-'+str(date_formatted[5:7]))
                    os.mkdir('{}'.format(folder_name))
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise exc
                shutil.move(file, '{}'.format(folder_name))
                print('Complete')

            else:
                print("Picture Format: .{}\nDoes not contain META info".format(file.upper().split(".")[1]))


'''
CHANGE DIRECTORY BELOW
'''
File_Date_Organiser("C:\Example") #Put the Explicit directory of the folder you wish to organise
#Update to something prettier