#!/usr/bin/env python

from argparse import ArgumentParser
from pyexif import ExifEditor
from os import environ
import boto3
import os
import json

class ImageKeywordTagger():

    def __init__(self, region, endpoint, access_key, secret_key):
        self.client = get_client(region, endpoint, access_key, secret_key)

    def readAndTagImages(self, start_dir):
        for root, dirs, files in os.walk(start_dir, topdown=False):
            for name in files:
                if name.endswith(('jpg','JPG')):
                    image = os.path.join(root, name)
                    self.writeKeywords(self.detectKeywords(image))

    def detectKeywords(self, image):
        keyword_list = []
        with open(image, 'rb') as image:
            response = self.client.detect_labels(Image={'Bytes': image.read()})
            for value in response['Labels']:
                keyword_list.append(value['Name'])
        return keyword_list

    def writeKeywords(image, keyword_list):
        editor = ExifEditor(image)
        editor.setKeywords(keyword_list)

    def get_client(region, endpoint, access_key, secret_key):
        client = boto3.client('rekognition', region_name=region, endpoint_url=endpoint, verify=False,
                              aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        return client

def get_args():
    parser = ArgumentParser(description='Automatic image tagging')
    parser.add_argument('-r', '--region')
    parser.add_argument('-e', '--endpoint')
    parser.add_argument('-a', '--access_key')
    parser.add_argument('-s', '--secret_key')
    parser.add_argument('-d', '--start_dir')
    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    tagger = ImageKeywordTagger(args.region, args.endpoint, args.access_key, args.secret_key)
    tagger.readAndTagImages(args.start_dir)
