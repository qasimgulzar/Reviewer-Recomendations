from setuptools import setup

setup(
    name='github-reviewer-recommendations',
    version='0.0.0',
    packages=['reviewer_recommendations'],
    install_requires=[
        'PyGithub==1.54.1',
        'gitpython==3.1.13'
    ],
    url='https://github.com/qasimgulzar/github-reviewer-recommendations',
    license='GNU GPLv2',
    author='qasimgulzar',
    author_email='qasim.khokhar52@gmail.com',
    description='',
)
