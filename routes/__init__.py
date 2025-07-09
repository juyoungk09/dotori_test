from flask_restx import Api

from .dotori import dotori_ns
from .product import product_ns


def add_namespaces(api):
    api.add_namespace(dotori_ns, path="/api/dotory")
    api.add_namespace(product_ns, path="/api/buy")
