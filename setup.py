"""wpgtk - setup.py"""
import setuptools
import os
import shutil

try:
    import wpgtk
except (ImportError, SyntaxError):
    print("error: wpgtk requires Python 3.5 or greater.")
    quit(1)


try:
    import pypandoc
    LONG_DESC = pypandoc.convert("README.md", "rst")
except(IOError, ImportError, RuntimeError):
    LONG_DESC = open('README.md').read()


VERSION = "4.5"
DOWNLOAD = "https://github.com/dylanaraps/pywal/archive/%s.tar.gz" % VERSION
WALL_DIR = os.path.expanduser('~') + '/.wallpapers'


setuptools.setup(
    name="wpgtk",
    packages=setuptools.find_packages(),
    version=VERSION,
    author="Fernando Vásquez",
    author_email="fmorataya.04@gmail.com",
    description="GTK+ theme/wallpaper manager which uses pywal as it's core",
    long_description=LONG_DESC,
    license="GPL2",
    url="https://github.com/deviantfero/wpgtk",
    download_url=DOWNLOAD,
    classifiers=[
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6",
    ],
    entry_points={
        "console_scripts": ["wpg=wpgtk.__main__:main"]
    },
    python_requires=">=3.5",
    install_requires=[
        'certifi>=2017.7.27.1',
        'chardet>=3.0.4',
        'idna<2.6',
        'olefile>=0.44',
        'Pillow>=4.2.1',
        'requests>=2.18.3',
        'pywal>=0.6.0',
        'ruamel.yaml>=0.15.23',
        'urllib3>=1.22',
    ],
    include_package_data=True,
    data_files=[('/etc/wpgtk', ['wpgtk/misc/wpg.conf']),
                ('/usr/local/bin/', ['wpgtk/misc/wpg-install.sh'])]
)
