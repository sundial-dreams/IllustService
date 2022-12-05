from service.server import app

if __name__ == "__main__":
    app.run(port=3030, fast=True, dev=True)
