#!/usr/bin/python3
"""
Copyright 2010 – 2024 Rocket Software, Inc. or its affiliates. 
This software may be used, modified, and distributed
(provided this notice is included without modification)
solely for internal demonstration purposes with other
Rocket® products, and is otherwise subject to the EULA at
https://www.rocketsoftware.com/company/trust/agreements.

THIS SOFTWARE IS PROVIDED "AS IS" AND ALL IMPLIED
WARRANTIES, INCLUDING THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE,
SHALL NOT APPLY.
TO THE EXTENT PERMITTED BY LAW, IN NO EVENT WILL
ROCKET SOFTWARE HAVE ANY LIABILITY WHATSOEVER IN CONNECTION
WITH THIS SOFTWARE.

Description:  A script to build application. 
"""

import os
import sys
import glob

from pathlib import Path
from utilities.input import read_json
from utilities.output import write_log 
from utilities.misc import parse_args 
from build.MFBuild import  run_ant_file
from utilities.misc import set_MF_environment, get_EclipsePluginsDir, get_CobdirAntDir

def resolve_os_type():
    return "Windows" if sys.platform.startswith('win32') else "Linux"

def find_ant_home(os_type, main_config):
    ant_home = None
    if 'ant_home' in main_config:
        ant_home = main_config['ant_home']
    elif "ANT_HOME" in os.environ:
        ant_home = os.environ["ANT_HOME"]
    else:
        eclipseinstalldir = get_EclipsePluginsDir(os_type)
        if eclipseinstalldir is not None:
            for file in os.listdir(eclipseinstalldir):
                if file.startswith("org.apache.ant_"):
                    ant_home = os.path.join(eclipseinstalldir, file)
        if ant_home is None:
            antdir = get_CobdirAntDir(os_type)
            if antdir is not None:
                for file in os.listdir(antdir):
                    if file.startswith("apache-ant-"):
                        ant_home = os.path.join(antdir, file)
    return ant_home

def resolve_bitism(main_config, os_type):
    if main_config['is64bit'] == False:
        if os_type == 'Linux':
            install_dir = set_MF_environment (os_type)
            if install_dir is None:
                write_log("Unable to determine COBDIR")
                return True
            path32 = Path(os.path.join(install_dir,'casstart32'))
            if path32.is_file() == False:
                write_log("Overriding bitism as platform only supports 64 bit")
                return True
            return False
    return True

def build_programs():
    cwd = os.getcwd()
    main_configfile = os.path.join(cwd, 'config', 'demo.json')
    main_config = read_json(main_configfile)
    region_name = main_config['region_name']
    os_type = resolve_os_type()
    ant_home = find_ant_home(os_type, main_config)
    if ant_home is None:
        write_log("Ant not found, set ANT_HOME")
        sys.exit(1)

    dataversion = 'vsam' if main_config['database'] == 'VSAM' else 'sql'

    build_file = os.path.join(cwd, 'build', 'build.xml')
    parentdir = str(Path(cwd).parents[0])
    source_dir = os.path.join(parentdir, 'sources')
    load_dir = os.path.join(parentdir, region_name,'system','loadlib')
    set64bit = resolve_bitism(main_config, os_type)

    run_ant_file(build_file,source_dir,load_dir,ant_home, dataversion, set64bit)

   
if __name__ == '__main__':
    build_programs()