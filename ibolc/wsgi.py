from .app import create_app
from .settings import ProdConfig

application = create_app(ProdConfig)
