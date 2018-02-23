""" Setuptools setup file for RDFSerializer """

from setuptools import setup


setup(
    name='rdfserializer',
    version='1.0.0b1',
    description='A small library to serialize Django models to RDF',
    url='https://github.com/severus21/RDFSerializer',
    author='Laurent Prosperi',
    classifiers=[
        'Development Status :: 4 - Beta',
        # 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        # ^ @severus21: this is a wild guess, please replace with anything that
        # seems appropriate to you -- FIXME
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3',
    keywords='django rdf',
    install_requires=[
        'django',
        'rdflib',
    ],
    py_modules=[
        '__init__',
        'rdfserializer.__init__',
    ],
    entry_points={
        'console_scripts': [
        ]
    }
    )
