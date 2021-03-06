#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


BASEDIR = os.path.dirname(__file__)


def get_version(*file_paths):
    """Retrieves the version from dcengine/base.py"""
    filename = os.path.join(BASEDIR, *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^VERSION = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')

version = get_version("dcengine", "base.py")


if sys.argv[-1] == 'publish':
    try:
        import wheel
        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open(os.path.join(BASEDIR, 'README.rst')).read()

setup(
    name='dcengine',
    version=version,
    description="""Wrapper for django-channels for creating websocket engines.""",
    long_description=readme,
    author='avigmati',
    author_email='avigmati@gmail.com',
    url='https://github.com/avigmati/dcengine',
    packages=[
        'dcengine',
    ],
    include_package_data=True,
    license="BSD",
    zip_safe=False,
    keywords='django channels engine',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
