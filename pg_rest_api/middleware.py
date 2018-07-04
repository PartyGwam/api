import logging
import re
import sys
from rest_framework.status import is_client_error, is_success


class ResponseFormattingMiddleware:
    """
    Rest Framework 을 위한 전용 커스텀 미들웨어에 대해 response format 을 자동으로 세팅
    """
    METHOD = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')

    def __init__(self, get_response):
        self.get_response = get_response
        self.API_URLS = [
            re.compile(r'^(.*)/api'),
            re.compile(r'^api'),
        ]

    def __call__(self, request):
        response = None
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

    def process_response(self, request, response):
        """
        API_URLS 와 method 가 확인이 되면
        response 로 들어온 data 형식에 맞추어
        response_format 에 넣어준 후 response 반환
        """
        path = request.path_info.lstrip('/')
        valid_urls = (url.match(path) for url in self.API_URLS)

        if request.method in self.METHOD and any(valid_urls):
            response_format = {
                'success': is_success(response.status_code),
                'result': {},
                'message': None
            }

            if hasattr(response, 'data') and \
                    getattr(response, 'data') is not None:
                data = response.data
                try:
                    response_format['message'] = data.pop('message')
                except (KeyError, TypeError):
                    response_format.update({
                        'result': data
                    })
                finally:
                    if is_client_error(response.status_code):
                        response_format['result'] = None
                        response_format['message'] = data
                    else:
                        response_format['result'] = data

                    response.data = response_format
                    response.content = response.render().rendered_content
            else:
                response.data = response_format

        return response


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
        path = request.path_info.lstrip('/')
        valid_urls = (url.match(path) for url in self.API_URLS)

        if request.method in self.METHOD and any(valid_urls):
            self._log_request_response_info(request)
            self._log_request_header(request)
            if hasattr(request, 'body'):
                self.logger.info('BODY: \n{}'.format(request.body.decode('utf-8')))

    def process_response(self, request, response):
        path = request.path_info.lstrip('/')
        valid_urls = (url.match(path) for url in self.API_URLS)

        if request.method in self.METHOD and any(valid_urls):
            self._log_request_response_info(request, response)
            if hasattr(response, 'content'):
                self.logger.info(response.content.decode('utf-8'))

    def _log_request_response_info(self, request, response=None):
        info = '{} {}'.format(request.method, request.path_info)
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
