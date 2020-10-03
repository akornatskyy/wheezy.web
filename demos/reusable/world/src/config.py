from shared import resolve_searchpath
from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import FileLoader

from wheezy.web.templates import WheezyTemplate

searchpath = ("content/templates", resolve_searchpath("hello"))

engine = Engine(loader=FileLoader(searchpath), extensions=(CoreExtension(),))

options = {"render_template": WheezyTemplate(engine)}
