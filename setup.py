from distutils.core import setup
from setuptools import find_packages

options = {
    "apk": {
          "package": "ovh.collonval.space_invader",
          "requirements": "python3,kivy",
          "android-api": "27",
          "ndk-api": "21",
          "dist-name": "space_invader",
          "ndk-version": "r16b"
    }
}

setup(
    name='space_invader',
    version='0.2',
    description="Top-Down space shooter game.",
    url= "https://github.com/fcollonval/shooter",
    author = "Frederic Collonval",
    author_email = "fcollonval@gmail.com",
    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7"
    ],
    zip_safe = False,
    install_requires = ["kivy==1.10.1"],
    packages=find_packages(),
    package_data={
        'space_invader': [
            '*.py', '*.kv',
            'img/space_invader-*.png', 'img/space_invader.atlas', 'img/bg/*.png',
            'font/*.ttf',
            'sounds/*.ogg'
        ]
    },
    options=options
)
