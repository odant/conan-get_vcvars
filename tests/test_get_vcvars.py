import unittest
from unittest.mock import patch


import get_vcvars
from conans.model.settings import Settings


class Test_get_vcvars(unittest.TestCase):

    @patch("get_vcvars.get_environment_variables")
    @patch("get_vcvars.select_vcvarsall")
    @patch("get_vcvars.find_installation_paths")
    def test_normal(self, mock_find_installation_paths, mock_select_vcvarsall, mock_get_environment_variables):
        mock_find_installation_paths.return_value = [
            {
                "installationVersion": "15.5.27130.2026",
                "productId": "Microsoft.VisualStudio.Product.Community",
                "installationPath": "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community"
            },
            {
                "installationVersion": "15.5.27130.2020",
                "productId": "Microsoft.VisualStudio.Product.BuildTools",
                "installationPath": "C:/Program Files (x86)/Microsoft Visual Studio/2017/BuildTools"
            },
            {
                "installationVersion": "14.0",
                "productId": "VisualStudio.14.0",
                "installationPath": "C:/Program Files (x86)/Microsoft Visual Studio 14.0/"
            }
        ]
        mock_select_vcvarsall.return_value = [
            "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/VC/Auxiliary/Build/vcvarsall.bat",
            ["amd64"]
        ]
        mock_get_environment_variables.return_value = {
            "INCLUDE": "C:/include",
            "PATH": "C:/bin"
        }
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

        result = get_vcvars.get_vcvars(settings)
        
        self.assertEqual(result, {
            "INCLUDE": "C:/include",
            "PATH": "C:/bin"
        })

        mock_find_installation_paths.assert_called_once_with()
        mock_select_vcvarsall.assert_called_once_with(settings, [
            {
                "installationVersion": "15.5.27130.2026",
                "productId": "Microsoft.VisualStudio.Product.Community",
                "installationPath": "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community"
            },
            {
                "installationVersion": "15.5.27130.2020",
                "productId": "Microsoft.VisualStudio.Product.BuildTools",
                "installationPath": "C:/Program Files (x86)/Microsoft Visual Studio/2017/BuildTools"
            },
            {
                "installationVersion": "14.0",
                "productId": "VisualStudio.14.0",
                "installationPath": "C:/Program Files (x86)/Microsoft Visual Studio 14.0/"
            }
        ])
        mock_get_environment_variables.assert_called_once_with(
            "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/VC/Auxiliary/Build/vcvarsall.bat",
            ["amd64"]
        )


if __name__ == "__main__":
    unittest.main()

