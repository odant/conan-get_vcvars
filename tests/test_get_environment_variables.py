import unittest
from unittest.mock import patch


import get_vcvars
import subprocess
from conans.errors import ConanException


set_output = r'''
**********************************************************************
** Visual Studio 2017 Developer Command Prompt v15.5.5
** Copyright (c) 2017 Microsoft Corporation
**********************************************************************
[vcvarsall.bat] Environment initialized for: 'x64'
__BEGINS__

INCLUDE=C:\Program Files (x86)\Windows Kits\10\include\10.0.16299.0\ucrt;
LIB=C:\Program Files (x86)\Windows Kits\10\lib\10.0.16299.0\ucrt\x64;
LIBPATH=C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.12.25827\lib\x64;
Path=C:\Program Files (x86)\Microsoft Visual Studio\2017\Community\VC\Tools\MSVC\14.12.25827\bin\HostX64\x64;C:\Program Files (x86)\Windows Kits\10\bin\10.0.16299.0\x64;

'''

class Test_get_environment_variables(unittest.TestCase):

    @patch("subprocess.check_output")
    def test_normal(self, mock_subprocess_check_output):
        mock_subprocess_check_output.return_value = set_output.encode()
        vcvarsall = "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Auxiliary\\Build\\vcvarsall.bat"
        args = ["amd64", "-vcvars_ver=14.0"]
        
        result = get_vcvars.get_environment_variables(vcvarsall, args)
        
        self.assertEqual(result, {
            "INCLUDE": "C:\\Program Files (x86)\\Windows Kits\\10\\include\\10.0.16299.0\\ucrt;",
            "LIB": "C:\\Program Files (x86)\\Windows Kits\\10\\lib\\10.0.16299.0\\ucrt\\x64;",
            "LIBPATH": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Tools\MSVC\\14.12.25827\\lib\\x64;",
            "PATH": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Tools\\MSVC\\14.12.25827\\bin\\HostX64\\x64;C:\\Program Files (x86)\\Windows Kits\\10\\bin\\10.0.16299.0\\x64;"
        })
        cmd = "call \"" + vcvarsall + "\" amd64 -vcvars_ver=14.0 && echo __BEGINS__ && set"
        mock_subprocess_check_output.assert_called_once_with(cmd, shell=True)

    def test_expeption(self):
        vcvarsall = "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Auxiliary\\Build\\vcvarsall.ba_"
        args = ["amd64", "-vcvars_ver=14.0"]
        with self.assertRaises(ConanException):
            get_vcvars.get_environment_variables(vcvarsall, args)


if __name__ == "__main__":
    unittest.main()
