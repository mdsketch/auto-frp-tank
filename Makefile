all: deps

deps:
	pip install -r requirements.txt

build:
	python -m PyInstaller --onefile --windowed --icon=icon.ico --name=app ui.py