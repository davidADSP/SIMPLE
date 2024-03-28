from setuptools import setup, find_packages

setup(
    name='frouge',
    version='0.1.0',
    description='Flamme Rouge Gym Environment',
    packages=find_packages(),
    install_requires=[
        'gymnasium==0.29.1',
        'numpy>=1.13.0',
        'opencv-python>=3.4.2.0',
        'shimmy>=0.2.1',
        'sb3-contrib==2.2.1',
        'nicegui==1.4.18'
    ]
)


