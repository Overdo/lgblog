from itsdangerous import TimedJSONWebSignatureSerializer
from flask_restful import Resource
from flask import abort, current_app
from lgblog.controllers.flask_restful import parsers
from lgblog.models import User


class AuthApi(Resource):
    """Restful api of Auth."""

    def post(self):
        """Can be execute when receive HTTP Method `POST`."""
        args = parsers.user_post_parser.parse_args()
        user = User.query.filter_by(username=args['username']).first()

        # Check the args['password'] whether as same as user.password.
        if user.check_password(args['password']):
            # serializer object will be saved the token period of time.
            serializer = TimedJSONWebSignatureSerializer(
                current_app.config['SECRET_KEY'],
                expires_in=600
            )
            return {'token': str(serializer.dumps({'id': user.id})).lstrip('b').strip('\'')}
        else:
            abort(401)
