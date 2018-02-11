import os
from conan.packager import ConanMultiPackager


# Common settings
username = "odant" if "CONAN_USERNAME" not in os.environ else None

    
if __name__ == "__main__":
    builder = ConanMultiPackager(username=username)
    builder.add(
        settings={"arch": "x86"},
        options={},
        env_vars={},
        build_requires={}
    )
    builder.add(
        settings={"arch": "x86_64"},
        options={},
        env_vars={},
        build_requires={}
    )
    builder.run()

