from django.http import HttpRequest
from jinja2 import Environment
from django.urls import reverse as _django_reverse
from django.templatetags.static import static
from django_vite.templatetags.django_vite import vite_hmr_client, vite_asset, vite_asset_url
from django.conf import settings
from django.core.paginator import Paginator, Page
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from urllib.parse import urlencode


def custom_reverse(name: str, **kwargs):
    return _django_reverse(name, kwargs=kwargs)


def pagination_links(
    request: HttpRequest,
    paginator: Paginator,
    page_obj: Page,
    with_query_params=False,
    on_each_side=3,
    on_ends=2,
    show_summary=True,
    object_name="results",
):
    html = render_to_string(
        "components/pagination.html",
        {
            "request": request,
            "paginator": paginator,
            "page": page_obj,
            "on_each_side": on_each_side,
            "on_ends": on_ends,
            "with_query_params": with_query_params,
            "show_summary": show_summary,
            "object_name": object_name,
        },
    )
    return mark_safe(html)


def get_page_link(request: HttpRequest, page_number: int, with_query_params=False):
    current_url = request.path
    params: dict[str, str | list[str]] = {}
    if with_query_params:
        params.update(request.GET.dict())
    params["page"] = str(page_number)
    current_url += "?" + urlencode(params)
    return current_url


def environment(**options):
    env = Environment(**options)

    env.globals.update(
        {
            "url": custom_reverse,
            "static": static,
            "config": settings,
            # vite
            "vite_hmr_client": vite_hmr_client,
            "vite_asset": vite_asset,
            "vite_asset_url": vite_asset_url,
            # pagination
            "pagination_links": pagination_links,
            "get_page_link": get_page_link,
        }
    )

    return env
