from setuptools import setup

setup(
    name='hhbot',
    version='0.1.0',    
    description='Python resume updater',
    license='pass',
    packages=['hhbot'],
    install_requires=['selenium',
                      'beautifulsoup4'                    
                      ]
)