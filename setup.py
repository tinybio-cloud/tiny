from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


dependencies = [
    "httpcore[http2]",
    "httpx==0.23.1",
    "tabulate",
    "anytree",
    "humanize",
]

setup(
    name='tiny-cli',
    version='0.1.0',
    description='tinybio cli allows you to run your genomic tools in the cloud quickly and easily.',
    long_description_content_type='text/markdown',
    url='https://github.com/tinybio-cloud/tiny',
    long_description=readme(),
    author='TinyBio LLC',
    author_email='vishal@tinybio.cloud',
    license='MIT',
    packages=['tiny'],
    install_requires=dependencies,
    python_requires=">=3.7",
    zip_safe=False
)
