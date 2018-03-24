from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth
from django.shortcuts import HttpResponse, render, redirect


def AutoLogout(get_response):

    def middleware(request):
        try:
            if not request.user.is_authenticated() :
              #Can't log out if not logged in
                return

            try:
                if datetime.now() - request.session['last_touch'] > timedelta( 0, 1 * 60, 0):
                    auth.logout(request)
                    del request.session['last_touch']
                    return HttpResponseRedirect('/')
            except KeyError:
                pass

            request.session['last_touch'] = datetime.now()
        except:
            return get_response(request)

    return middleware