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
    if not info:
        return exif_data
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        exif_data[decoded] = value
        if decoded == "GPSInfo":
            gps_data = {}
            for t in value:
                sub_decoded = GPSTAGS.get(t, t)
                gps_data[sub_decoded] = value[t]

            exif_data[decoded] = gps_data
    return exif_data


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

        gps_latitude = gps_info.get('GPSLatitude', None)
        gps_latitude_ref = gps_info.get('GPSLatitudeRef', None)
        gps_longitude = gps_info.get('GPSLongitude', None)
        gps_longitude_ref = gps_info.get('GPSLongitudeRef', None)

        if all([gps_latitude, gps_latitude_ref, gps_longitude, gps_longitude_ref]):
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
    def should_process_file(fn):
        valid_exts = ['JPG', 'TIF', 'WAV']
        _, ext = os.path.splitext(fn)
        return os.path.isfile(fn) and ext.upper() in valid_exts
    os.chdir(absolute_path)
    print(os.listdir('.'), os.path.abspath(os.curdir))
    for number, file in enumerate(os.listdir()):
        if should_process_file(file):
            print (number,':',file)
            _, ext = os.path.splitext(file)
            try:
                date_formatted = pulling_metadata_date(file)
                folder_name = (str(date_formatted[:4])+'-'+str(date_formatted[5:7]))
                os.mkdir('{}'.format(folder_name))
            except KeyError:
                print('Images Do not Contain Date Information in their METADATA')
                continue
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

def ask_and_confirm(question):
    ans1 = input(question)
    ans2 = input("Please confirm my repeating response:\n")
    if ans1 == ans2:
        return ans1
    return None


def ask_until_confirmed(question):
    address = None
    while not address:
        address = ask_and_confirm(question)
    return address


def main():
    question = "Enter Directory with pictures you wish to organise by Date YYYY-MM:\n"
    address = ask_until_confirmed(question)
    if os.path.isdir(confirm_directory_address):
        File_Date_Organiser(directory_address)
    else:
        print("Directory: {}\nDoes Not Exist".format(confirm_directory_address))#Put the Explicit directory of the folder you wish to organise
        main()

if __name__ == "__main__":
    main()
