import logging, hashlib, random
import re, sys, os
import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.http import urlquote

def home(request):
    return render(request, 'home.html')

def faq(request):
    return render(request, 'faq.html')

def timeline(request):
    return render(request, 'timeline.html')

def team(request):
    return render(request, 'team.html')

def prototype(request):
    return render(request, 'prototype.html')

def code(request):
    return render(request, 'code.html')