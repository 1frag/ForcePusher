from setuptools import setup

setup(
    name="force_push",
    version="0.1.0",
    py_modules=["force_push"],
    author="Aleksei Piskunov",
    author_email="piskunov.alesha@gmail.com",
    install_requires=["PyGithub"],
    package_dir={'': 'Sources/PythonForcePusher'},
    description="push with force",
    entry_points=dict(console_scripts=['force-push = force_push:main']),
)
