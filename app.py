from cakes_app import create_app
from config.config import DevelopmentConfig, ProductionConfig

app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    app.run()

if __name__ == 'cakes_app':
    app = create_app(ProductionConfig)
