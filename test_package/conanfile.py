from conans import ConanFile, tools


class TestPackage(ConanFile):
    settings = {"os": ["Windows"], "arch": ["x86", "x86_64"]}

    def build(self):
        with tools.pythonpath(self):
            import get_vcvars
            self.output.info("--------Visual Studio enviroment--------")
            self.output.info("arch: %s compiler.version: %s" % (self.setting.arch, self.settings.compiler.version))
            env_vcvars = get_vcvars.get_vcvars(self.settings)
            for key, value in env_vcvars.items():
                self.output.info("%s :" % key)
                for split_value in value.split(";"):
                    self.output.info(split_value)

    def test(self):
        pass

