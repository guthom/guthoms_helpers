import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='guthoms_helpers',
     version='0.1',
     scripts=[] ,
     author="Thomas Gulde",
     author_email="thomas.gulde@reutlingen-university.de",
     description="Common python helper tools for different projects",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/guthom/guthoms_helpers",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
     ],
 )
