from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


dependencies = [
    "requests==2.28.1",
    "requests-toolbelt==0.10.1",
]

setup(
    name='tiny-cli',
    version='0.1',
    description='TinyBio genome analysis tool',
    long_description_content_type='text/markdown',
    url='https://github.com/tinybio-cloud/tiny',
    long_description=readme(),
    author='TinyBio LLC',
    author_email='tiny-packages@tinybio.cloud',
    license='MIT',
    packages=['tiny'],
    install_requires=dependencies,
    python_requires=">=3.10",
    zip_safe=False
)
