from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

import opentracing
import six

tracing = settings.OPENTRACING_TRACING

# Create your views here.

def client_index(request):
    return HttpResponse("HOLA MUNDO APP1")

@tracing.trace()
def client_simple(request):
    print(1)
    url = "http://localhost:8001/app"
    new_request = six.moves.urllib.request.Request(url)
    inject_as_headers(tracing, tracing.tracer.active_span, new_request)
    print(2)
    try:
        print(3)
        response = six.moves.urllib.request.urlopen(new_request)
        print(4)
        return HttpResponse(response)
    except six.moves.urllib.error.URLError as e:
        return HttpResponse("Error: " + str(e))

@tracing.trace()
def client_log(request):
    url = "http://localhost:8000/server/log"
    new_request = six.moves.urllib.request.Request(url)
    inject_as_headers(tracing, tracing.tracer.active_span, new_request)
    try:
        response = six.moves.urllib.request.urlopen(new_request)
        return HttpResponse("Sent a request to log")
    except six.moves.urllib.error.URLError as e:
        return HttpResponse("Error: " + str(e))

@tracing.trace()
def client_child_span(request):
    url = "http://localhost:8000/server/childspan"
    new_request = six.moves.urllib.request.Request(url)
    inject_as_headers(tracing, tracing.tracer.active_span, new_request)
    try:
        response = six.moves.urllib.request.urlopen(new_request)
        return HttpResponse("Sent a request that should produce an additional child span")
    except six.moves.urllib.error.URLError as e:
        return HttpResponse("Error: " + str(e))

def inject_as_headers(tracing, span, request):
    print(tracing)
    print(tracing.tracer)
    print(span)
    text_carrier = {}
    tracing.tracer.inject(span.context, opentracing.Format.TEXT_MAP, text_carrier)
    for k, v in six.iteritems(text_carrier):
        request.add_header(k,v)

