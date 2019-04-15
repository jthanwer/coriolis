from setuptools import setup, find_packages

# notez qu'on import la lib
# donc assurez-vous que l'importe n'a pas d'effet de bord
import coriolis

setup(
    name='coriolis',
    version=coriolis.__version__,
    packages=find_packages(),
    author="Joel Thanwerdas",
    author_email="joel.thanwerdas@gmail.com",
    description="Quick visualization python software for NetCDF files",
    long_description=open('README.md').read(),
    install_requires=['matplotlib>=3.0.3', 'xarray>=0.11.3',
                      'netcdf4>=1.4.2', 'PyQt5>=5.12.1'],
    include_package_data=True,
    url='http://github.com/jthanwer/coriolis',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7.3",
        "Topic :: Communications",
    ],
    entry_points={
        'console_scripts': [
            'coriolis = coriolis.__main__:main',
        ],
    }
)
