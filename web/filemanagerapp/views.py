#!/usr/bin/env python
# views.py
#
# Copyright (C) 2008-2018 Veselin Penev, https://bitdust.io
#
# This file (views.py) is part of BitDust Software.
#
# BitDust is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BitDust Software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with BitDust Software.  If not, see <http://www.gnu.org/licenses/>.
#
# Please contact us if you have any questions at bitdust.io@gmail.com

#------------------------------------------------------------------------------

import json
import traceback
import pprint

from django.views import generic
from django.http import HttpResponse, HttpResponseBadRequest

#------------------------------------------------------------------------------

from logs import lg
from interface import api

#------------------------------------------------------------------------------


class FileManagerView(generic.TemplateView):
    template_name = 'filemanager.html'

#------------------------------------------------------------------------------


def filemanager_api_view(request):
    try:
        json_request = json.loads(request.body.decode('utf-8'))
    except:
        error_dict = {"result": {"success": False, "error": traceback.format_exc()}}
        json_context = json.dumps(
            error_dict).encode('utf-8')
        return HttpResponseBadRequest(
            json_context, content_type='application/json')
    # lg.out(4, 'filemanagerapp.filemanager_api_view request: %s' % json_request)
    mode = json_request['params']['mode']
    params = json_request['params']
    try:
        if mode == 'list':
            result = api.files_list(params['path'])
        if mode == 'listall':
            result = api.files_list('')
        elif mode == 'upload':
            filename = unicode(params['path'])
            import os
            local_path = os.path.abspath(os.path.join(os.path.expanduser('~'), filename))
            api.file_create(filename)
            result = api.file_upload_start(local_path, filename)
        else:
            result = api.filemanager(json_request)
    except:
        return HttpResponseBadRequest(
            json_context, content_type='application/json')
    return HttpResponse(json.dumps(result), content_type='application/json')


# class JSONResponseMixin(object):
#    """
#    A mixin that allows you to easily serialize simple data such as a dict or
#    Django models.
#    """
#    content_type = None
#    json_dumps_kwargs = None
#    json_encoder_class = DjangoJSONEncoder
#
#    def get_content_type(self):
#        if (self.content_type is not None and not isinstance(self.content_type, str)):
#            raise ImproperlyConfigured(
#                '{0} is missing a content type. Define {0}.content_type, '
#                'or override {0}.get_content_type().'.format(
#                    self.__class__.__name__))
#        return self.content_type or "application/json"
#
#    def get_json_dumps_kwargs(self):
#        if self.json_dumps_kwargs is None:
#            self.json_dumps_kwargs = {}
#        self.json_dumps_kwargs.setdefault('ensure_ascii', False)
#        return self.json_dumps_kwargs
#
#    def render_json_response(self, context_dict, status=200):
#        """
#        Limited serialization for shipping plain data. Do not use for models
#        or other complex or custom objects.
#        """
#        json_context = json.dumps(
#            context_dict,
#            cls=self.json_encoder_class,
#            **self.get_json_dumps_kwargs()).encode('utf-8')
#        return HttpResponse(json_context,
#                            content_type=self.get_content_type(),
#                            status=status)
#
#    def render_json_object_response(self, objects, **kwargs):
#        """
#        Serializes objects using Django's builtin JSON serializer. Additional
#        kwargs can be used the same way for django.core.serializers.serialize.
#        """
#        json_data = serializers.serialize("json", objects, **kwargs)
#        return HttpResponse(json_data, content_type=self.get_content_type())
#
#
# class AjaxResponseMixin(object):
#    """
#    Mixin allows you to define alternative methods for ajax requests. Similar
#    to the normal get, post, and put methods, you can use get_ajax, post_ajax,
#    and put_ajax.
#    """
#    def dispatch(self, request, *args, **kwargs):
#        request_method = request.method.lower()
#
#        if request.is_ajax() and request_method in self.http_method_names:
#            handler = getattr(self, "{0}_ajax".format(request_method),
#                              self.http_method_not_allowed)
#            self.request = request
#            self.args = args
#            self.kwargs = kwargs
#            return handler(request, *args, **kwargs)
#
#        return super(AjaxResponseMixin, self).dispatch(
#            request, *args, **kwargs)
#
#    def get_ajax(self, request, *args, **kwargs):
#        return self.get(request, *args, **kwargs)
#
#    def post_ajax(self, request, *args, **kwargs):
#        return self.post(request, *args, **kwargs)
#
#    def put_ajax(self, request, *args, **kwargs):
#        return self.get(request, *args, **kwargs)
#
#    def delete_ajax(self, request, *args, **kwargs):
#        return self.get(request, *args, **kwargs)
#
#
# class JsonRequestResponseMixin(JSONResponseMixin):
#    """
#    Extends JSONResponseMixin.  Attempts to parse request as JSON.  If request
#    is properly formatted, the json is saved to self.request_json as a Python
#    object.  request_json will be None for imparsible requests.
#    Set the attribute require_json to True to return a 400 "Bad Request" error
#    for requests that don't contain JSON.
#    Note: To allow public access to your view, you'll need to use the
#    csrf_exempt decorator or CsrfExemptMixin.
#    Example Usage:
#        class SomeView(CsrfExemptMixin, JsonRequestResponseMixin):
#            def post(self, request, *args, **kwargs):
#                do_stuff_with_contents_of_request_json()
#                return self.render_json_response(
#                    {'message': 'Thanks!'})
#    """
#    require_json = False
#    error_response_dict = {"errors": ["Improperly formatted request"]}
#
#    def render_bad_request_response(self, error_dict=None):
#        if error_dict is None:
#            error_dict = self.error_response_dict
#        json_context = json.dumps(
#            error_dict,
#            cls=self.json_encoder_class,
#            **self.get_json_dumps_kwargs()
#        ).encode('utf-8')
#        return HttpResponseBadRequest(
#            json_context, content_type=self.get_content_type())
#
#    def get_request_json(self):
#        try:
#            return json.loads(self.request.body.decode('utf-8'))
#        except ValueError:
#            return None
#
#    def dispatch(self, request, *args, **kwargs):
#        self.request = request
#        self.args = args
#        self.kwargs = kwargs
#
#        self.request_json = self.get_request_json()
#        if self.require_json and self.request_json is None:
#            return self.render_bad_request_response()
#        return super(JsonRequestResponseMixin, self).dispatch(
#            request, *args, **kwargs)
