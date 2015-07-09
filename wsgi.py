import os
import site
import sys

app_root = os.path.dirname(os.path.realpath(__file__))
venv_path = os.path.join(app_root, 'venv')

venv_site_packages = os.path.join(venv_path, 'lib',
                                  'python%s' % sys.version[:3], 'site-packages')
site.addsitedir(venv_site_packages)

old_os_path = os.environ['PATH']
os.environ['PATH'] = (os.path.dirname(os.path.abspath(__file__))
                      + os.pathsep + old_os_path)

prev_sys_path = list(sys.path)

sys.real_prefix = sys.prefix
sys.prefix = venv_path
# Move the added items to the front of the path:
new_sys_path = []
for item in list(sys.path):
    if item not in prev_sys_path:
        new_sys_path.append(item)
        sys.path.remove(item)
sys.path[:0] = new_sys_path

sys.path.insert(0, app_root)

from ibolc.app import create_app
from ibolc.settings import ProdConfig

application = create_app(ProdConfig)
