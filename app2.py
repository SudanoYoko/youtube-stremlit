from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
import streamlit as st
from PIL import ImageDraw
from PIL import ImageFont

import json

with open('secret.json') as f:
    secret = json.load(f)

KEY = secret['key']
ENDPOINT = secret['endpoint']

computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(KEY))

def get_tags(filepath):
    local_image = open(filepath, "rb")

    tags_result = computervision_client.tag_image_in_stream(local_image)
    tags = tags_result.tags
    tags_names = []
    for tag in tags:
        tags_names.append(tag.name)
    
    return tags_names

def detect_objects(filepath):
    local_image = open(filepath, "rb")

    detect_objects_results = computervision_client.detect_objects_in_stream(local_image)
    objects = detect_objects_results.objects
    return objects


st.title('物体検出アプリ')

# file_uploaderではファイルパスの取得はできない
uploaded_file = st.file_uploader('Choose an image...', type=[
    'jpg', 'png'
])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    img_path = f'img/{uploaded_file.name}'
    img.save(img_path)
    objects = detect_objects(img_path)

    # 矩形描画
    draw = ImageDraw.Draw(img)
    for object in objects:
        x = object.rectangle.x
        y = object.rectangle.y
        w = object.rectangle.w
        h = object.rectangle.h
        caption = object.object_property

        draw.rectangle([(x, y),(x+w, y+h)], fill=None, outline='green', width=15)

        font = ImageFont.truetype('./Togalite-Regular.otf', size=50)
        text_w, text_h = draw.textsize(caption, font=font)
        draw.rectangle([(x,y), (x+text_w, y+text_h)], fill='green', outline=None)
        draw.text((x, y), caption, fill='white', font=font)

    st.image(img)

    tags_name = get_tags(img_path)

    st.markdown('**認識されたコンテンツタグ**')
    st.markdown(', '.join(tags_name))