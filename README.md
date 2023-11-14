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
<a href="https://github.com/amadeus4dev/amadeus-python"><strong>Explore Amadeus API »</strong></a>
</div>

## Project Description
Data collection workflow for flight data using Amadeus API.


## Getting Started
The docker uses `conda` to create a virtual environment, `poetry`
for package management, as well as `make` and `Makefile`.
Make sure you have them installed on your machine.

### Installation
To set up a conda environment and install all required packages, run:
```shell
$ make install
```
The script will create a conda environment named `FW` and install all required packages.
Now you can run the `main.py` file!

### Configuration
To execute the project properly, you need to first configure the `api_config.json` file in `workflow/configs/` folder.
You need to generate a key and secret for the Amadeus API and provide them in that config (see [here](https://developers.amadeus.com/get-started/get-started-with-self-service-apis-335)).

Then, when executing the `main.py` script you need to provide the path to the desired query config file in json format
(default is `workflow/flight_queries/example.json`).

The query config file follow this schema:

```json
{
  "cities": {
      "description": "A list of Airport codes we want to find flights.",
      "value_type": "array",
        "elements": {
          "type" : "string",
          "pattern" : "^[A-Z]{3}$"
      },
      "minItems": 2,
      "uniqueItems": true
  },
  "date": {
      "description": "Year, month and day to look for flights.",
      "value_type": "object",
      "elements": {
        "year" : "int",
        "month" : "int",
        "day" : "int"
      },
      "required": ["year"]
  },
  "params": {
      "description": "Other params to add in the API query.",
      "elements": {
        "adults" : "int",
        ...
      },
      "required": ["adults"]
  }
}
```



## Development
The project uses `black` and `isort` code formatters for styling purposes. Prior to pushing, use
```shell
$ make format
```
to reformat all python files into black style.



