import unittest
from unittest.mock import patch


import get_vcvars
import os


class Test_select_vcvarsall(unittest.TestCase):

    @patch("os.path.isfile")
    def test_normal(self, mock_os_path_isfile):
        mock_os_path_isfile.return_value = True
        
        result = get_vcvars.find_vcvarsall([
            {
                "installationVersion": "15.5.27130.2026",
                "productId": "Microsoft.VisualStudio.Product.Community",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community"
            },
            {
                "installationVersion": "15.5.27130.2020",
                "productId": "Microsoft.VisualStudio.Product.BuildTools",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\BuildTools"
            },
            {
                "installationVersion": "14.0",
                "productId": "VisualStudio.14.0",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0"
            }
        ])

        self.assertEqual(result, [
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
        ])
        self.assertEqual(mock_os_path_isfile.call_count, 3)
        calls = [
            unittest.mock.call("C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Auxiliary\\Build\\vcvarsall.bat"),
            unittest.mock.call("C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\BuildTools\\VC\\Auxiliary\\Build\\vcvarsall.bat"),
            unittest.mock.call("C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\vcvarsall.bat")
        ]
        mock_os_path_isfile.assert_has_calls(calls)

    @patch("os.path.isfile")
    def test_skip_miss_vs15(self, mock_os_path_isfile):
        mock_os_path_isfile.side_effect = [True, False, True]
        
        result = get_vcvars.find_vcvarsall([
            {
                "installationVersion": "15.5.27130.2026",
                "productId": "Microsoft.VisualStudio.Product.Community",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community"
            },
            {
                "installationVersion": "15.5.27130.2020",
                "productId": "Microsoft.VisualStudio.Product.BuildTools",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\BuildTools"
            },
            {
                "installationVersion": "14.0",
                "productId": "VisualStudio.14.0",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0"
            }
        ])

        self.assertEqual(result, [
            {
                "installationVersion": "15.5.27130.2026",
                "productId": "Microsoft.VisualStudio.Product.Community",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community",
                "vcvarsall": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Auxiliary\\Build\\vcvarsall.bat"
            },
            {
                "installationVersion": "14.0",
                "productId": "VisualStudio.14.0",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0",
                "vcvarsall": "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\vcvarsall.bat"
            }
        ])
        self.assertEqual(mock_os_path_isfile.call_count, 3)
        calls = [
            unittest.mock.call("C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Auxiliary\\Build\\vcvarsall.bat"),
            unittest.mock.call("C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\BuildTools\\VC\\Auxiliary\\Build\\vcvarsall.bat"),
            unittest.mock.call("C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\vcvarsall.bat")
        ]
        mock_os_path_isfile.assert_has_calls(calls)

    @patch("os.path.isfile")
    def test_skip_miss_vs14(self, mock_os_path_isfile):
        mock_os_path_isfile.side_effect = [True, True, False]
        
        result = get_vcvars.find_vcvarsall([
            {
                "installationVersion": "15.5.27130.2026",
                "productId": "Microsoft.VisualStudio.Product.Community",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community"
            },
            {
                "installationVersion": "15.5.27130.2020",
                "productId": "Microsoft.VisualStudio.Product.BuildTools",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\BuildTools"
            },
            {
                "installationVersion": "14.0",
                "productId": "VisualStudio.14.0",
                "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0"
            }
        ])

        self.assertEqual(result, [
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
            }
        ])
        self.assertEqual(mock_os_path_isfile.call_count, 3)
        calls = [
            unittest.mock.call("C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Auxiliary\\Build\\vcvarsall.bat"),
            unittest.mock.call("C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\BuildTools\\VC\\Auxiliary\\Build\\vcvarsall.bat"),
            unittest.mock.call("C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\VC\\vcvarsall.bat")
        ]
        mock_os_path_isfile.assert_has_calls(calls)


if __name__ == "__main__":
    unittest.main()
