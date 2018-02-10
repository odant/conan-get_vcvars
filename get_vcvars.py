import subprocess
import json
import os


from conans.util.files import decode_text


def find_installation_paths():
    vswhere_output = subprocess.check_output(["vswhere.exe", "-products", "*", "-legacy", "-format", "json"])
    vswhere_text = decode_text(vswhere_output).strip()
    vswhere_json = json.loads(vswhere_text)
    result = []
    for item in vswhere_json:
        productId = item.get("productId")
        if productId is None:
            productId = item.get("instanceId")
        installationVersion = item.get("installationVersion")
        installationPath = item.get("installationPath")
        installationPath = os.path.dirname(installationPath)
        result.append({
            "productId": productId,
            "installationVersion": installationVersion,
            "installationPath": installationPath
        })
    result.sort(key=lambda v: v["installationVersion"], reverse=True)
    return result

def select_vcvarsall(installation_paths):
    return "", []

def get_environment_variables(vcvarsall, args):
    return {}
    
def get_vcvars(settings):
    installation_paths = find_installation_paths()
    vcvarsall, args = select_vcvarsall(settings, installation_paths)
    return get_environment_variables(vcvarsall, args)
