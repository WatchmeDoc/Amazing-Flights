<div align="center">

# Flight Collection Workflow
### November 2023
### Author: [George Manos](mailto:george.manos01@outlook.com)

    

<a href="#">
    <img src="https://img.shields.io/badge/Python-3.8, 3.9, 3.10-306998">
</a>
<a href="#">
    <img src="https://img.shields.io/badge/Conda-4.12.0-44903d">
</a>
<br>
<a href="#">
    <img src="https://img.shields.io/badge/Poetry-1.2.2-5119d4">
</a>
<br>
<a href="https://developers.amadeus.com"><strong>Explore Amadeus API »</strong></a>
</div>

## Project Description
Data collection workflow for flight data using Amadeus API.


## Getting Started
The docker uses `conda` to create a virtual environment, and poetry 
for package management. Make sure you have them both installed on your machine.
### Running it locally
First, create a conda environment. The recommended python version is `3.10`.
```sh
$ conda create -n FW python=3.10 -y && conda activate FW
```
Then, install all required packages:
```shell
$ poetry install
```
Now you can run the `main.py` file.

