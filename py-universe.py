#!/usr/bin/pypy
# encoding=utf8
# File name: py-universe.py
# This file is part of: pyuni
#
# LICENSE
#
# The contents of this file are subject to the Mozilla Public License
# Version 1.1 (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS"
# basis, WITHOUT WARRANTY OF ANY KIND, either express or implied. See
# the License for the specific language governing rights and limitations
# under the License.
#
# Alternatively, the contents of this file may be used under the terms
# of the GNU General Public license (the  "GPL License"), in which case
# the provisions of GPL License are applicable instead of those above.
#
# FEEDBACK & QUESTIONS
#
# For feedback and questions about pyuni please e-mail one of the
# authors named in the AUTHORS file.
########################################################################
"""
Nothing yet.
"""

from __future__ import unicode_literals, print_function, division
from our_future import *

# global PyOpenGL flags MUST ONLY be set here.
# import OpenGL
# OpenGL.ERROR_ON_COPY = True

import numpypy
import argparse

def main(args):
    from Client.PythonicUniverse import PythonicUniverse
    app = PythonicUniverse()
    if args.profile:
        app.TimeLimit = args.timeLimit or 60.0
        print("Will run {0} seconds under cProfile".format(app.TimeLimit))
        import cProfile
        cProfile.runctx("app.run()", globals(), {"app": app}, args.profile)
    else:
        app.run()

if __name__ == '__main__':
    import sys
    sys.setcheckinterval(1000)
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--profile", "-p",
        metavar="FILENAME",
        help="Run the application under control of the cProfile and store the results in FILENAME.",
        dest="profile",
        default=None)
    argparser.add_argument("--time-limit", "-t",
        metavar="SECONDS",
        help="Limits the time the application will run to SECONDS. Has only effect if profiling is enabled.",
        type=float,
        dest="timeLimit",
        default=None)

    args = argparser.parse_args()
    main(args)
    
