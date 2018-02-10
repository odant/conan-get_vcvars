def find_installation_paths():
    return {}

def select_vcvarsall(installation_paths):
    return "", []

def get_environment_variables(vcvarsall, args):
    return {}
    
def get_vcvars(settings):
    installation_paths = find_installation_paths()
    vcvarsall, args = select_vcvarsall(settings, installation_paths)
    return get_environment_variables(vcvarsall, args)
