from setuptools import setup, find_packages

setup(
    name='md5ls',
    version='0.1.0',
    packages=find_packages(),
    description='Python script for generating and comparing lists of filenames and hashes',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    url='https://github.com/slbelden/md5ls.py',
    author='Stephen Lee Belden',
    author_email='belden.stephen@gmail.com',
    license='MIT',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'md5ls=md5ls.cli:main',
        ],
    },
)
