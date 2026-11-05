import os
from PIL import Image, ImageOps
from PIL.ExifTags import TAGS
SUPPORTED_FORMATS = ['jpg','jpeg','JPG','JPEG','png','PNG','webp','WEBP']

print("""
 /$$   /$$                 /$$             /$$               /$$                
| $$$ | $$                | $$            | $$              | $$                
| $$$$| $$  /$$$$$$   /$$$$$$$  /$$$$$$  /$$$$$$    /$$$$$$ | $$   /$$  /$$$$$$ 
| $$ $$ $$ /$$__  $$ /$$__  $$ |____  $$|_  $$_/   |____  $$| $$  /$$/ |____  $$
| $$  $$$$| $$  \\ $$| $$  | $$  /$$$$$$$  | $$      /$$$$$$$| $$$$$$/   /$$$$$$$
| $$\\  $$$| $$  | $$| $$  | $$ /$$__  $$  | $$ /$$ /$$__  $$| $$_  $$  /$$__  $$
| $$ \\  $$|  $$$$$$/|  $$$$$$$|  $$$$$$$  |  $$$$/|  $$$$$$$| $$ \\  $$|  $$$$$$$
|__/  \\__/ \\______/  \\_______/ \\_______/   \\___/   \\_______/|__/  \\__/ \\_______/
                                                                                
""")
def plbs():
    print("________________________________________________________________________________")
plbs()
print()

userinput = input(">>> Select a file or folder to proceed (finish the folder with '/' or '\'):\n")
if userinput[-1] == "/" or userinput[-1] == "\\":
    target = "folder"
else:
    target = "file"
print(f"Detected : {target}")
print()

files:list[str] = []
# search da file
try:
    path = os.path.join(os.getcwd(),userinput)
    if target=="file":
        if not os.path.isfile(path):
            raise FileNotFoundError(f"File {path} not found !")
        files.append(path)
    else:
        if not os.path.isdir(path):
            raise FileNotFoundError(f"Directory {path} doesn't exist...")
        os.chdir(path)
        fx = os.listdir()
        for fprcs in fx:
            if not os.path.isfile(fprcs):
                print(Warning(f"This thing {path+fprcs} is not a correct file !"))
                continue
            files.append(fprcs)
except Exception as err:
    raise err
else:
    if len(files)==0:
        raise UserWarning("No file to proceed with !")
    imgs = []
    for file in files:
        f = file.split(".")
        if f[-1] in SUPPORTED_FORMATS:
            imgs.append(file)

delposs = False
for img in imgs:
    try:
        print()
        image = Image.open(img)

        print(f">>>>>> Currently analysing {img} <<<<<<")

        if image.getexif() == None:
            print(f"{img} does not contain any metadata.")
        else:
            delposs = True
            for tag,value in image.getexif().items():
                tag_name = TAGS.get(tag)
                print(f"{tag_name} >> {value}")
            if image.info:
                for key, value in image.info.items():
                    print(f"{key} >>> {value}")
        plbs()
        print()
    except IOError: # in case of
        print("File format not supported!") 
    except Exception as err:
        raise err

if delposs:
    print("Do you want to delete the metadata for those files ? (y/Y)")
    cs = input("Note this action will overwrite your existing files : ")
    if cs.lower()=='y':
        for img in imgs:
            try:
                with Image.open(img) as image:
                    image.load()
                    image = ImageOps.exif_transpose(image)
                    if image.mode == "P":
                        if "transparency" in image.info:
                            image = image.convert("RGBA")
                        else:
                            image = image.convert("RGB")
                    img_data = list(image.getdata())
                    img_no_exif = Image.new(image.mode,image.size)
                    img_no_exif.putdata(img_data)
                    img_no_exif.save(img)

                    nimg = Image.new(image.mode,image.size)
                    nimg.putdata(img_data)

                    extension = img.split('.')[-1]
                    if extension.lower()=='png':
                        fmt = "PNG"
                        nimg.save(img, format=fmt, optimize=True)
                    elif extension.lower()=='webp':
                        fmt = "WEBP"
                        nimg.save(img, format=fmt, lossless=True)
                    else: #jpeg and jpg
                        fmt = extension.upper()
                        nimg.save(img)
            except IOError:
                print("File format not supported!")
            except Exception as err:
                raise err

print("Process completed.")