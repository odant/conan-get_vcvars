from conans import ConanFile


class FindWindowsSigntool(ConanFile):
    name = "get_vcvars"
    version = "1.0"
    license = "MIT"
    url = "https://github.com/odant/conan-get_vcvars"
    description = "Python module for find Visual Studio environment"
    settings = {"os": ["Windows"]}
    exports = "__init__.py", "get_vcvars.py", "vswhere.exe"
    build_policy = "missing"
    
    def package(self):
        self.copy("*.py")
        self.copy("*.exe")
        
    def package_info(self):
        self.env_info.PYTHONPATH.append(self.package_folder)
        self.env_info.PATH.append(self.package_folder)
