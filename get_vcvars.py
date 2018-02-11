import subprocess
import json
import os


from conans.util.files import decode_text
from conans.errors import ConanException


def find_installation_paths():
    vswhere_output = None
    try:
        vswhere_output = subprocess.check_output(["vswhere.exe", "-products", "*", "-legacy", "-format", "json"])
    except OSError:
        raise ConanException("Can`t run vswhere.exe!")
    vswhere_text = decode_text(vswhere_output).strip()
    vswhere_text = vswhere_text.replace(r"\\", "/")
    vswhere_json = json.loads(vswhere_text)
    result = []
    for item in vswhere_json:
        productId = item.get("productId")
        if productId is None:
            productId = item.get("instanceId")
        installationVersion = item.get("installationVersion")
        installationPath = item.get("installationPath")
        installationPath = os.path.normpath(installationPath)
        result.append({
            "productId": productId,
            "installationVersion": installationVersion,
            "installationPath": installationPath
        })
    result.sort(key=lambda v: v["installationVersion"], reverse=True)
    return result

def select_vcvarsall(settings, installation_paths):
    arch = {
        "x86": "x86",
        "x86_64": "amd64"
    }.get(str(settings.arch))
    args = [arch]
    for item in installation_paths:
        vcvarsall = os.path.join(item["installationPath"], "VC/Auxiliary/Build/vcvarsall.bat")
        if not os.path.isfile(vcvarsall):
            continue
        if item["installationVersion"].startswith("15") and settings.compiler.version == 14:
            args.append("-vcvars_ver=14.0")
        return vcvarsall, args

def get_environment_variables(vcvarsall, args):
    return {}
    
def get_vcvars(settings):
    installation_paths = find_installation_paths()
    vcvarsall, args = select_vcvarsall(settings, installation_paths)
    return get_environment_variables(vcvarsall, args)
