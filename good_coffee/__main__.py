import uvicorn

from .lib.settings import AppSettings
from .lib.setup_app import setup_app


def main():
    settings = AppSettings()
    app = setup_app(settings)
    uvicorn.run(app=app, host=settings.host, port=settings.port, debug=settings.debug, http="httptools")


if __name__ == "__main__":
    main()
