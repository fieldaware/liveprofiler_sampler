from setuptools import setup, find_packages

setup(
    name='liveprofiler_sampler',
    author='Piotr Szymanski',
    author_email='piotr.szymanski@fieldaware.com',
    url='https://github.com/fieldaware/liveprofiler_sampler',
    license='MIT',
    version='0.9.0',
    description='Module for sampling profiling output from the main process',
    long_description=open('README.md').read(),
    packages=find_packages(),
    include_package_data=True,
)
