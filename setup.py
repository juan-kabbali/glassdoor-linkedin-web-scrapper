# from setuptools import setup, find_packages
# from src.kohaSync import koha_sync_version
#

version = '1.0'

# with open("README.md", "r") as readme:
#     long_description = readme.read()
#
# setup(
#     name='koha-sync',
#     version=koha_sync_version,
#     license='MIT',
#     author='Juan Pablo Aguirre',
#     author_email='jaguirre@referencistas.com',
#     description='This projects allows to synchronize remote Koha rows to an endpoint',
#     long_description=long_description,
#     long_description_content_type='text/markdown',
#     url='https://jaguirre_referencistas@bitbucket.org/jaguirre_referencistas/koha_synchronizer.git',
#     packages=find_packages(),
#     entry_points={
#       "console_scripts": ['koha-sync = src.kohaSync:main']
#     },
#     python_requires='>=2.7',
#     install_requires=[
#         'click',
#         'tqdm',
#         'jsonschema',
#         'requests',
#         'pymysql',
#         'loguru',
#         'diskcache',
#         'setuptools',
#         'wheel',
#         'pyyaml'
#     ]
# )


# execute build
#   > pip install --user --upgrade twine
#   > python3 setup.py sdist bdist_wheel
#       - tar.gz = source archive
#       - whl    = built distribution

# upload package
#   > pip install --user --upgrade twine
#   > twine upload --repository pypi dist/*

# install
#   > install python3.7 and pip3
#   > install setuptools wheel
#   > alias python="python3.7"
#   > apt-get install python3-pip
#   > pip3 install virtualenv
#   > virtualenv venv
#   > source venv/bin/activate | deactivate
#   > pip3 install --index-url https://pypi.org/ --no-deps koha-sync

