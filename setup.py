from setuptools import find_packages, setup

setup(
    name='subjunctive',
    version='0.1',
    install_requires=[
        'pysdl2 >=0.8.0',
    ],
    packages=find_packages(),
    scripts=[
        'games/think-green/think-green.py',
        'games/floorpaint/floorpaint.py',
    ],
)
