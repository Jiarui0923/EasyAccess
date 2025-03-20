"""Package installer."""
from setuptools import find_packages, setup
import os

LONG_DESCRIPTION = '''
EasyAccess is a Python package designed to seamlessly connect to and interact with EasyAPI. This package provides a user-friendly interface to access EasyAPI's algorithms as if they were local Python functions, simplifying remote computation tasks. It also includes features for automatic organization and visualization of documentation, making it easier to understand and use available functionalities.

This package is ideal for developers and researchers looking for a straightforward way to leverage EasyAPI's computational capabilities while maintaining a Pythonic workflow.

For detailed usage instructions, installation steps, and API references, please refer to the documentation included with the project or explore the source code.

If there is any issue, please put up with an issue or contact Jiarui Li (jli78@tulane.edu)
'''
VERSION = '1.0.3'
NAME = 'EasyAccess'

setup(
    name=NAME,
    version=VERSION,
    description='Access EasyAPI algorithms and documentations seamlessly.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author='Jiarui Li, Marco K. Carbullido, Jai Bansal, Samuel J. Landry, Ramgopal R. Mettu',
    author_email=('jli78@tulane.edu'),
    url='https://github.com/Jiarui0923/EasyAccess',
    license='GPLv3',
    install_requires=[
        'requests',
        'websocket-client',
        'pandas',
        'markdown',
        'docflow @ git+https://github.com/Jiarui0923/DocFlow@1.0.0'
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GPLv3 License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=find_packages('.'),
    platforms=["any"],
    zip_safe=True,
)
