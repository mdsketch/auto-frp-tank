all: deps

deps:
	pip install -r requirements.txt

build:
	python -m PyInstaller --onefile --windowed --name=autofrptank ui.py