import os
import shutil
import re
import logging
from subprocess import Popen, check_output
from pywal.colors import cache_fname, list_backends

from os.path import join, basename
from .config import (
    settings,
    WALL_DIR,
    WPG_DIR,
    OPT_DIR,
    SAMPLE_DIR,
)

def __check_is_pywal16cols():
    raw_output = check_output(["wal", "-h"])

    if "--cols16" in raw_output.decode("utf-8"):
        return True

    return False


def get_file_list(path=WALL_DIR, regex=None):
    """gets file names in a given directory, optional regex
    parameter to filter the list of files by."""

    files = []

    for _, _, filenames in os.walk(path):
        files.extend(filenames)
        break

    files.sort()

    if regex is not None:
        valid = re.compile(regex)
        return [elem for elem in files if valid.fullmatch(elem)]
    else:
        return files


def write_script(wallpaper, colorscheme):
    """writes the script that should be called on startup
    to restore the theme."""
    set_wall = settings.getboolean("set_wallpaper", True)
    light_theme = settings.getboolean("light_theme", True)

    flags = "-L" if light_theme else "-"
    flags += "rs" if set_wall else "nrs"

    with open(join(WPG_DIR, "wp_init.sh"), "w") as script:
        command = "wpg %s '%s' '%s'" % (flags, wallpaper, colorscheme)
        script.writelines(["#!/usr/bin/env bash\n", command])
        Popen(['chmod', '+x', join(WPG_DIR, "wp_init.sh")])


def get_cache_path(wallpaper, backend=None):
    """get a colorscheme cache path using a wallpaper name"""
    if not backend:
        backend = settings.get("backend", "wal")

    filepath = join(WALL_DIR, wallpaper)
    # placeholder for variable
    filename = None

    try:
        filename = cache_fname(filepath, backend, False, WPG_DIR)
    except TypeError as error:
        # in pywal16cols this function have another api
        if __check_is_pywal16cols():
            # pywal16cols add boolean after `backend` that means 16cols mode or standart wal
            filename = cache_fname(filepath, backend, True, False, WPG_DIR) 
        else: raise error
    return join(*filename)


def get_sample_path(wallpaper, backend=None):
    """gets a wallpaper colorscheme sample's path"""
    if not backend:
        backend = settings.get("backend", "wal")

    sample_filename = "%s_%s_sample.png" % (wallpaper, backend)

    return join(SAMPLE_DIR, sample_filename)


def add_template(cfile, bfile=None):
    """adds a new base file from a config file to wpgtk
    or re-establishes link with config file for a
    previously generated base file"""
    cfile = os.path.realpath(cfile)

    if bfile:
        template_name = basename(bfile)
    else:
        clean_atoms = [atom.lstrip(".") for atom in cfile.split("/")[-3::]]
        template_name = "_".join(clean_atoms) + ".base"

    try:
        shutil.copy2(cfile, cfile + ".bak")
        src_file = bfile if bfile else cfile

        shutil.copy2(src_file, join(OPT_DIR, template_name))
        os.symlink(cfile, join(OPT_DIR, template_name.replace(".base", "")))

        logging.info("created backup %s.bak" % cfile)
        logging.info("added %s @ %s" % (template_name, cfile))
    except Exception as e:
        logging.error(str(e.strerror))


def delete_template(basefile):
    """delete a template in wpgtk with the given
    base file name"""
    base_file = join(OPT_DIR, basefile)
    conf_file = base_file.replace(".base", "")

    try:
        os.remove(base_file)
        if os.path.islink(conf_file):
            os.remove(conf_file)
    except Exception as e:
        logging.error(str(e.strerror))


def delete_colorschemes(colorscheme):
    """delete all files related to the given colorscheme"""
    for backend in list_backends():
        try:
            os.remove(get_cache_path(colorscheme, backend))
            os.remove(get_sample_path(colorscheme, backend))
        except OSError:
            pass


def change_current(filename):
    """update symlink to point to the current wallpaper"""
    os.symlink(join(WALL_DIR, filename), join(WPG_DIR, ".currentTmp"))
    os.rename(join(WPG_DIR, ".currentTmp"), join(WPG_DIR, ".current"))
