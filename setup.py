from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

author = 'Leo Wotzak'
email = 'leojwotzak@gmail.com'

description = """
Quantitative trading and analysis library that provides essential tools for 
underwriting and executing algorithmic trading strategies
"""


setup(
    name='LJWE',
    version="BETA",
    author=author,
    author_email=email,
    maintainer=author,
    maintainer_email=email,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/leowotzak/LJWEquities',
    # ? download_url='https://github.com/leowotzak/LJWEquities/archive/refs/heads/master.zip',
    # ? packages=find_packages(include=['api']),
    project_urls={
        'Bug Tracker': 'https://github.com/leowotzak/LJWEquities/issues',
        'Wiki': 'https://github.com/leowotzak/LJWEquities/wiki'
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Office/Business :: Financial :: Investment'
    ],
    install_requires=[
        'python-dotenv',
        'numpy',
        'pandas',
        'sqlalchemy',
        'alembic',
        'alpha_vantage'
    ]
)