import unittest
from unittest.mock import patch


import get_vcvars
from conans.model.settings import Settings
from conans.errors import ConanException


class Test_select_vcvarsall(unittest.TestCase):

    def test_normal_vs15_x86_64(self):
        installation_paths = [
            {
                "installationVersion": "15.5.27130.2026",
                "productId": "Microsoft.VisualStudio.Product.Community",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community",
                "vcvarsall": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Auxiliary\\Build\\vcvarsall.bat"
            },
            {
                "installationVersion": "15.5.27130.2020",
                "productId": "Microsoft.VisualStudio.Product.BuildTools",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\BuildTools",
                "vcvarsall": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\BuildTools\\VC\\Auxiliary\\Build\\vcvarsall.bat"
            },
            {
                "installationVersion": "14.0",
                "productId": "VisualStudio.14.0",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0",
                "vcvarsall": "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\vcvarsall.bat"
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

    def test_normal_vs15_x86(self):
        installation_paths = [
            {
                "installationVersion": "15.5.27130.2026",
                "productId": "Microsoft.VisualStudio.Product.Community",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community",
                "vcvarsall": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Auxiliary\\Build\\vcvarsall.bat"
            },
            {
                "installationVersion": "15.5.27130.2020",
                "productId": "Microsoft.VisualStudio.Product.BuildTools",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\BuildTools",
                "vcvarsall": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\BuildTools\\VC\\Auxiliary\\Build\\vcvarsall.bat"
            },
            {
                "installationVersion": "14.0",
                "productId": "VisualStudio.14.0",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0",
                "vcvarsall": "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\vcvarsall.bat"
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

    def test_vcvars_from_vs15_as_vs_14_x86_64(self):
        installation_paths = [
            {
                "installationVersion": "15.5.27130.2026",
                "productId": "Microsoft.VisualStudio.Product.Community",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community",
                "vcvarsall": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Auxiliary\\Build\\vcvarsall.bat"
            },
            {
                "installationVersion": "15.5.27130.2020",
                "productId": "Microsoft.VisualStudio.Product.BuildTools",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\BuildTools",
                "vcvarsall": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\BuildTools\\VC\\Auxiliary\\Build\\vcvarsall.bat"
            },
            {
                "installationVersion": "14.0",
                "productId": "VisualStudio.14.0",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0",
                "vcvarsall": "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\vcvarsall.bat"
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

    def test_vs15_not_found(self):
        installation_paths = [
            {
                "installationVersion": "14.0",
                "productId": "VisualStudio.14.0",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0",
                "vcvarsall": "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\vcvarsall.bat"
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

    def test_use_vs14_if_vs15_not_found(self):
        installation_paths = [
            {
                "installationVersion": "14.0",
                "productId": "VisualStudio.14.0",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0",
                "vcvarsall": "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\vcvarsall.bat"
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

        self.assertEqual(vcvarsall, "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\vcvarsall.bat")
        self.assertEqual(args, ["amd64"])

    def test_vs14_not_found(self):
        installation_paths = []
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

        with self.assertRaises(ConanException):
            get_vcvars.select_vcvarsall(settings, installation_paths)


if __name__ == "__main__":
    unittest.main()


