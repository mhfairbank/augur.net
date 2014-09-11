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

import numpy
from numpy import ma
from consensus import Factory

owners = [
    {'name': 'Jack', 'coin': 8.5},
    {'name': 'Jill', 'coin': 11},
    {'name': 'Hansel', 'coin': 0.5},
    {'name': 'Gretel', 'coin': 2.5},
    {'name': 'Mary Mary', 'coin': 1},
    {'name': 'You', 'coin': 3}
]

def home(request):

    return render(request, 'home.html')


def voting(request):

    return render(request, 'voting.html', {'owners': owners})


def faq(request):

    return render(request, 'faq.html')


class NumpyEncoder(json.JSONEncoder):

    def default(self, obj):

        if isinstance(obj, numpy.ndarray):

            return obj.tolist();

        return json.JSONEncoder.default(self, obj)


@csrf_exempt
def vote(request):

    if request.method == 'POST':

        user_ballot = [
            float(request.POST.get('d1', 0.5)),
            float(request.POST.get('d2', 0.5)),
            float(request.POST.get('d3', 0.5)),
            float(request.POST.get('d4', 0.5)),
            float(request.POST.get('d5', 0.5))
        ]

        votes = ma.masked_array([
            ma.masked_array([0, 0, 0.5, 0, 0]),   # jack
            ma.masked_array([0, 0, 0.5, 0, 0]),   # jill
            ma.masked_array([0, 0, 0.5, 0, 0]),   # hansel
            ma.masked_array([0, 0, 0.5, 0, 0]),   # gretel
            ma.masked_array([0, 0, 0.5, 0, 0]),   # mary mary
            ma.masked_array(user_ballot),      # user
        ])


        results = Factory(votes) 
        response = {'raw': results}

        for i, reward in enumerate(results['Agents']['RowBonus'][0]):

            logging.info(reward)

            owners[i]['reward'] = owners[i]['coin'] * reward
            owners[i]['newCoin'] = owners[i]['reward'] + owners[i]['coin']

        response['owners'] = owners

        response = json.dumps(response, cls=NumpyEncoder)
        
    else:

        response = '{}'

    return HttpResponse(response, content_type='application/json')

