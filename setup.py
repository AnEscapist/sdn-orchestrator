from setuptools import setup, find_packages

setup(
    mane='ucpe',
    version='1.0',
    description='',
    author='intern',
    author_email='',
    pachages=find_packages(),
    py_modules=['ucpe'],
    install_requires=[
        'docker',
        'paramiko',
        'click'
    ],
    entry_points='''
        [console_scripts]
        ucpe=ucpe.cli:start
    '''
)
