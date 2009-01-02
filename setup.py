from setuptools import setup, find_packages
import sys, os

import pydirduplicatefinder

setup(name='PyDirDuplicateFinder',
      py_modules=['pydirduplicatefinder',],
      scripts=['pydirduplicatefinder.py',],
      version=pydirduplicatefinder.version,
      description=pydirduplicatefinder.description,
      long_description=open(os.path.join("docs", "README.txt")).read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: End Users/Desktop",
                   "License :: OSI Approved :: GNU General Public License (GPL)",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 2.5",
                   "Topic :: Desktop Environment :: File Managers",
                   "Topic :: Utilities"], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='filesystem file duplicate directory utility',
      author='Keul',
      author_email='lucafbb@gmail.com',
      url='http://keul.it/develop/python/pydirduplicatefinder/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
