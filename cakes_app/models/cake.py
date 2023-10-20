from flask_restx import fields

cake_model = {
    'name': fields.String,
    'comment': fields.String,
    'imageUrl': fields.String,
    'yumFactor': fields.Integer,
}
