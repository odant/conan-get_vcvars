import unittest
from unittest.mock import patch
import os
import platform


import get_vcvars
import subprocess
from conans.errors import ConanException

vswhere_output = r'''
[
  {
    "instanceId": "d8ae1ead",
    "installDate": "2018-01-10T14:23:04Z",
    "installationName": "VisualStudio/15.5.3+27130.2020",
    "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio/2017\\BuildTools",
    "installationVersion": "15.5.27130.2020",
    "productId": "Microsoft.VisualStudio.Product.BuildTools",
    "productPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\BuildTools\\Common7\\Tools\\LaunchDevCmd.bat",
    "isPrerelease": false,
    "displayName": "Visual Studio Build Tools 2017",
    "description": "Visual Studio Build Tools позволяет осуществлять сборку собственных и управляемых приложений на базе MSBuild без использования среды Visual Studio IDE. Существуют разные варианты установки компиляторов и библиотек Visual C++, ATL, MFC и поддержки C++/CLI.",
    "channelId": "VisualStudio.15.Release",
    "channelPath": "C:\\Users\\Admin\\AppData\\Local\\Microsoft\\VisualStudio\\Packages\\_Channels\\4CB340F5\\catalog.json",
    "channelUri": "https://aka.ms/vs/15/release/channel",
    "enginePath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\Installer\\resources\\app\\ServiceHub\\Services\\Microsoft.VisualStudio.Setup.Service",
    "releaseNotes": "https://go.microsoft.com/fwlink/?LinkId=660692#15.5.3",
    "thirdPartyNotices": "https://go.microsoft.com/fwlink/?LinkId=660708",
    "catalog": {
      "buildBranch": "d15svc",
      "buildVersion": "15.5.27130.2020",
      "id": "VisualStudio/15.5.3+27130.2020",
      "localBuild": "build-lab",
      "manifestName": "VisualStudio",
      "manifestType": "installer",
      "productDisplayVersion": "15.5.3",
      "productLine": "Dev15",
      "productLineVersion": "2017",
      "productMilestone": "RTW",
      "productMilestoneIsPreRelease": "False",
      "productName": "Visual Studio",
      "productPatchVersion": "3",
      "productPreReleaseMilestoneSuffix": "0.0",
      "productRelease": "RTW",
      "productSemanticVersion": "15.5.3+27130.2020"
    },
    "properties": {
      "campaignId": "1622459557.1502792825",
      "channelManifestId": "VisualStudio.15.Release/15.5.3+27130.2020",
      "nickname": "2",
      "setupEngineFilePath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\Installer\\vs_installershell.exe"
    }
  },
  {
    "instanceId": "5667fd94",
    "installDate": "2017-08-15T11:08:46Z",
    "installationName": "VisualStudio/15.5.5+27130.2026",
    "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community",
    "installationVersion": "15.5.27130.2026",
    "productId": "Microsoft.VisualStudio.Product.Community",
    "productPath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\Common7\\IDE\\devenv.exe",
    "isPrerelease": false,
    "displayName": "Visual Studio Community 2017",
    "description": "Бесплатная полнофункциональная интегрированная среда разработки для учащихся, разработчиков решений с открытым кодом и индивидуальных разработчиков",
    "channelId": "VisualStudio.15.Release",
    "channelPath": "C:\\Users\\Admin\\AppData\\Local\\Microsoft\\VisualStudio\\Packages\\_Channels\\4CB340F5\\catalog.json",
    "channelUri": "https://aka.ms/vs/15/release/channel",
    "enginePath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\Installer\\resources\\app\\ServiceHub\\Services\\Microsoft.VisualStudio.Setup.Service",
    "releaseNotes": "https://go.microsoft.com/fwlink/?LinkId=660692#15.5.3",
    "thirdPartyNotices": "https://go.microsoft.com/fwlink/?LinkId=660708",
    "catalog": {
      "buildBranch": "d15svc",
      "buildVersion": "15.5.27130.2026",
      "id": "VisualStudio/15.5.5+27130.2026",
      "localBuild": "build-lab",
      "manifestName": "VisualStudio",
      "manifestType": "installer",
      "productDisplayVersion": "15.5.5",
      "productLine": "Dev15",
      "productLineVersion": "2017",
      "productMilestone": "RTW",
      "productMilestoneIsPreRelease": "False",
      "productName": "Visual Studio",
      "productPatchVersion": "5",
      "productPreReleaseMilestoneSuffix": "0.0",
      "productRelease": "RTW",
      "productSemanticVersion": "15.5.5+27130.2026",
      "requiredEngineVersion": "1.14.192.55101"
    },
    "properties": {
      "campaignId": "1622459557.1502792825",
      "channelManifestId": "VisualStudio.15.Release/15.5.5+27130.2026",
      "defaultProgram": "VisualStudio.5667fd94",
      "nickname": "",
      "setupEngineFilePath": "C:\\Program Files (x86)\\Microsoft Visual Studio\\Installer\\vs_installershell.exe"
    }
  },
  {
    "instanceId": "VisualStudio.14.0",
    "installationPath": "C:\\Program Files (x86)\\Microsoft Visual Studio 14.0\\",
    "installationVersion": "14.0"
  }
]
'''


class Test_find_installation_paths(unittest.TestCase):

    @patch("subprocess.check_output")
    def test_normal(self, mock_check_output):
        mock_check_output.return_value = vswhere_output.encode()
        
        result = get_vcvars.find_installation_paths()
        self.assertEqual(result, [
            {
                "productId": "Microsoft.VisualStudio.Product.Community",
                "installationVersion": "15.5.27130.2026",
                "installationPath": "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community"
            },
            {
                "productId": "Microsoft.VisualStudio.Product.BuildTools",
                "installationVersion": "15.5.27130.2020",
                "installationPath": "C:/Program Files (x86)/Microsoft Visual Studio/2017/BuildTools"
            },
            {
                "productId": "VisualStudio.14.0",
                "installationVersion": "14.0",
                "installationPath": "C:/Program Files (x86)/Microsoft Visual Studio 14.0"
            }
        ])

        mock_check_output.assert_called_once_with(["vswhere.exe", "-products", "*", "-legacy", "-format", "json"])

    def test_run_on_non_windows(self):
        if platform.system == "Windows":
            return
        os.environ["PATH"] = os.getcwd() + ":" + os.environ["PATH"]
        with self.assertRaises(ConanException):
            get_vcvars.find_installation_paths()


if __name__ == "__main__":
    unittest.main()

