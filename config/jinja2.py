from django.urls import reverse
from django.templatetags.static import static
from jinja2 import Environment


def _custom_reverse(name, **kwargs):
    return reverse(name, kwargs=kwargs)


def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            "url_for": _custom_reverse,
            "static": static,
        }
    )
    return env
