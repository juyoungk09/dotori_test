from flask_restx import Namespace, Resource, fields
from services.dotori_service import DotoriService

product_ns = Namespace("buy", description="상품 구매 API")

buy_request_model = product_ns.model(
    "BuyRequest",
    {
        "user_id": fields.Integer(required=True),
    },
)

buy_response_model = product_ns.model(
    "BuyResponse",
    {
        "isSuccess": fields.Boolean,
        "user_id": fields.Integer,
        "dotory": fields.Integer,
    },
)


@product_ns.route("/<int:productId>")
class BuyProduct(Resource):
    @product_ns.expect(buy_request_model)
    @product_ns.response(200, "Success", buy_response_model)
    @product_ns.response(400, "Failed")
    def post(self, productId):
        data = product_ns.payload
        user_id = data.get("user_id")
        if not user_id:
            product_ns.abort(400, "userId is required")

        product_price = 100  # 가격이 얼마에요?
        success = DotoriService.buy_product(user_id, product_price)
        if success:
            user_dotori = DotoriService.get_user_dotori(user_id)
            if user_dotori is None:
                product_ns.abort(400, "Failed to Buy Product")
            return {
                "isSuccess": True,
                "user_id": user_id,
                "dotory": user_dotori.to_response(),
            }
        else:
            product_ns.abort(400, "Insufficient dotory or purchase failed")
