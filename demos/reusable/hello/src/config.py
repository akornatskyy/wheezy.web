import os.path

from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import FileLoader

from wheezy.web.templates import WheezyTemplate

engine = Engine(
    loader=FileLoader(
        (os.path.join(os.path.dirname(__file__), "hello/templates"),)
    ),
    extensions=(CoreExtension(),),
)

options = {"render_template": WheezyTemplate(engine)}
