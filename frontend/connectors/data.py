import json
import jinja2
from .templates import TEMPLATE

# create template for the report


def saveSettings(filename, settings):
    with open(filename, 'w') as f:
        json.dump(settings, f, indent=4)


def loadSettings(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def exportResults(filename, results):
    # import template from file
    with open(filename, 'w') as f:
        f.write(jinja2.Template(TEMPLATE).render(**results))
