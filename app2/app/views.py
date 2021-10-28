from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

import opentracing
import six

import time

tracing = settings.OPENTRACING_TRACING

# Create your views here.

def app2_index(request):
    time.sleep(1)
    return HttpResponse("Hola Mundo APP2")

@tracing.trace()
def app2_simple(request):
    url = "http://localhost:8000/server/simple"
    new_request = six.moves.urllib.request.Request(url)
    inject_as_headers(tracing, tracing.tracer.active_span, new_request)
    try:
        response = six.moves.urllib.request.urlopen(new_request)
        return HttpResponse("Made a simple request")
    except six.moves.urllib.error.URLError as e:
        return HttpResponse("Error: " + str(e))

@tracing.trace()
def app2_log(request):
    url = "http://localhost:8000/server/log"
    new_request = six.moves.urllib.request.Request(url)
    inject_as_headers(tracing, tracing.tracer.active_span, new_request)
    try:
        response = six.moves.urllib.request.urlopen(new_request)
        return HttpResponse("Sent a request to log")
    except six.moves.urllib.error.URLError as e:
        return HttpResponse("Error: " + str(e))

@tracing.trace()
def app2_child_span(request):
    url = "http://localhost:8000/server/childspan"
    new_request = six.moves.urllib.request.Request(url)
    inject_as_headers(tracing, tracing.tracer.active_span, new_request)
    try:
        response = six.moves.urllib.request.urlopen(new_request)
        return HttpResponse("Sent a request that should produce an additional child span")
    except six.moves.urllib.error.URLError as e:
        return HttpResponse("Error: " + str(e))

def inject_as_headers(tracing, span, request):
    text_carrier = {}
    tracing.tracer.inject(span.context, opentracing.Format.TEXT_MAP, text_carrier)
    for k, v in six.iteritems(text_carrier):
        request.add_header(k,v)

