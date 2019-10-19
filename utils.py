import json
import warnings

import requests
from django.conf import settings as django_settings
from django.contrib.auth import (
    BACKEND_SESSION_KEY,
    REDIRECT_FIELD_NAME,
    SESSION_KEY,
    load_backend,
)
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import resolve_url
from django.utils.six.moves import urllib_parse
from vanila_djangocore_cas.models import SessionTicket, VanilaCasUser


def validateService(ticket,service):
    user_info = requests.get("{}serviceValidation?ticket={}&service={}".format(django_settings.CAS_SERVER_URL,ticket,service))
    if user_info.status_code == 200:
        info = json.loads(user_info.text)
        return (None, None, None) if "authenticationFailure" in info["serviceResponse"] else (info["serviceResponse"]["authenticationSuccess"]["id"],
                info["serviceResponse"]["authenticationSuccess"]["username"],
                info["serviceResponse"]["authenticationSuccess"]["group"],)

def createSessionTicket(request,ticket):
    sessionTicket = SessionTicket(ticket=ticket,session_key=request.session.session_key)
    sessionTicket.save()

def createVanila_cas_model(request,user,id,group):
    mcu = VanilaCasUser(cas_user_id = id,user=user,group=group,
                     session_key =request.session.session_key)
    mcu.save()

def get_protocol(request):
    """Returns 'http' or 'https' for the request protocol"""
    if request.is_secure():
        return 'https'
    return 'http'

def get_logout_url():
    return "{}logout".format(django_settings.CAS_SERVER_URL)

def get_redirect_url(request):
    """Redirects to referring page, or CAS_REDIRECT_URL if no referrer is
    set.
    """
    next_ = request.GET.get(REDIRECT_FIELD_NAME)
    if not next_:
        redirect_url = resolve_url(django_settings.CAS_REDIRECT_URL)
        if django_settings.CAS_IGNORE_REFERER:
            next_ = redirect_url
        else:
            next_ = request.META.get('HTTP_REFERER', redirect_url)
        prefix = urllib_parse.urlunparse(
            (get_protocol(request), request.get_host(), '', '', '', ''),
        )
        if next_.startswith(prefix):
            next_ = next_[len(prefix):]
    return next_


def get_service_url(request, redirect_to=None):
    """Generates application django service URL for CAS"""
    if hasattr(django_settings, 'CAS_ROOT_PROXIED_AS'):
        service = django_settings.CAS_ROOT_PROXIED_AS + request.path
    else:
        protocol = get_protocol(request)
        host = request.get_host()
        service = urllib_parse.urlunparse(
            (protocol, host, request.path, '', '', ''),
        )
    if not django_settings.CAS_STORE_NEXT:
        if '?' in service:
            service += '&'
        else:
            service += '?'
        service += urllib_parse.urlencode({
            REDIRECT_FIELD_NAME: redirect_to or get_redirect_url(request)
        })
    return service

def get_user_from_session(session):
    try:
        user_id = session[SESSION_KEY]
        backend_path = session[BACKEND_SESSION_KEY]
        backend = load_backend(backend_path)
        return backend.get_user(user_id) or AnonymousUser()
    except KeyError:
        return AnonymousUser()