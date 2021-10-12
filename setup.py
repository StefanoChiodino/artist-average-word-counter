from distutils.core import setup

from setuptools import find_packages

setup(
    name="ArtistAverageWordCounter",
    version="0.1",
    packages=find_packages(where="src"),
    license="Creative Commons Attribution-Noncommercial-Share Alike license",
    long_description=open("README.md").read(),
    package_dir={'': 'src'},
    entry_points={
        "console_scripts": [
            "artist-average-word-counter = artist_average_word_counter:main",
        ],
    },
    extras_require={
        'dev': ['check-manifest'],
    },
    install_requires=[
        "musicbrainzngs == 0.7.1",
        "requests == 2.26.0",
        "tqdm ~= 4.62.3",
    ],
)
