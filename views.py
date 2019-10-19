
from django.contrib.auth import authenticate,login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from vanila_djangocore_cas.models import SessionTicket, VanilaCasUser
from vanila_djangocore_cas.utils import get_service_url, get_redirect_url, get_protocol, get_logout_url


def login(request):
    ticket = request.GET.get('ticket')
    service = get_service_url(request)
    if ticket and service:
        user = authenticate(ticket=ticket,request=request,service=service)
        if user is not None:
            auth_login(request, user)
        else:
            auth_logout(request)
        if request.user.is_authenticated:
            return successful_login(request,settings.CAS_NEXT_DEFAULT)
    return redirect("{}login/?service={}".format(settings.CAS_SERVER_URL,get_service_url(request)))

def successful_login(request, next_page):
        """
        This method is called on successful login. Override this method for
        custom post-auth actions (i.e, to add a cookie with a token).
        :param request:
        :param next_page:
        :return:
        """
        return HttpResponseRedirect(next_page)

def logout(request):
    """
    Redirects to CAS logout page
    :param request:
    :return:
    """
    next_page = request.GET.get('next')

    # try to find the ticket matching current session for logout signal
    try:
        st = SessionTicket.objects.get(session_key=request.session.session_key)
        ticket = st.ticket
    except SessionTicket.DoesNotExist:
        ticket = None
    auth_logout(request)
    # clean current session CasUser and SessionTicket
    VanilaCasUser.objects.filter(session_key=request.session.session_key).delete()
    SessionTicket.objects.filter(session_key=request.session.session_key).delete()
    return HttpResponseRedirect(get_logout_url())
