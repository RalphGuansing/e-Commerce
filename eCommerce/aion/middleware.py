from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth
from django.shortcuts import HttpResponse, render, redirect
from django.utils.deprecation import MiddlewareMixin


class AutoLogout(MiddlewareMixin):

    def process_request(self, request):
        print(request.user.is_authenticated)
        if not request.user.is_authenticated:
          #Can't log out if not logged in
            return

        try:
            print('hello')
            if datetime.now() - request.session['last_touch'] > timedelta( 0, 1 * 60, 0):
                auth.logout(request)
                del request.session['last_touch']
                return HttpResponseRedirect('/')
        except KeyError as e:
            print(e)

        request.session['last_touch'] = datetime.now()