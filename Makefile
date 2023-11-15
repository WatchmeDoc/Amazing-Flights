
install:
	conda create -n FW python=3.10 -y && conda activate FW
	poetry install

format:
	@isort .
	@black .