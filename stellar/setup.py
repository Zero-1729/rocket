from setuptools import setup

setup(name="stellar",
    version='0.8.0',
    description="Rocket lang 'stellar' utilities",
    author="Zero-1729",
    author_email="zero1729@protonmail.com",
    py_modules=["tokens", "expr", "stmt", "env", "reporter", "rocketClass"],
    package_dir={"": "utils"},
    license="MIT")
