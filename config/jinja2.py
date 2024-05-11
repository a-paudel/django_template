from jinja2 import Environment
from django.urls import reverse as _django_reverse
from django.templatetags.static import static


def custom_reverse(name: str, **kwargs):
    return _django_reverse(name, kwargs=kwargs)


def environment(**options):
    env = Environment(**options)

    env.globals.update(
        {
            "url": _django_reverse,
            "static": static,
        }
    )

    return env
