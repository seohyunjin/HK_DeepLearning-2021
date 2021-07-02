with open('etriaikey.txt') as kfile:
    etri_key = kfile.read()

import os
import urllib3
import json
import base64
from glob import glob
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

openApiURL = 'http://aiopen.etri.re.kr:8000/ObjectDetect'
http = urllib3.PoolManager()

def detective(folder_name) :
    for img_file in glob(f'{folder_name}/*') :
        _, img_type = os.path.splitext(img_file)
        img_type = 'jpg' if img_type == '.jfif' else img_type[1:]

        with open(img_file, 'rb') as file :
            img_contents = base64.b64encode(file.read()).decode("utf8")

        requestJson = {
            "access_key": etri_key,
            "argument": {
                "type": img_type,
                "file": img_contents}
                }

        response = http.request(
            "POST",
            openApiURL,
            headers={"Content-Type": "application/json; charset=UTF-8"},
            body=json.dumps(requestJson)
            )

        result = json.loads(response.data)
        obj_list = result['return_object']['data']

        image = Image.open(img_file)
        draw = ImageDraw.Draw(image)
        
        for obj in obj_list :
            name = obj['class']
            x = int(obj['x'])
            y = int(obj['y'])
            w = int(obj['width'])
            h = int(obj['height'])
            draw.text((x+10,y+10), name, font=ImageFont.truetype('malgun.ttf',20), fill=(255,0,0))
            draw.rectangle(((x, y), (x + w, y + w)), outline = (255, 0, 0), width = 2)

        
        plt.figure(figsize = (12, 8))
        plt.imshow(image)
        print(plt.show())