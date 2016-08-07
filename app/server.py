import os
import logging
import logging.config

import tornado.ioloop
import tornado.web
from tornado.options import options

from sklearn.externals import joblib

from app.settings import LOG_SETTINGS, MODEL_DIR
from app import handler


MODELS = {}


def load_model(pickle_filename):
    return joblib.load(pickle_filename)


def main():

    # Get the Port and Debug mode from command line options or default in settings.py
    options.parse_command_line()

    # logging.config.dictConfig(LOG_SETTINGS)
    logger = logging.getLogger("app")

    # Load ML Models
    logger.info("Loading IRIS Prediction Model...")
    MODELS["iris"] = load_model(os.path.join(MODEL_DIR, "iris", "model.pkl"))

    urls = [
        (r"/live$", handler.LiveHandler),
        (r"/api/iris/(?P<action>[a-zA-Z]+)?",
            handler.IrisPredictionHandler, { "model": MODELS["iris"]}),
    ]

    application = tornado.web.Application(
        urls,
        debug=options.debug,
        autoreload=options.debug)

    logger.info("Starting App on Port: {} with Debug Mode: {}".format(options.port, options.debug))
    application.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


