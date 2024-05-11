from jinja2 import Environment
from django.urls import reverse as _django_reverse
from django.templatetags.static import static
from django_vite.templatetags.django_vite import vite_hmr_client, vite_asset, vite_asset_url


def custom_reverse(name: str, **kwargs):
    return _django_reverse(name, kwargs=kwargs)


def environment(**options):
    env = Environment(**options)

    env.globals.update(
        {
            "url": _django_reverse,
            "static": static,
            "vite_hmr_client": vite_hmr_client,
            "vite_asset": vite_asset,
            "vite_asset_url": vite_asset_url,
        }
    )

    return env
