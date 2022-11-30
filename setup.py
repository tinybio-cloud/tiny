from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

dependencies = [
    "google-cloud-storage==2.6.0",
    "google-cloud-workflows==1.7.4",
]

setup(
    name='tiny',
    version='0.1',
    description='TinyBio genome analysis tool',
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
