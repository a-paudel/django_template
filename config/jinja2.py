from django.urls import reverse
from django.templatetags.static import static
from jinja2 import Environment
from django.core.paginator import Paginator, Page
from django.http import HttpRequest
from django_vite.templatetags.django_vite import vite_hmr_client, vite_asset
from django.conf import settings


def _custom_reverse(name, **kwargs):
    return reverse(name, kwargs=kwargs)


def _get_page_links(request: HttpRequest, page: Page, paginator: Paginator):
    def _get_page_link(request: HttpRequest, page_number: int):
        params = request.GET.copy()
        params["page"] = str(page_number)
        link = request.path + "?" + params.urlencode()
        return link

    first_link = _get_page_link(request, 1)
    last_link = _get_page_link(request, paginator.num_pages)
    prev_link = _get_page_link(request, page.previous_page_number()) if page.has_previous() else None
    next_link = _get_page_link(request, page.next_page_number()) if page.has_next() else None
    return first_link, prev_link, next_link, last_link


def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            "vite_hmr_client": vite_hmr_client,
            "vite_asset": vite_asset,
            "url_for": _custom_reverse,
            "static": static,
            "get_page_links": _get_page_links,
            "debug": settings.DEBUG,
        }
    )
    return env
