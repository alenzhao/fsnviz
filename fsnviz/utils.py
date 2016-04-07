# -*- coding: utf-8 -*-
"""
    fsnviz.utils
    ~~~~~~~~~~~~

    General utilities.

    :copyright: (c) 2016 Wibowo Arindrarto <bow@bow.web.id>
    :license: BSD

"""
import os
import sys
from os import path
from subprocess import run, PIPE

import click


if sys.version_info[0] > 2:
    basestring = str


def is_exe(fname):
    """Returns whether the given file name is an executable file or not."""
    return path.isfile(fname) and os.access(fname, os.X_OK)


# Adapted from:
# https://stackoverflow.com/questions/377017/test-if-executable-exists-in-python/377028#377028
def which(program):
    """Resolves the absolute path to a program's executable."""
    dir_part, fname = path.split(program)

    if dir_part:
        dir_abs = os.getcwd() if dir_part == "." else path.realpath(dir_part)
        exe_file = path.join(dir_abs, program)
        if is_exe(exe_file):
            return exe_file
        msg = "Could not find an executable circos at '{0}'."
        raise click.BadParameter(msg.format(program))

    for env_path in os.environ.get("PATH", "").split(os.pathsep):
        exe_file = path.join(env_path, program)
        if is_exe(exe_file):
            return exe_file

    msg = "Could not find the circos executable."
    raise click.BadParameter(msg)


def which_circos(exe="circos"):
    """Returns the absolute path to the circos executable."""
    circos_exe = which(exe)
    mod_test = run([circos_exe, "-modules"], stdout=PIPE, stderr=PIPE)
    if mod_test.returncode != 0:
        msg = "Unexpected error when running circos executable '{0}'."
        raise click.BadParameter(msg.format(circos_exe))
    mod_test_lines = mod_test.stdout.decode().split(os.linesep)
    all_modules_ok = all([x.startswith("ok")
                          for x in filter(None, mod_test_lines)])
    if not all_modules_ok:
        msg = "Some required Perl modules for circos can not be found."
        raise click.BadParameter(msg)
    return circos_exe
