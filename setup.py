from setuptools import find_packages, setup

setup(
    name='bitcoin-hd-seed',
    version='1.0',
    author='Evan Klitzke',
    author_email='evan@eklitzke.org',
    description='Extract the Bitcoin Core HD wallet seed',
    packages=find_packages('hdseed'),
    install_requires=['python-bitcoinrpc'],
    entry_points={'console_scripts': [
        'get-hd-seed = hdseed.getseed:main',
    ]})
