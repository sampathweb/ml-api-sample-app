from tornado.web import RequestHandler
from tornado import concurrent
from tornado import gen
from concurrent.futures import ThreadPoolExecutor

from app.base_handler import BaseAPIHandler
from app.settings import MAX_THREAD_POOL

class LiveHandler(RequestHandler):
    """Check if the APP is live"""

    def get(self):
        self.write("App is Live!")

    def head(self):
        self.finish()


class IrisPredictionHandler(BaseAPIHandler):

    _thread_pool = ThreadPoolExecutor(max_workers=MAX_THREAD_POOL)

    def initialize(self, model):
        self.model = model

    @concurrent.run_on_executor(executor='_thread_pool')
    def _blocking_predict(self, X):
        target_values = self.model.predict(X)
        target_names = ['setosa', 'versicolor', 'virginica']
        results = [target_names[pred] for pred in target_values]
        return results


    @gen.coroutine
    def predict(self, data):
        if type(data) == dict:
            data = [data]

        X = []
        for item in data:
            record  = (item.get("sepal_length"), item.get("sepal_width"), \
                    item.get("petal_length"), item.get("petal_width"))
            X.append(record)

        results = yield self._blocking_predict(X)
        self.respond(results)
