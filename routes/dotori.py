from flask_restx import Namespace, Resource, fields
from services.dotori_service import DotoriService

dotori_ns = Namespace('dotory', description='도토리 관련 API')

user_model = dotori_ns.model('UserDotori', {
    'user_id': fields.Integer,
    'dotory': fields.Integer,
})

@dotori_ns.route('/<int:userId>')
class UserDotori(Resource):
    @dotori_ns.marshal_with(user_model)
    def get(self, userId):
        user_dotori = DotoriService.get_user_dotori(userId)
        if not user_dotori:
            dotori_ns.abort(404, 'User not found')
        return user_dotori.to_response()

    @dotori_ns.expect(dotori_ns.model('AddDotori', {'num': fields.Integer(required=True)}))
    def put(self, userId):
        data = dotori_ns.payload
        num = data.get('num')
        return DotoriService.add_dotori(userId, num).to_response()

@dotori_ns.route('')
class InitializeDotori(Resource):
    @dotori_ns.expect(dotori_ns.model('Initialize', {'user_id': fields.Integer(required=True)}))
    def post(self):
        data = dotori_ns.payload
        user_id = data.get('user_id')
        return DotoriService.initialize_user_dotori(user_id)

@dotori_ns.route('/all')
class GetAllDotori(Resource):
    def get(self):
        users = DotoriService.get_all_users_dotori()
        return users