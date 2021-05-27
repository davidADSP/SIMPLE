from setuptools import setup, find_packages

setup(
    name='frouge',
    version='0.1.0',
    description='Flamme Rouge Gym Environment',
    packages=find_packages(),
    install_requires=[
        'gym>=0.9.4',
        'numpy>=1.13.0',
        'opencv-python>=3.4.2.0',
    ]
)


