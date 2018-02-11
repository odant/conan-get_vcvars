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

def find_vcvarsall(installation_paths):
    result = []
    for item in installation_paths:
        vcvarsall = None
        if item["installationVersion"].startswith("15"):
            vcvarsall = os.path.join(item["installationPath"], "VC\\Auxiliary\\Build\\vcvarsall.bat")
        else:
            vcvarsall = os.path.join(item["installationPath"], "VC\\vcvarsall.bat")
        if not os.path.isfile(vcvarsall):
            continue
        item["vcvarsall"] = vcvarsall
        result.append(item)
    return result
    
def select_vcvarsall(settings, installation_paths):
    arch = {
        "x86": "x86",
        "x86_64": "amd64"
    }.get(str(settings.arch))
    args = [arch]
    for item in installation_paths:
        if item["installationVersion"].startswith("15") and settings.compiler.version == 15:
            return item["vcvarsall"], args
        if item["installationVersion"].startswith("15") and settings.compiler.version == 14:
            args.append("-vcvars_ver=14.0")
            return item["vcvarsall"], args
        if item["installationVersion"].startswith("14") and settings.compiler.version == 14:
            return item["vcvarsall"], args
    else:
        raise ConanException("Can`t find vcvarsall.bat")

def get_environment_variables(vcvarsall, args):
    cmd = "call %s %s %s" % (vcvarsall, " ".join(args), "&& echo __BEGINS__ && set")
    set_output = subprocess.check_output(cmd, shell=True)
    set_text = decode_text(set_output)
    result = {}
    start_reached = False
    for line in set_text.splitlines():
        line.strip()
        if len(line) == 0:
            continue
        if not start_reached:
            if "__BEGINS__" in line:
                start_reached = True
            continue
        name_var, value = line.split("=", 1)
        result[name_var.upper()] = value
    return result
    
def get_vcvars(settings):
    installation_paths = find_installation_paths()
    installation_paths = find_vcvarsall(installation_paths)
    vcvarsall, args = select_vcvarsall(settings, installation_paths)
    return get_environment_variables(vcvarsall, args)
