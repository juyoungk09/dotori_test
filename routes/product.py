from flask_restx import Namespace, Resource, fields
from services.dotori_service import DotoriService

product_ns = Namespace('buy', description='상품 구매 API')

buy_request_model = product_ns.model('BuyRequest', {
    'userId': fields.Integer(required=True),
})

buy_response_model = product_ns.model('BuyResponse', {
    'isSuccess': fields.Boolean,
    'userId': fields.Integer,
    'dotory': fields.Integer,
})

@product_ns.route('/<int:productId>')
class BuyProduct(Resource):
    @product_ns.expect(buy_request_model)
    @product_ns.response(200, 'Success', buy_response_model)
    @product_ns.response(400, 'Failed')
    def post(self, productId):
        data = product_ns.payload
        user_id = data.get('userId')
        if not user_id:
            product_ns.abort(400, 'userId is required')
        
        product_price = 100 # 가격이 얼마에요?
        success = DotoriService.buy_product(user_id, product_price)
        if success:
            user_dotori = DotoriService.get_user_dotori(user_id)
            return {
                'isSuccess': True,
                'userId': user_id,
                'dotory': user_dotori if user_dotori else 0
            }
        else:
            product_ns.abort(400, 'Insufficient dotory or purchase failed')