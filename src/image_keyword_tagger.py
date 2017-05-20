#!/usr/bin/env python

from argparse import ArgumentParser
from pyexif import ExifEditor
from os import environ
import boto3
import os
import json

class ImageKeywordTagger():

    def __init__(self, region, access_key, secret_key):
        self.client = self.get_client(region, access_key, secret_key)

    def readAndTagImages(self, start_dir):
        for root, dirs, files in os.walk(start_dir, topdown=True):
            dirs[:] = [d for d in dirs if d not in ['@eaDir']]
            for name in files:
                print (os.path.join(root, name))
                if name.endswith(('jpg','JPG')):
                    image = os.path.join(root, name)
                    self.writeKeywords(image, self.detectKeywords(image))

    def detectKeywords(self, image):
        keyword_list = []
        with open(image, 'rb') as image:
            response = self.client.detect_labels(Image={'Bytes': image.read()}, MinConfidence=80)
            for value in response['Labels']:
                keyword_list.append(value['Name'])
                print 'Found Keyword: ' + value['Name']
        return keyword_list

    def writeKeywords(self, image, keyword_list):
        editor = ExifEditor(image)
        editor.setKeywords(keyword_list)

    def get_client(self, region, access_key, secret_key):
        client = boto3.client('rekognition', region_name=region, endpoint_url='https://rekognition.'+region+'.amazonaws.com', verify=False,
                              aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        return client

def main():
    parser = ArgumentParser(description='Automatic image tagging')
    parser.add_argument('-r', '--region')
    parser.add_argument('-a', '--access_key')
    parser.add_argument('-s', '--secret_key')
    parser.add_argument('-d', '--start_dir')
    args = parser.parse_args()

    tagger = ImageKeywordTagger(args.region, args.access_key, args.secret_key)
    tagger.readAndTagImages(args.start_dir)

if __name__ == '__main__':
    main()
