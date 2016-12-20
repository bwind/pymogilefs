from setuptools import setup, find_packages

setup(
    name='pymogilefs',
    version='0.1.1',
    description='Python MogileFS Client',
    long_description='Python MogileFS Client',
    url='https://github.com/bwind/pymogilefs',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
    author='Bas Wind',
    author_email='mailtobwind@gmail.com',
    license='MIT',
    packages=['pymogilefs'],
    install_requires=['requests==2.12.3'],
)
