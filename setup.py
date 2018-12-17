from setuptools import setup, find_packages
setup(
    name="jcdssync",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'jcdssync=jcdssync.cli:main'
        ]
    },
    install_requires=[
        'typing>=3.6.6',
        'python_jss>=2.0.1',
    ],
    dependency_links=[
        'git+https://github.com/jssimporter/python-jss.git#egg=python_jss-2.0.1'
    ],
    author="mosen",
    author_email="mosen@noreply.users.github.com",
    description="JCDSSync is a command line utility for syncing content to, and from, "
                "a JAMF Pro JCDS Distribution Point",
    license="MIT",
    url="https://github.com/mosen/jcdssync",
    zip_safe=False,
)

