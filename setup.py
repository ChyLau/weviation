try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Weight estimation tool for commercial transport aircrafts',
    'author': 'Chy Lau',
    'url': 'https://github.com/ChyLau/weviation',
    'download_url': 'https://github.com/ChyLau/weviation',
    'author_email': 'chyho.lau@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['weviation'],
    'scripts': [],
    'name': 'weviation'
}

setup(**config)
