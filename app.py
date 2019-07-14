from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# init app
app = Flask(__name__)

# Set our base dir for a db file
basedir = os.path.abspath(os.path.dirname(__file__))

# set up our db 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite') 

# set another config setting needed only to suppress warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db
db = SQLAlchemy(app)
# init marshmallow
ma = Marshmallow(app)

# Resource (Table) Class/Model
class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), unique=True)
	description = db.Column(db.String(200))
	price = db.Column(db.Float)
	qty = db.Column(db.Integer)
	
	def __init__(self, name, description, price, qty):
		self.name = name
		self.description = description
		self.price = price
		self.qty = qty
		
# Product Schema class (marshmallow)
# what fields do we show?

class ProductSchema(ma.Schema):
	class Meta:
		fields = ('id', 'name', 'description', 'price', 'qty')
		
# Init schema
product_schema = ProductSchema(strict=True) 
products_schema = ProductSchema(many=True, strict=True)  	

		
# here we can create the db through the shell: type in console:
# >>> python
# >>> from app import db
# >>> db.create_all()

# NOW we have the db.sqlite file

# create a product
@app.route('/product', methods=['POST'])
def add_product():
	name = request.json['name']
	description = request.json['description']
	price = request.json['price']
	qty = request.json['qty']
	
	new_product = Product(name, description, price, qty)
	
	db.session.add(new_product)
	db.session.commit()
	
	return product_schema.jsonify(new_product)
	
# GET all products
@app.route('/product', methods=['GET'])
def get_products():
	all_products = Product.query.all()
	result = products_schema.dump(all_products)
	
	return jsonify(result.data) 
	


# @app.route("/")
# def home():
    # return render_template('home.html')


	
	
# Run Server
if __name__ == "__main__":
	app.run(debug=True)
