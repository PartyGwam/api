import os
import glob
from split_settings.tools import include

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = os.environ['PG_SECRET_KEY']

ENV = os.environ.get('PROJECT_ENV', 'development')

COMPONENTS_DIR = os.path.join(
    BASE_DIR,
    'pg_rest_api',
    'settings',
    'components'
)
COMPONENTS = [
    'components/{}'.format(os.path.basename(component))
    for component in glob.glob(os.path.join(COMPONENTS_DIR, '*.py'))
]

ENVIRONMENTS = ['environments/{}.py'.format(ENV)]

SETTINGS = COMPONENTS + ENVIRONMENTS

include(*SETTINGS)
