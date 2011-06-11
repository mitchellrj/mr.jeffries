from setuptools import setup, find_packages

setup(
    name = "mr.jeffries",
    version = "0.0.1",
    author = 'Richard Mitchell',
    author_email = 'mitch@awesomeco.de',
    description = '\n'.join([open('README.rst').read(),
                             open('DEVELOPERS.rst').read(),
                             open('HISTORY.rst').read(),
                             open('LICENSE.rst').read()]),
    packages = find_packages(),
    install_requires = ['zope.interface', 'simplejson'],
    extras_requires = {
        'Error Log Monitoring': ['Products.SiteErrorLog', 'collective.monkeypatcher']
    },
    zip_safe = False,
    include_package_data = True,
    package_data = {'': ['*.rst', 'buildout.cfg'],
                    'mr.jeffries.resource': ['*.*',]
                    },
)