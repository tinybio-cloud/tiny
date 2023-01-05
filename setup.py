from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


dependencies = [
    "httpx==0.23.1"
]

setup(
    name='tiny-cli',
    version='0.11',
    description='TinyBio genome analysis tool',
    long_description_content_type='text/markdown',
    url='https://github.com/tinybio-cloud/tiny',
    long_description=readme(),
    author='TinyBio LLC',
    author_email='tiny-packages@tinybio.cloud',
    license='MIT',
    packages=['tiny'],
    install_requires=dependencies,
    python_requires=">=3.7",
    zip_safe=False
)
