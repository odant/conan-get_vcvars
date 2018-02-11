import unittest
from unittest.mock import patch
import os

import get_vcvars
from conans.model.settings import Settings
from conans.errors import ConanException


class Test_select_vcvarsall(unittest.TestCase):

    @patch("os.path.isfile")
    def test_normal_vs15_x86_64(self, mock_os_path_isfile):
        mock_os_path_isfile.return_value = True
        installation_paths = [
            {
                "productId": "Microsoft.VisualStudio.Product.Community",
                "installationVersion": "15.5.27130.2026",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community"
            },
            {
                "productId": "Microsoft.VisualStudio.Product.BuildTools",
                "installationVersion": "15.5.27130.2020",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\BuildTools"
            },
            {
                "productId": "VisualStudio.14.0",
                "installationVersion": "14.0",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0"
            }
        ]
        settings = Settings(definition={
            "arch": ["x86", "x86_64"],
            "compiler": {
                "Visual Studio": {
                    "version": [14, 15]
                }
            }
        })
        settings.arch = "x86_64"
        settings.compiler = "Visual Studio"
        settings.compiler.version = "15"

        vcvarsall, args = get_vcvars.select_vcvarsall(settings, installation_paths)

        self.assertEqual(vcvarsall, "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Auxiliary\\Build\\vcvarsall.bat")
        self.assertEqual(args, ["amd64"])

    @patch("os.path.isfile")
    def test_use_next_installation(self, mock_os_path_isfile):
        mock_os_path_isfile.side_effect = [False, True]
        installation_paths = [
            {
                "productId": "Microsoft.VisualStudio.Product.Community",
                "installationVersion": "15.5.27130.2026",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community"
            },
            {
                "productId": "Microsoft.VisualStudio.Product.BuildTools",
                "installationVersion": "15.5.27130.2020",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\BuildTools"
            },
            {
                "productId": "VisualStudio.14.0",
                "installationVersion": "14.0",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0"
            }
        ]
        settings = Settings(definition={
            "arch": ["x86", "x86_64"],
            "compiler": {
                "Visual Studio": {
                    "version": [14, 15]
                }
            }
        })
        settings.arch = "x86_64"
        settings.compiler = "Visual Studio"
        settings.compiler.version = "15"

        vcvarsall, _ = get_vcvars.select_vcvarsall(settings, installation_paths)

        self.assertEqual(vcvarsall, "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\BuildTools\\VC\\Auxiliary\\Build\\vcvarsall.bat")
        calls = [
            unittest.mock.call("C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Auxiliary\\Build\\vcvarsall.bat"),
            unittest.mock.call("C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\BuildTools\\VC\\Auxiliary\\Build\\vcvarsall.bat")
        ]
        mock_os_path_isfile.assert_has_calls(calls)

    @patch("os.path.isfile")
    def test_normal_vs15_x86(self, mock_os_path_isfile):
        mock_os_path_isfile.return_value = True
        installation_paths = [
            {
                "productId": "Microsoft.VisualStudio.Product.Community",
                "installationVersion": "15.5.27130.2026",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community"
            },
            {
                "productId": "Microsoft.VisualStudio.Product.BuildTools",
                "installationVersion": "15.5.27130.2020",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\BuildTools"
            },
            {
                "productId": "VisualStudio.14.0",
                "installationVersion": "14.0",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0"
            }
        ]
        settings = Settings(definition={
            "arch": ["x86", "x86_64"],
            "compiler": {
                "Visual Studio": {
                    "version": [14, 15]
                }
            }
        })
        settings.arch = "x86"
        settings.compiler = "Visual Studio"
        settings.compiler.version = "15"

        vcvarsall, args = get_vcvars.select_vcvarsall(settings, installation_paths)

        self.assertEqual(vcvarsall, "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Auxiliary\\Build\\vcvarsall.bat")
        self.assertEqual(args, ["x86"])

    @patch("os.path.isfile")
    def test_vcvars_from_vs15_as_vs_14_x86_64(self, mock_os_path_isfile):
        mock_os_path_isfile.return_value = True
        installation_paths = [
            {
                "productId": "Microsoft.VisualStudio.Product.Community",
                "installationVersion": "15.5.27130.2026",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community"
            },
            {
                "productId": "Microsoft.VisualStudio.Product.BuildTools",
                "installationVersion": "15.5.27130.2020",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\BuildTools"
            },
            {
                "productId": "VisualStudio.14.0",
                "installationVersion": "14.0",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0"
            }
        ]
        settings = Settings(definition={
            "arch": ["x86", "x86_64"],
            "compiler": {
                "Visual Studio": {
                    "version": [14, 15]
                }
            }
        })
        settings.arch = "x86_64"
        settings.compiler = "Visual Studio"
        settings.compiler.version = "14"

        vcvarsall, args = get_vcvars.select_vcvarsall(settings, installation_paths)

        self.assertEqual(vcvarsall, "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Auxiliary\\Build\\vcvarsall.bat")
        self.assertEqual(args, ["amd64", "-vcvars_ver=14.0"])

    @patch("os.path.isfile")
    def test_vs15_not_found(self, mock_os_path_isfile):
        mock_os_path_isfile.return_value = False
        installation_paths = [
            {
                "productId": "Microsoft.VisualStudio.Product.Community",
                "installationVersion": "15.5.27130.2026",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community"
            },
            {
                "productId": "Microsoft.VisualStudio.Product.BuildTools",
                "installationVersion": "15.5.27130.2020",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\BuildTools"
            },
            {
                "productId": "VisualStudio.14.0",
                "installationVersion": "14.0",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0"
            }
        ]
        settings = Settings(definition={
            "arch": ["x86", "x86_64"],
            "compiler": {
                "Visual Studio": {
                    "version": [14, 15]
                }
            }
        })
        settings.arch = "x86_64"
        settings.compiler = "Visual Studio"
        settings.compiler.version = "15"

        with self.assertRaises(ConanException):
            get_vcvars.select_vcvarsall(settings, installation_paths)
        calls = [
            unittest.mock.call("C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Auxiliary\\Build\\vcvarsall.bat"),
            unittest.mock.call("C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\BuildTools\\VC\\Auxiliary\\Build\\vcvarsall.bat")
        ]
        mock_os_path_isfile.assert_has_calls(calls)
        self.assertEqual(mock_os_path_isfile.call_count, 2)


if __name__ == "__main__":
    unittest.main()


