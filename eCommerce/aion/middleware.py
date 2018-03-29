from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth
from django.shortcuts import HttpResponse, render, redirect
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache, caches
from importlib import import_module
from .models import *


class AutoLogout(MiddlewareMixin):

    def process_request(self, request):
        if not request.user.is_authenticated:
          #Can't log out if not logged in
            return

        try:
            if datetime.now() - request.session['last_touch'] > timedelta( 0, 1 * 60, 0):
                auth.logout(request)
                del request.session['last_touch']
                return HttpResponseRedirect('/')
        except KeyError as e:
            print(e)

        request.session['last_touch'] = datetime.now()


class UserRestrict(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            try:
                cur_session_key = UserSession.objects.get(user=request.user).session.session_key
            except:
                cur_session_key = None
            if cur_session_key != request.session.session_key:
                # Default handling... kick the old session...
                try:
                    s = Session.objects.get(session_key=cur_session_key)
                    s.delete()
                    print('session deleted')
                except:
                    pass
            # if not cur_session_key or cur_session_key != request.session.session_key:
            #     p = request.user.get_profile()
            #     p.session_key = request.session.session_key
            #     p.save()