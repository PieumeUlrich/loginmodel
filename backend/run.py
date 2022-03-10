from app import create_app
from config import ProdConfig
from config import DevConfig

if __name__ == "__main__":
    app = create_app(DevConfig)
    app.run()
else:
    app = create_app(ProdConfig)
    app.run(debug=True)