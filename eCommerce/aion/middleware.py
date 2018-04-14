from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth
from django.shortcuts import HttpResponse, render, redirect
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache, caches
from importlib import import_module
from .models import *
from django.contrib.sessions.models import Session


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


class OneSessionPerUserMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if isinstance(request.user, User):
            current_key = request.session.session_key
            if hasattr(request.user, 'visitor'):
                active_key = request.user.visitor.session_key
                print(active_key, current_key)
                if active_key != current_key:
                    Session.objects.filter(session_key=active_key).delete()
                    request.user.visitor.session_key = current_key
                    request.user.visitor.save()
            else:
                Visitor.objects.create(
                    pupil=request.user,
                    session_key=current_key,
                )