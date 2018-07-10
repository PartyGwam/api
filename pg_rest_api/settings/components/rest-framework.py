REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'pg_rest_api.authentication.PartyGwamAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'pg_rest_api.pagination.StandardPagination'
}

SWAGGER_SETTINGS = {
    'DOC_EXPANSION': 'list',
    'JSON_EDITOR': True,
    'SHOW_REQUEST_HEADERS': True,
}
