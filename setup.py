from os import path

from setuptools import setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='extra-context',

    version='1.0.0',

    description='Add additional context to warnings and exceptions',

    long_description=long_description,

    long_description_content_type='text/markdown',

    url='https://github.com/WanzenBug/extra-context-py',

    author='Moritz "WanzenBug" Wanzenböck',

    author_email='moritz.wanzenboeck@gmail.com',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: System :: Logging',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    keywords='warnings exception context logging',

    py_modules=[
        'extra_context',
    ],

    extras_require={  # Optional
        'test': ['pytest'],
    },

    project_urls={  # Optional
        'Bug Reports': 'https://github.com/WanzenBug/extra-context-py/issues',
        'Source': 'https://github.com/WanzenBug/extra-context-py',
    },
)
