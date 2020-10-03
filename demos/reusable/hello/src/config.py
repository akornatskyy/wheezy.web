from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import FileLoader

from wheezy.web.templates import WheezyTemplate

engine = Engine(
    loader=FileLoader(("src/hello/templates",)), extensions=(CoreExtension(),)
)

options = {"render_template": WheezyTemplate(engine)}
