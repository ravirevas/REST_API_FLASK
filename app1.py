from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Date, text, PrimaryKeyConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# Init our app here
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database url
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# init db
db = SQLAlchemy(app)


# init marshmallow
ma = Marshmallow(app)


class Datastore(db.Model):
    __tablename__ = 'dq2_datastore'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    create_ts = db.Column(db.DateTime, nullable=False, default=text('NOW()'))
    update_ts = db.Column(db.DateTime, nullable=False, default=text('NOW()'))
    zone = db.Column(db.String(250), nullable=False)
    conn_type = db.Column(db.String(50), nullable=False)

    def __init__(self, name,zone,conn_type):
        self.name = name
        self.zone = zone
        self.conn_type = conn_type





class DatastoreSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('name','zone','conn_type')


user_schema = DatastoreSchema(strict=True)
users_schema = DatastoreSchema(many=True)



# endpoint to create new user
@app.route("/user", methods=["POST"])
def add_user():
    name = request.json['name']                           #insert data in table 1
    zone=request.json['zone']
    conn_type=request.json['conn_type']


    new_user = Datastore(name,zone,conn_type)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)








class Entity(db.Model):
    __tablename__ = 'dq2_entity'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    subsidiary_name = db.Column(db.String(250), nullable=False)
    domain_name = db.Column(db.String(100), nullable=False)
    zone = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    datastore_id = db.Column(db.Integer, db.ForeignKey("dq2_datastore.id"))
    unq_row_id = db.Column(db.String(250), nullable=False)
    create_ts = db.Column(db.DateTime, nullable=False, default=text('NOW()'))
    update_ts = db.Column(db.DateTime, nullable=False, default=text('NOW()'))
    datastore = db.relationship("Datastore", backref=db.backref("entities", uselist=False))



    def __init__(self, name, subsidiary_name, domain_name, zone,type,location,datastore_id,unq_row_id):
         self.name = name
         self.subsidiary_name=subsidiary_name
         self.domain_name=domain_name
         self.zone=zone
         self.type=type
         self.location=location
         self.datastore_id=datastore_id
         self.unq_row_id=unq_row_id

class EntitySchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('name','subsidiary_name','domain_name','zone','type','location','datastore_id','unq_row_id')


Entity_schema = EntitySchema(strict=True)
Entityies_schema = EntitySchema(many=True)


@app.route("/entity", methods=["POST"])
def add_entity():                                               #insert data in table 2
    name = request.json['name']
    subsidiary_name=request.json['subsidiary_name']
    domain_name=request.json['domain_name']
    zone = request.json['zone']
    type = request.json['type']
    location = request.json['location']
    datastore_id = request.json['datastore_id']
    unq_row_id = request.json['unq_row_id']




    new_entity = Entity(name,subsidiary_name,domain_name,zone,type,location,datastore_id,unq_row_id)

    db.session.add(new_entity)
    db.session.commit()

    return Entity_schema.jsonify(new_entity)

@app.route("/entity", methods=["GET"])                 #dump entity table 2 data
def get_entity():
    all_entity = Entity.query.all()
    print(all_entity)
    result_entity = Entityies_schema.dump(all_entity)
    print(result_entity)
    return jsonify(result_entity.data)




@app.route("/user", methods=["GET"])
def get_user():                                   #dump all table 1 data
    all_users = Datastore.query.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)



# endpoint to get user detail by id
@app.route("/user/<id>", methods=["GET"])            #search in table 1
def user_detail(id):
    user = Datastore.query.get(id)
    return user_schema.jsonify(user)



@app.route("/entity/<datastore_id>", methods=["GET"])          # to search in table 2
def entity_detail(datastore_id):
    print(datastore_id)

    enity_q = Entity.query.filter_by(datastore_id=datastore_id)
    print(enity_q)
    return Entityies_schema.jsonify(enity_q)

@app.route("/entity/search/<name>", methods=["GET"])          # to search in table 2 with name
def entity_search_detail(name):
    datastore_iid=Datastore.query.with_entities(Datastore.id).filter_by(name=name).first()
    print(type(datastore_iid))
    print(datastore_iid[0])
    idd=datastore_iid[0]
    print(idd)
    print(type(idd))
    enity_q1 = Entity.query.filter_by(datastore_id=idd)
    return Entityies_schema.jsonify(enity_q1)



# endpoint to delete user
@app.route("/user/<id>", methods=["DELETE"])                  #delete in table1
def user_delete(id):
    user = Datastore.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)


if __name__ == '__main__':
    app.run(debug=True)






