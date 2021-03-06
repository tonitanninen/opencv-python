from setuptools import setup
from setuptools.dist import Distribution
import pip
import os
import sys
import io

# cv_version.py should be generated by running find_version.py
from cv_version import opencv_version

contrib_build = False
package_name = "opencv-python"
numpy_version = ""
long_description = ""
package_data = {}

contrib = os.getenv('ENABLE_CONTRIB', None)

if contrib is not None:
    if int(contrib) == 1:
        contrib_build = True
else:
    try:
        print("Trying to read contrib enable flag from file...")
        with open("contrib.enabled") as f:
            flag = int(f.read(1))
            if flag == 1:
                contrib_build = True
    except:
        pass

# Use different README and package name for contrib build.
if contrib_build:
    package_name = "opencv-contrib-python"
    with io.open('README_CONTRIB.rst', encoding="utf-8") as f:
        long_description = f.read()
else:
    with io.open('README.rst', encoding="utf-8") as f:
        long_description = f.read()

# Get required numpy version
for package in pip.get_installed_distributions():
    if package.key == "numpy":
        numpy_version = package.version

if os.name == 'posix':
    package_data['cv2'] = ['*.so']
else:
    package_data['cv2'] = ['*.pyd', '*.dll']

package_data['cv2'] += ["LICENSE.txt", "LICENSE-3RD-PARTY.txt"]

"""

This is my old hack to force binary distribution.

However, it doesn't work properly because the binaries
are placed into purelib instead of platlib.

class BinaryDistribution(Distribution):
    def has_ext_modules(self):
        return True

    def is_pure(self):
        return False
"""

# This creates a list which is empty but returns a length of 1.
# Should make the wheel a binary distribution and platlib compliant.


class EmptyListWithLength(list):
    def __len__(self):
        return 1


setup(name=package_name,
      version=opencv_version,
      url='https://github.com/skvark/opencv-python',
      license='MIT',
      description='Wrapper package for OpenCV python bindings.',
      long_description=long_description,
      packages=['cv2'],
      package_data=package_data,
      maintainer="Olli-Pekka Heinisuo",
      include_package_data=True,
      ext_modules=EmptyListWithLength(),
      install_requires="numpy>=%s" % numpy_version,
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: C++',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Software Development',
        ]
      )
