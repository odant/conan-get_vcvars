from conans import ConanFile, tools


class TestPackage(ConanFile):
    settings = {"os": ["Windows"], "arch": ["x86", "x86_64"]}

    def test(self):
        with tools.pythonpath(self):
            import get_vcvars
            self.output.info("--------Variable for SDK--------")
            env_vcvars = get_vcvars.get_vcvars(self.settings)
            for key, value in env_vcvars.items():
                self.output.info("%s :" % key)
                for split_value in value.split(";")
                    self.output.info(split_value)

