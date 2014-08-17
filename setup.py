from distutils.core import setup
from distutils.command.install import INSTALL_SCHEMES
from awis import __version__, __maintainer__, __email__


# Patch distutils to make sure LICENSE and README
# are in the same directory as the code
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']


license_text = open('LICENSE.txt').read()
long_description = open('README.rst').read()


setup(
    name = 'python-awis',
    version = __version__,
    url = 'http://github.com/muhuk/python-awis',
    author = __maintainer__,
    author_email = __email__,
    license = license_text,
    packages = ['awis'],
    data_files=[('awis', ['LICENSE.txt', 'README.rst'])],
    description = 'Python bindings for Alexa Web ' \
                  'Information Service (AWIS) API',
    long_description=long_description,
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
    ]
)
