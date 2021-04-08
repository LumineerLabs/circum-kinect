from setuptools import setup, find_packages
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


test_requirements = [
    'pytest',
    'pytest-cov',
]

setup(
    name='circum_kinect',
    version_format='{tag}',
    author="Lane Haury",
    author_email="lane@lumineerlabs.com",
    description="Kinect sensor plugin for circum.",
    license="MIT",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/LumineerLabs/circum-kinect",
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        'circum',
        'click',
    ],
    setup_requires=[
        'setuptools',
        'setuptools-git-version',
    ],
    tests_require=test_requirements,
    entry_points={
        'circum.sensors': [
            'kinect=circum_kinect.kinect:kinect'
        ]
    },
    extras_require={
        'lint': [
            'flake8',
            'flake8-import-order',
            'flake8-builtins',
            'flake8-comprehensions',
            'flake8-bandit',
            'flake8-bugbear',
        ],
        'pykinect': [
            'pykinect @ https://github.com/LumineerLabs/PTVS/archive/9c9b02416e46a8661fd324a5d66f9b32dff0b55a.zip'
        ],
        'pykinect2': [
            'pykinect2 @ https://github.com/LumineerLabs/PyKinect2/archive/81f9a55d5ceeec342dc0c95b0f8084b5816aca08.zip',
        ],
        'test': test_requirements,
    }
)
