from app import create_app
from config import ProdConfig
from config import DevConfig

if __name__ == "__main__":
# print(__name__)
    app = create_app(DevConfig)
    app.run()
else:
    app = create_app(ProdConfig)
    app.run()