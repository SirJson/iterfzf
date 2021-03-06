from __future__ import print_function

import errno
import os.path
import subprocess
import sys
from enum import Enum
from shutil import which

__all__ = 'EXECUTABLE_PATH', 'iterfzf', 'LayoutStyle', 'InfoStyle'

EXECUTABLE_NAME = 'fzf.exe' if sys.platform == 'win32' else 'fzf'
EXECUTABLE_PATH = which(EXECUTABLE_NAME) if not None else None


class LayoutStyle(Enum):
    DEFAULT = 'default'
    REVERSE = 'reverse'
    REVERSE_LIST = 'reverse-list'


class InfoStyle(Enum):
    DEFAULT = 'default'
    INLINE = 'inline'
    HIDDEN = 'hidden'


def iterfzf(
    # CHECK: When the signature changes, __init__.pyi file should also change.
    iterable,
    # Search mode:
    extended=True, exact=False, case_sensitive=None,
    # Interface:
    multi=False, mouse=True, print_query=False, cycle=False, header=None,
    # Layout:
    prompt='> ',
    preview=None,
    border=False,
    info=None,
    margin=None,
    layout=None,
    # Misc:
    query='', encoding=None, executable=EXECUTABLE_PATH
):
    if executable is None:
        print("fzf is missing but required to run this script")
        print("See https://github.com/junegunn/fzf#installation for instructions")
        sys.exit(1)
    cmd = [executable, '--no-sort', '--prompt=' + prompt]
    if not extended:
        cmd.append('--no-extended')
    if case_sensitive is not None:
        cmd.append('+i' if case_sensitive else '-i')
    if exact:
        cmd.append('--exact')
    if multi:
        cmd.append('--multi')
    if not mouse:
        cmd.append('--no-mouse')
    if print_query:
        cmd.append('--print-query')
    if query:
        cmd.append('--query=' + query)
    if preview:
        cmd.append('--preview=' + preview)
    if border:
        cmd.append('--border')
    if header:
        cmd.append('--header=' + header)
    if cycle:
        cmd.append("--cycle")
    if info:
        cmd.append("--info=" + info.value)
    if margin:
        cmd.append("--margin=" + margin)
    if layout:
        cmd.append("--layout=" + layout.value)

    encoding = encoding or sys.getdefaultencoding()
    proc = None
    stdin = None
    byte = None
    lf = u'\n'
    cr = u'\r'
    for line in iterable:
        if byte is None:
            byte = isinstance(line, bytes)
            if byte:
                lf = b'\n'
                cr = b'\r'
        elif isinstance(line, bytes) is not byte:
            raise ValueError(
                'element values must be all byte strings or all '
                'unicode strings, not mixed of them: ' + repr(line)
            )
        if lf in line or cr in line:
            raise ValueError(r"element values must not contain CR({1!r})/"
                             r"LF({2!r}): {0!r}".format(line, cr, lf))
        if proc is None:
            proc = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=None
            )
            stdin = proc.stdin
        if not byte:
            line = line.encode(encoding)
        try:
            stdin.write(line + b'\n')
            stdin.flush()
        except IOError as e:
            if e.errno != errno.EPIPE:
                raise
            break
    if proc is None or proc.wait() not in [0, 1]:
        if print_query:
            return None, None
        else:
            return None
    try:
        stdin.close()
    except IOError as e:
        if e.errno != errno.EPIPE:
            raise
    stdout = proc.stdout
    decode = (lambda b: b) if byte else (lambda t: t.decode(encoding))
    output = [decode(l.strip(b'\r\n')) for l in iter(stdout.readline, b'')]
    if print_query:
        try:
            if multi:
                return output[0], output[1:]
            else:
                return output[0], output[1]
        except IndexError:
            return output[0], None
    else:
        if multi:
            return output
        else:
            try:
                return output[0]
            except IndexError:
                return None
