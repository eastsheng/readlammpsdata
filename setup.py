"""run this
python setup.py sdist
pip install .
twine upload dist/*
"""

from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt","r") as f:
    required = f.read().splitlines()


setup(
name         = 'readlammpsdata',
version      = '1.0.1',
py_modules   = ['readlammpsdata'],
author       = 'CHENDONGSHENG',
author_email = 'eastsheng@hotmail.com',
packages=find_packages('src'),
package_dir={'': 'src'},
install_requires=required,
url          = 'https://github.com/eastsheng/readlammpsdata',
description  = 'Read lammps data infomations.',
long_description=long_description,
long_description_content_type='text/markdown'
)

