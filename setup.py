from setuptools import setup, find_packages
import os



setup_path = os.path.dirname(os.path.realpath(__file__))
tailor_path = os.path.join(setup_path, "tailor")


home_data = "def get_tailor_path():\n\treturn'" + tailor_path + "'\n"
home_data += "\n\n\ndef get_crab_home():\n\treturn'" + setup_path + "'\n"

file = open(os.path.join(tailor_path, "home.py"), "w")
file.write(home_data)
file.close() 


setup(
    name='tailor',
    version='1.0',
    description='Automatically tailoring abstract interpretation to custom usage scenarios',
    author='Numair Mansur',
    author_email='numair@mpi-sws.org',
    url='https://numairmansur.github.io/',
    keywords='Abstract Interpretation, Optimization',
    packages=find_packages(),
    install_requires=['termcolor', 'pyfiglet'],
    entry_points={
        'console_scripts': ['tailor = tailor.__main__:main']
    }
)
