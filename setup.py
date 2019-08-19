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
    long_description_content_type='text/markdown',
    install_requires=[],
    include_package_data=True,
    url='http://github.com/jthanwer/coriolis',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Topic :: Communications",
    ],
    entry_points={
        'console_scripts': [
            'coriolis = coriolis.__main__:main',
        ],
    }
)
