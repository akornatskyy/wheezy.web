""" ``views`` module.
"""

from datetime import timedelta

from config import cached, session
from models import Greeting
from repository import Repository
from validation import greeting_validator

from wheezy.http import CacheProfile
from wheezy.http.transforms import gzip_transform
from wheezy.web import handler_cache
from wheezy.web.handlers import BaseHandler
from wheezy.web.transforms import handler_transforms


class ListHandler(BaseHandler):
    @handler_cache(
        CacheProfile(
            "server",
            duration=timedelta(minutes=15),
            vary_environ=["HTTP_ACCEPT_ENCODING"],
        )
    )
    @handler_transforms(gzip_transform(compress_level=9, min_length=250))
    def get(self):
        with session() as db:
            repo = Repository(db)
            greetings = repo.list_greetings()
        response = self.render_response("list.html", greetings=greetings)
        response.cache_dependency = ("d_list",)
        # response.cache_dependency.append('d_list')
        return response


class AddHandler(BaseHandler):
    @handler_cache(
        CacheProfile(
            "both",
            duration=timedelta(hours=1),
            vary_environ=["HTTP_ACCEPT_ENCODING"],
            http_vary=["Accept-Encoding"],
        )
    )
    @handler_transforms(gzip_transform(compress_level=9, min_length=250))
    def get(self, greeting=None):
        greeting = greeting or Greeting()
        return self.render_response("add.html", greeting=greeting)

    def post(self):
        greeting = Greeting()
        if not self.try_update_model(greeting) or not self.validate(
            greeting, greeting_validator
        ):
            if self.request.ajax:
                return self.json_response({"errors": self.errors})
            return self.get(greeting)
        with session() as db:
            repo = Repository(db)
            if not repo.add_greeting(greeting):
                self.error("Sorry, can not add your greeting.")
                return self.get(greeting)
            db.commit()
        cached.dependency.delete("d_list")
        return self.see_other_for("list")
