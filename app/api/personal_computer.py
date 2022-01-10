from flask import jsonify, current_app
from flask_restful import Resource, Api, fields, marshal_with, reqparse, abort
from .. import db
from . import api
from ..personal_computers.models import PersonalComputer


post_post_args = reqparse.RequestParser()
post_post_args.add_argument("firm", type=str, help="Firm is required", required=True)
post_post_args.add_argument("type_processor", type=str, help="Type processor is required", required=True)
post_post_args.add_argument("image_file", type=str, help="Image is required", required=True)
post_post_args.add_argument("date_created", type=str, help="Date is required", required=True)
post_post_args.add_argument("clock_frequency", type=float, help="Clock frequency is required", required=True)
post_post_args.add_argument("is_available", type=bool, help="Available is required", required=True)
post_post_args.add_argument("user_id", type=int, help="User id is required", required=True)
post_post_args.add_argument("category_ram_id", type=int, help="Category id is required", required=True)


post_update_args = reqparse.RequestParser()
post_update_args.add_argument("firm", type=str)
post_update_args.add_argument("type_processor", type=str)
post_update_args.add_argument("image_file", type=str)
post_update_args.add_argument("is_available", type=bool)


resourses = {
    'id': fields.Integer,
    'firm': fields.String,
    'type_processor': fields.String,
    'image_file': fields.String(default='default_comp.jpg'),
    'date_created': fields.String,
    'clock_frequency': fields.Float,
    'is_available': fields.Boolean,
    'user_id': fields.Integer,
    'category_ram_id': fields.Integer,
}


class PersonalComputerAllApi(Resource):
    @marshal_with(resourses)
    def get(self):
        return PersonalComputer.query.all()


class PersonalComputerApi(Resource):
    @marshal_with(resourses)
    def get(self, pc_id):
        pc = PersonalComputer.query.filter_by(id=pc_id).first()

        if not pc:
            abort(404, message="Could not find post with that id")

        return pc

    @marshal_with(resourses)
    def post(self, pc_id):
        data = post_post_args.parse_args()
        pc = PersonalComputer.query.filter_by(id=pc_id).first()

        if pc:
            abort(409, message="PC id taken ...")

        pc_new = PersonalComputer(
            id=pc_id,
            firm=data['firm'],
            image_file=data['image_file'],
            date_created=db.func.now(),
            type_processor=data['type_processor'],
            clock_frequency=data['clock_frequency'],
            is_available=data['is_available'],
            user_id=data['user_id'],
            category_ram_id=data['category_ram_id'],
        )

        db.session.add(pc_new)
        db.session.commit()
        return pc_new, 201

    @marshal_with(resourses)
    def put(self, pc_id):
        args = post_update_args.parse_args()
        pc = PersonalComputer.query.filter_by(id=pc_id).first()

        if not pc:
            abort(404, message="Post doesn`t exist, cannot update")
        if args['firm']:
            pc.firm = args['firm']
        if args['type_processor']:
            pc.type_processor = args['type_processor']
        if args['image_file']:
            pc.image_file = args['image_file']
        if type(args['is_available']) == bool:
            pc.is_available = args['is_available']

        db.session.commit()
        return pc

    @marshal_with(resourses)
    def delete(self, pc_id):
        pc = PersonalComputer.query.filter_by(id=pc_id).first()
        db.session.delete(pc)
        db.session.commit()
        return jsonify({'message': 'The PC has been deleted!'})


api = Api(current_app)
api.add_resource(PersonalComputerApi, "/api/kandiuk_anatolii/<int:pc_id>")
api.add_resource(PersonalComputerAllApi, "/api/kandiuk_anatolii/")


