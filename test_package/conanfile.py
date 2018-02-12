from conans import ConanFile, tools


class TestPackage(ConanFile):
    settings = {
        "os": ["Windows"],
        "arch": ["x86", "x86_64"],
        "compiler": ["Visual Studio"]
    }
    _env_vcvars = {}

    def build(self):
        with tools.pythonpath(self):
            import get_vcvars
            self.output.info("--------Settings------------------------")
            self.output.info("arch: %s compiler.version: %s" % (self.settings.arch, self.settings.compiler.version))
            self.output.info("--------Visual Studio enviroment--------")
            env_vcvars = get_vcvars.get_vcvars(self.settings)
            for key, value in env_vcvars.items():
                self.output.info("Variable %s =>" % key)
                for split_value in value.split(";"):
                    self.output.info(split_value)
            self._env_vcvars = env_vcvars

    def test(self):
        with tools.environment_append(self._env_vcvars):
            self.output.info("Check run MS Resource Compiler (from Windows SDK)")
            self.run("rc /?")

