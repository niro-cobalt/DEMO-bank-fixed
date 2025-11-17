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

Description:  Miscelaneous utility functions. 
"""

import os
import sys
import getopt
if sys.platform.startswith('win32'):
    import winreg
from utilities.output import write_log 
from utilities.exceptions import HTTPException
from pathlib import Path
import subprocess

def get_elem_with_prop(arr, key, value):
    """ Gets an array object with a specific property"""
    for elem in arr:
        if elem[key] == value:
            return elem


def create_headers(requested_with, ip_address):
    """ Creates headers for sending API requests to the server region. """

    headers = {
        'accept': 'application/json',
        'X-Requested-With': requested_with,
        'Content-Type': 'application/json',
        'Origin': 'http://{}:10086'.format(ip_address)
        #'Origin': 'http://{}:10086'.format('127.0.0.1')
    }

    return headers


def check_http_error(res):
    """ Error handling for HTTP status codes. """
    if res.status_code >= 400 and res.status_code < 500:
        raise HTTPException('A general Client Error occured.')
    if res.status_code >= 500 and res.status_code < 600:
        raise HTTPException('A general Server Error occured.')


def parse_args(arg_list, short_map, long_map):
    """ Parses arguments passed on the command line. """
    short_opts = "".join([key.lstrip('-') for key in short_map.keys()])
    long_opts = [key.lstrip('-') for key in long_map.keys()]
    try:
        opts, _ = getopt.getopt(arg_list, short_opts, long_opts)
    except getopt.GetoptError as error:
        print(error)
        return None
    short_map = {key.rstrip(':'): val for key, val in short_map.items()}
    long_map = {key.rstrip('='): val for key, val in long_map.items()}
    arg_map = {**short_map, **long_map}

    kwargs = {arg_map[opt[0]]: opt[1] for opt in opts}

    return kwargs

def set_mf_environment(os_type):

    if os_type == 'Windows':
        localmachinekey = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        cobolkey = winreg.OpenKey(localmachinekey, r"SOFTWARE\\Micro Focus\\Visual COBOL")
        defaultversion = winreg.QueryValueEx(cobolkey, "DefaultVersion")
        installkeystring =  r'{}\\COBOL\\Install'.format(defaultversion[0])
        write_log('Found COBOL version: {}'.format(defaultversion[0]))
        installkey = winreg.OpenKey(cobolkey, installkeystring)
        install_dir = winreg.QueryValueEx(installkey, "BIN")
        winreg.CloseKey(installkey)
        winreg.CloseKey(cobolkey)
        winreg.CloseKey(localmachinekey)
        return install_dir[0]
    else:
        if "COBDIR" in os.environ:
           return os.path.join(os.environ["COBDIR"], "bin")

        pathcobdir = Path("/opt/rocketsoftware/EnterpriseDeveloper/bin")
        if pathcobdir.is_dir():
            return str(pathcobdir)
        pathcobdir = Path("/opt/rocketsoftware/EnterpriseServer/bin")
        if pathcobdir.is_dir():
            return str(pathcobdir)
        pathcobdir = Path("/opt/microfocus/EnterpriseDeveloper/bin")
        if pathcobdir.is_dir():
            return str(pathcobdir)
        pathcobdir = Path("/opt/microfocus/EnterpriseServer/bin")
        if pathcobdir.is_dir():
            return str(pathcobdir)

    return None

def get_eclipse_plugins_dir(os_type):
    if os_type == 'Windows':
       localmachinekey = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
       cobolkey = winreg.OpenKey(localmachinekey, r"SOFTWARE\\Micro Focus\\Visual COBOL")
       defaultversion = winreg.QueryValueEx(cobolkey, "DefaultVersion")
       installkeystring =  r'{}'.format(defaultversion[0])
       installkey = winreg.OpenKey(cobolkey, installkeystring)
       try:
           install_dir = winreg.QueryValueEx(installkey, "ECLIPSEINSTALLDIR")
           pluginsdir = os.path.join(install_dir[0], "eclipse", "plugins")   
       except FileNotFoundError:
           pluginsdir = None
       winreg.CloseKey(installkey)
       winreg.CloseKey(cobolkey)
       winreg.CloseKey(localmachinekey)
       return pluginsdir
    else:
       installdir = set_mf_environment(os_type)
       if installdir is not None:
           cobdir = Path(installdir).parents[0]
           if cobdir is not None:
               pluginsdir = os.path.join(cobdir, "eclipse", "eclipse", "plugins")
               pathpluginsdir = Path(pluginsdir)
               if pathpluginsdir.is_dir():
                   return pluginsdir

    return None

def get_cobdir_ant_dir(os_type):
    if os_type == 'Windows':
       return None
    else:
       cobdir = set_mf_environment(os_type)
       if cobdir is not None:
           antdir = os.path.join(cobdir, "remotedev", "ant")
           pathantdir = Path(antdir)
           if pathantdir.is_dir():
               return antdir

    return None
    
def get_cobdir_bin(is64bit):
    if sys.platform.startswith('win32') and is64bit:
        bindir = 'bin64'
    else:
        bindir = 'bin'
    cobdir = os.path.join(os.environ['COBDIR'], bindir)
    return cobdir

def powershell(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed

def check_elevation():
    # Check if the current process is running as administator role
    isadmin = '$user = [Security.Principal.WindowsIdentity]::GetCurrent();if ((New-Object Security.Principal.WindowsPrincipal $user).IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)) {exit 1} else {exit 0}'
    completed = powershell(isadmin)
    return completed.returncode == 1

def check_esuid(esuid):
    myuid = subprocess.getoutput("whoami")
    return esuid==myuid

