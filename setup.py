# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='image-recognition-tagger',
    version='0.1.0',
    description='Add keyword rekognized by AWS',
    author='Holger Protzek',
    author_email='h.protzek@icloud.com',
    url='https://github.com/hprotzek/image-keyword-tagger',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
          'image-recognition-tagger = src.image_keyword_tagger:main',
        ]
      }
)
