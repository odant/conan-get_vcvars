from conans import ConanFile, tools


class TestPackage(ConanFile):
    settings = {
        "os": ["Windows"],
        "arch": ["x86", "x86_64"],
        "compiler": ["Visual Studio"]
    }

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

    def test(self):
        pass

