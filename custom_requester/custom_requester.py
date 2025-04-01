import json
import logging
import os
from constants.const import BASE_HEADERS, RED, GREEN, RESET, BLUE
from pydantic import BaseModel

class CustomRequester:

    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        self.session.headers = BASE_HEADERS.copy()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def send_requests(self, method, endpoint, expected_status = 200, **kwargs):
        url = f"{self.base_url}{endpoint}"
        if 'data' in kwargs:
            if isinstance(kwargs['data'], BaseModel):
                kwargs['json'] = json.loads(kwargs.pop('data').model_dump_json(exclude_unset=True))
            elif isinstance(kwargs['data'], dict):
                kwargs['json'] = kwargs.pop('data')
        response = self.session.request(method, url, **kwargs)
        self.log_request_response(response) 
        if response.status_code not in (expected_status if type(expected_status) == list else [expected_status]):
            raise ValueError(f"Unexpected status code: {response.status_code}. Expected: {expected_status}")
        return response

    def _update_session_headers(self, **kwargs):
        self.session.headers.update(kwargs)

    def log_request_response(self, response):
        try:
            request = response.request
            headers = "\n".join([f"-header: {header}: {value}" for header, value in request.headers.items()])
            if getattr(request, 'params', None):
                params = "\n".join([f"-param: {param}: {value}" for param, value in request.params.items()])
            else:
                params = f"-param: {None}"
            response_data = response.text
            try:
                response_data = json.dumps(json.loads(response.text), indent=4, ensure_ascii=False)
            except json.JSONDecodeError:
                pass
            body = ""
            if hasattr(request, 'body') and request.body is not None:
                if isinstance(request.body, bytes):
                    body = request.body.decode('utf-8')
                elif isinstance(request.body, str):
                    body = request.body
                body = f"-d '{body}' \n" if body != '{}' else ''

            self.logger.info(f"{BLUE}pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}{RESET}\n")
            self.logger.info(
                f"\n{'=' * 10} REQUEST{'=' * 10}\n"
                f"-url: {request.url} \n"
                f"-method: {request.method} \n"
                f"{headers} \n"
                f"{params} \n"
                f"{body}"
            )
            COLOR = GREEN if response.ok else RED
            self.logger.info(
                    f"\n{'=' * 10} RESPONSE{'=' * 10}\n"
                    f"status code: {COLOR}{response.status_code}{RESET}\n"
                    f"data: {COLOR}{response_data}{RESET}\n"
            )
            self.logger.info(f"{BLUE}{'=' * 80}{RESET}\n")
        except Exception as e:
            self.logger.error(f"\nLoging failed: {type(e)} - {e}")