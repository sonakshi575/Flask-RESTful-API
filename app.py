from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:Aihub@2020@localhost:3306/aienterprise'
db = SQLAlchemy(app)

class Details(db.Model):
    __tablename__ = "details"
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    dob = db.Column(db.String(100))
    amount = db.Column(db.Integer)

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self
    def __init__(self,student_id,first_name,last_name,dob,amount):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.amount = amount
    def __repr__(self):
        return '' % self.student_id
db.create_all()


class DetailsSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Details
        sqla_session = db.session
    student_id = fields.Number(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required =True)
    dob = fields.String(required=True)
    amount = fields.Number(required=True)

@app.route('/details', methods = ['GET'])
def index():
    get_products = Details.query.all()
    product_schema = DetailsSchema(many=True)
    products = product_schema.dump(get_products)
    return make_response(jsonify({"Student Details": products}))

@app.route('/details/<student_id>', methods = ['GET'])
def get_details_by_id(id):
    get_product = Details.query.get(id)
    product_schema = DetailsSchema()
    product = product_schema.dump(get_product)
    return make_response(jsonify({"Student Details": product}))

@app.route('/details/<student_id>', methods = ['POST'])
def update_details_by_id(student_id):
    data = request.get_json()
    get_product = Details.query.get(student_id)
    if data.get('first_name'):
        get_product.first_name = data['first_name']
    if data.get('last_name'):
        get_product.last_name = data['last_name']
    if data.get('dob'):
        get_product.dob = data['dob']
    if data.get('amount'):
        get_product.price= data['amount']
    db.session.add(get_product)
    db.session.commit()
    product_schema = DetailsSchema(only=['student_id', 'first_name', 'last_name','dob','amount'])
    product = product_schema.dump(get_product)
    return make_response(jsonify({"Student Details": product}))

@app.route('/details/<student_id>', methods = ['DELETE'])
def delete_details_by_id(student_id):
    get_product = Details.query.get(student_id)
    db.session.delete(get_product)
    db.session.commit()
    return make_response("",204)

@app.route('/details', methods = ['POST'])
def create_product():
    data = request.get_json()
    product_schema = DetailsSchema()
    product = product_schema.load(data)
    result = product_schema.dump(product.create())
    return make_response(jsonify({"Student Details": result}),200)

if __name__ == "__main__":
    app.run(debug=True , port=8054)
