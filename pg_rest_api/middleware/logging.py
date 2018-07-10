import logging
import re
import sys

from django.urls import resolve
from urllib.parse import unquote


class LoggingMiddleware:
    METHOD = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')

    def __init__(self, get_response):
        self.get_response = get_response
        self.API_URLS = [
            re.compile(r'^(.*)/api'),
            re.compile(r'^api'),
        ]

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        self.handler = logging.StreamHandler(stream=sys.stdout)
        self.handler.setFormatter(self.formatter)
        self.handler.setLevel(logging.INFO)
        self.logger.addHandler(self.handler)

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        self.process_response(request, response)
        return response

    def process_request(self, request):
        if self._should_log(request):
            self._log_request_response_info(request)
            self._log_request_header(request)
            if hasattr(request, 'body') and getattr(request, 'body'):
                try:
                    self.logger.info('BODY: \n{}'.format(request.body.decode('utf-8')))
                except UnicodeDecodeError:
                    self.logger.info('BODY: \n{}'.format(request.body))

    def process_response(self, request, response):
        if self._should_log(request):
            self._log_request_response_info(request, response)
            if hasattr(response, 'content') and getattr(response, 'content'):
                if re.match('^application/json', response.get('Content-Type', ''), re.I):
                    self.logger.info(response.content.decode('utf-8'))

    def _should_log(self, request):
        path = request.path_info.lstrip('/')
        valid_urls = (url.match(path) for url in self.API_URLS)

        return request.method in self.METHOD and any(valid_urls)

    def _log_request_response_info(self, request, response=None):
        info = '{} {}'.format(request.method, unquote(request.get_full_path()))
        if response:
            info += ' - {}'.format(response.status_code)
        self.logger.info(info)

    def _log_request_header(self, request):
        headers = {
            'Content-Type': request.content_type
        }
        if 'HTTP_AUTHORIZATION' in request.META:
            headers['Authorization'] = request.META['HTTP_AUTHORIZATION']

        self.logger.info('HEADERS: {}'.format(headers))
