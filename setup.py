from setuptools import setup, find_packages

setup(
    name='pymogilefs',
    version='0.1',
    description='pymogilefs',
    long_description='Python MogileFS Client',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
    author='bwind',
    author_email='mailtobwind@gmail.com',
    license='GPL',
    packages=find_packages(exclude=['tests']),
    install_requires=['nose==1.3.7'],
    test_suite='tests',
    include_package_data=True,
    zip_safe=False
)
