import sys
import exiftool

extentions = ["jpg", "jpeg", "png", "gif", "bmp"]
files = sys.argv[1:]

def print_metadata(file):
    with exiftool.ExifToolHelper() as ext:
        metadata = ext.get_metadata(file)
        for line in metadata:
            for key, value in line.items():
                ky = key.split(":")[-1]
                vl = value
                print(f"{ky : <25}{':' : ^20}{vl}")

for file in files:
    if file.split(".")[-1] in extentions:
        metadata = print_metadata(file)
        print("**********************************************************************")
    else:
        print("error extracting metadata")