from flask import Flask, request, jsonify
from rest_api_dq.metastore_model import *
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import configparser
import subprocess


config = configparser.ConfigParser()
config.read('C:\\Users\\Ravi\\PycharmProjects\\REST_API_FLASK\\conf\\config.ini')
username = config.get('MySQL_METASTORE', 'username')
password = config.get('MySQL_METASTORE', 'password')
hostname = config.get('MySQL_METASTORE', 'host')
databaseType = config.get('MySQL_METASTORE', 'databaseType')
port = config.get('MySQL_METASTORE', 'port')
databaseName = config.get('MySQL_METASTORE', 'databaseName')


app =  Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:root@localhost:3306/test3'

app.config['SQLALCHEMY_DATABASE_URI'] = databaseType+"+"+'pymysql://'+username+':'+password+'@'+hostname+":"+port+"/"+databaseName
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# init marshmallow
ma = Marshmallow(app)


class DatastoreSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'name','conn_type','create_ts','update_ts','zone')



Datastore_schema = DatastoreSchema(strict=True)
Datastores_schema = DatastoreSchema(many=True)


@app.route('/drop_all_dq')
def drop_all():
    Base.metadata.drop_all(bind=db.engine)                #to drop all tables
    return jsonify("Tables have been dropped")


@app.route('/create_all_dq')
def create_all():
    Base.metadata.create_all(bind=db.engine)              #to create all tables
    return jsonify("Tables have been created")



@app.route("/datastore", methods=["POST"])
def add_datastore():

    name = request.json['name']         #insert data in table 1

    zone=request.json['zone']
    conn_type=request.json['conn_type']

    new_datastore = Datastore(name,conn_type,zone)

    db.session.add(new_datastore)
    db.session.commit()

    return Datastore_schema.jsonify(new_datastore)


@app.route("/datastore/<id>", methods=["PUT"])
def update_datastore(id):
    datastore_id = db.session.query(Datastore).get(id)
    name = request.json['name']
    zone = request.json['zone']                                    #update datastore on id
    conn_type = request.json['conn_type']

    datastore_id.name = name
    datastore_id.zone = zone
    datastore_id.conn_type = conn_type

    db.session.commit()
    return Datastore_schema.jsonify(datastore_id)


@app.route("/datastore", methods=["GET"])
def get_datastore():                                   #dump all table 1 data
    datastore_query = db.session.query(Datastore).all()
    result_datastore = Datastores_schema.dump(datastore_query)
    return jsonify(result_datastore.data)



# endpoint to get user detail by id
@app.route("/datastore/<id>", methods=["GET"])            #search in table 1
def datstore_detail(id):
    datastore_id = db.session.query(Datastore).get(id)
    return Datastore_schema.jsonify(datastore_id)


@app.route("/datastores/<name>", methods=["GET"])
def get_datastores(name):                                   #dump all table 1 data with name
    expr="%"+name+"%"

    result = db.session.query(Datastore).filter(Datastore.name.ilike(expr))
    result_datastore_name = Datastores_schema.dump(result)
    print(result)
    #datastore_query_name = db.session.query(Datastore).filter_by(name=name)
    #result_datastore_name = Datastores_schema.dump(datastore_query_name)
    #print(result_datastore_name_1)
    return jsonify(result_datastore_name.data)


@app.route("/datastore/<id>", methods=["DELETE"])                  #delete in table1
def datastore_delete(id):
    datastore_id = db.session.query(Datastore).get(id)
    db.session.delete(datastore_id)
    db.session.commit()

    return Datastore_schema.jsonify(datastore_id)


########################################table1_crudends_here##############################

class EntitySchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id','name','subsidiary_name','domain_name','zone','type','location','datastore_id','unq_row_id','create_ts','update_ts')




Entity_schema = EntitySchema(strict=True)
Entities_schema = EntitySchema(many=True)

@app.route("/entity", methods=["POST"])
def add_entity():   #insert data in table 2

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



@app.route("/entity/<id>", methods=["PUT"])
def update_entity(id):
    entity_id = db.session.query(Entity).get(id)
    name = request.json['name']
    subsidiary_name = request.json['subsidiary_name']                                    #update  on id
    domain_name = request.json['domain_name']
    zone = request.json['zone']
    type = request.json['type']
    location = request.json['location']
    datastore_id = request.json['datastore_id']
    unq_row_id = request.json['unq_row_id']

    entity_id.name = name
    entity_id.subsidiary_name = subsidiary_name
    entity_id.domain_name = domain_name
    entity_id.zone = zone
    entity_id.type = type
    entity_id.location = location
    entity_id.datastore_id = datastore_id
    entity_id.unq_row_id = unq_row_id

    db.session.commit()
    return Entity_schema.jsonify(entity_id)




@app.route("/entity", methods=["GET"])                 #dump entity table 2 data
def get_entity():
    all_entity = db.session.query(Entity).all()
    print(all_entity)
    result_entity = Entities_schema.dump(all_entity)
    print(result_entity)
    return jsonify(result_entity.data)


@app.route("/entities/<name>", methods=["GET"])
def get_entity_name(name):                                        # dump all table 2 data with name
    expr = "%" + name + "%"
    result = db.session.query(Entity).filter(Entity.name.ilike(expr))
    result_entity_name = Entities_schema.dump(result)
    return jsonify(result_entity_name.data)



@app.route("/entity/<id>", methods=["GET"])            #search in table 2
def entity_details(id):
    Entity_id = db.session.query(Entity).get(id)
    return Entity_schema.jsonify(Entity_id)


@app.route("/entity/<id>", methods=["DELETE"])                  #delete in table2
def entity_delete(id):
    entity_id = db.session.query(Entity).get(id)
    db.session.delete(entity_id)
    db.session.commit()

    return Entity_schema.jsonify(entity_id)


################################table2crudends##################################
class RuletypeSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'name','template_query','implementation_name','create_ts','update_ts')



Ruletype_schema = RuletypeSchema(strict=True)
Ruletypes_schema = RuletypeSchema(many=True)



@app.route("/ruletype", methods=["POST"])
def add_ruletype():
    name = request.json['name']         #insert data in table 3

    template_query=request.json['template_query']
    implementation_name=request.json['implementation_name']

    new_ruletype = RuleType(name,template_query,implementation_name)

    db.session.add(new_ruletype)
    db.session.commit()

    return Ruletype_schema.jsonify(new_ruletype)

@app.route("/ruletype/<id>", methods=["PUT"])
def update_ruletype(id):
    ruletype_id = db.session.query(RuleType).get(id)
    name = request.json['name']
    template_query = request.json['template_query']                                    #update  on id
    implementation_name = request.json['implementation_name']

    ruletype_id.name = name
    ruletype_id.template_query = template_query
    ruletype_id.implementation_name = implementation_name

    db.session.commit()
    return Ruletype_schema.jsonify(ruletype_id)





@app.route("/ruletype", methods=["GET"])                 #dump entity table 3 data
def get_ruletype():
    all_ruletype = db.session.query(RuleType).all()
    result_ruletype = Ruletypes_schema.dump(all_ruletype)
    print(result_ruletype)
    return jsonify(result_ruletype.data)




@app.route("/ruletypes/<name>", methods=["GET"])
def get_ruletype_name(name):                                        # dump all table 2 data with name
    expr = "%" + name + "%"
    result = db.session.query(RuleType).filter(RuleType.name.ilike(expr))
    result_ruletype_name = Ruletypes_schema.dump(result)
    return jsonify(result_ruletype_name.data)



@app.route("/ruletype/<id>", methods=["GET"])            #search in table 3
def ruletype_details(id):
    ruletype_id = db.session.query(RuleType).get(id)
    return Ruletype_schema.jsonify(ruletype_id)


@app.route("/ruletype/<id>", methods=["DELETE"])                  #delete in table3
def ruletype_delete(id):
    ruleype_id = db.session.query(RuleType).get(id)
    db.session.delete(ruleype_id)
    db.session.commit()

    return Ruletype_schema.jsonify(ruleype_id)


##############################crudendsfor table3######################


class RuletypeparameterSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id','rule_type_id','name','mandatory_flg','default_value','create_ts','update_ts')


Ruletypeparameter_schema =  RuletypeparameterSchema(strict=True)
Ruletypesparameters_schema =  RuletypeparameterSchema(many=True)


@app.route("/ruletypeparams", methods=["POST"])
def add_ruletypeparams():
    rule_type_id = request.json['rule_type_id']                  #insert data in table 4

    name=request.json['name']
    mandatory_flg=request.json['mandatory_flg']
    default_value = request.json['default_value']

    new_ruletype_params = RuleTypeParameter(rule_type_id,name,mandatory_flg,default_value)

    db.session.add(new_ruletype_params)
    db.session.commit()

    return Ruletypeparameter_schema.jsonify(new_ruletype_params)

@app.route("/ruletypeparams/<id>", methods=["PUT"])
def update_ruletypeparams(id):
    ruletypeparams_id = db.session.query(RuleTypeParameter).get(id)
    rule_type_id = request.json['rule_type_id']                             # updated on id
    name = request.json['name']
    mandatory_flg = request.json['mandatory_flg']
    default_value = request.json['default_value']

    ruletypeparams_id.rule_type_id = rule_type_id
    ruletypeparams_id.name = name
    ruletypeparams_id.mandatory_flg = mandatory_flg
    ruletypeparams_id.default_value = default_value

    db.session.commit()
    return Ruletypeparameter_schema.jsonify(ruletypeparams_id)






@app.route("/ruletypeparams", methods=["GET"])                 #dump entity table 4 data
def get_ruletypeparams():
    all_ruletypeparams = db.session.query(RuleTypeParameter).all()
    result_ruletype_par = Ruletypesparameters_schema.dump(all_ruletypeparams)
    print(result_ruletype_par)
    return jsonify(result_ruletype_par.data)


@app.route("/ruletypesparams/<name>", methods=["GET"])
def get_ruletypeparams_name(name):                                        # dump all table 4 data with name
    expr = "%" + name + "%"
    result = db.session.query(RuleTypeParameter).filter(RuleTypeParameter.name.ilike(expr))
    result_ruletypeparams_name = Ruletypesparameters_schema.dump(result)
    return jsonify(result_ruletypeparams_name.data)



@app.route("/ruletypeparams/<id>", methods=["GET"])            #search in table 4
def ruletypeparams_details(id):
    ruletypeparams_id = db.session.query(RuleTypeParameter).get(id)
    return Ruletypeparameter_schema.jsonify(ruletypeparams_id)


@app.route("/ruletypeparams/<id>", methods=["DELETE"])                  #delete in table4
def ruletypeparams_delete(id):
    ruleypeparams_id = db.session.query(RuleTypeParameter).get(id)
    db.session.delete(ruleypeparams_id)
    db.session.commit()

    return Ruletypeparameter_schema.jsonify(ruleypeparams_id)

#####################################crudfor table4 ends#################################

class RuleAssignmentSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id','description','rule_type_id','send_alert_flg','stop_job_flg','target_entity_id','source_entity_id','create_ts','update_ts','store_result_to_db_flg')


RuleAssignment_schema =  RuleAssignmentSchema(strict=True)
RuleAssignments_schema =  RuleAssignmentSchema(many=True)



@app.route("/ruleassig", methods=["POST"])
def add_ruleassig():
    description = request.json['description']                  #insert data in table 5
    rule_type_id=request.json['rule_type_id']
    send_alert_flg=request.json['send_alert_flg']
    stop_job_flg = request.json['stop_job_flg']
    target_entity_id = request.json['target_entity_id']
    source_entity_id = request.json['source_entity_id']
    store_result_to_db_flg = request.json['store_result_to_db_flg']

    new_ruleassig_params = RuleAssignment(description,rule_type_id,send_alert_flg,stop_job_flg,target_entity_id,source_entity_id,store_result_to_db_flg)

    db.session.add(new_ruleassig_params)
    db.session.commit()

    return RuleAssignment_schema.jsonify(new_ruleassig_params)


@app.route("/ruleassig/<id>", methods=["PUT"])
def update_ruleassig(id):
    ruleassig_id = db.session.query(RuleAssignment).get(id)
    description = request.json['description']                            #update on id
    rule_type_id = request.json['rule_type_id']
    send_alert_flg = request.json['send_alert_flg']
    stop_job_flg = request.json['stop_job_flg']
    target_entity_id = request.json['target_entity_id']
    source_entity_id = request.json['source_entity_id']
    store_result_to_db_flg = request.json['store_result_to_db_flg']

    ruleassig_id.description = description
    ruleassig_id.rule_type_id = rule_type_id
    ruleassig_id.send_alert_flg = send_alert_flg
    ruleassig_id.stop_job_flg = stop_job_flg
    ruleassig_id.target_entity_id = target_entity_id
    ruleassig_id.source_entity_id = source_entity_id
    ruleassig_id.store_result_to_db_flg = store_result_to_db_flg

    db.session.commit()
    return RuleAssignment_schema.jsonify(ruleassig_id)






@app.route("/ruleassig", methods=["GET"])                 #dump entity table 5 data
def get_ruleassig():
    all_ruleassig = db.session.query(RuleAssignment).all()
    result_ruleassig = RuleAssignments_schema.dump(all_ruleassig)
    print(result_ruleassig)
    return jsonify(result_ruleassig.data)



@app.route("/ruleassigs/<description>", methods=["GET"])
def get_ruleassigs_name(description):                                        # dump all table 5 data with name
    expr = "%" + description + "%"
    result = db.session.query(RuleAssignment).filter(RuleAssignment.description.ilike(expr))
    result_ruleassigs_name = RuleAssignments_schema.dump(result)
    return jsonify(result_ruleassigs_name.data)




@app.route("/ruleassig/<id>", methods=["GET"])            #search in table 5
def ruleassig_details(id):
    ruleassig_id = db.session.query(RuleAssignment).get(id)
    return RuleAssignment_schema.jsonify(ruleassig_id)



@app.route("/ruleassig/<id>", methods=["DELETE"])                  #delete in table5
def ruleassig_delete(id):
    ruleassig_id = db.session.query(RuleAssignment).get(id)
    db.session.delete(ruleassig_id)
    db.session.commit()

    return RuleAssignment_schema.jsonify(ruleassig_id)


##########################################crudfor5table5end############################################



class RuleAssignmentParameterSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id','rule_assignment_id','rule_type_parameter_id','value','create_ts','update_ts')


RuleAssignmentParameter_schema =  RuleAssignmentParameterSchema(strict=True)
RuleAssignmentParameters_schema =  RuleAssignmentParameterSchema(many=True)





@app.route("/ruleassignmentpara", methods=["POST"])
def add_ruleassigparams():
    rule_assignment_id = request.json['rule_assignment_id']                  #insert data in table 6

    rule_type_parameter_id=request.json['rule_type_parameter_id']
    value=request.json['value']

    new_ruleassig_params = RuleAssignmentParameter(rule_assignment_id,rule_type_parameter_id,value)

    db.session.add(new_ruleassig_params)
    db.session.commit()

    return RuleAssignmentParameter_schema.jsonify(new_ruleassig_params)


@app.route("/ruleassignmentpara/<id>", methods=["PUT"])
def update_ruleassignmentpara(id):
    ruleassignmentpara_id = db.session.query(RuleAssignmentParameter).get(id)
    rule_assignment_id = request.json['rule_assignment_id']                       # update on id

    rule_type_parameter_id = request.json['rule_type_parameter_id']
    value = request.json['value']

    ruleassignmentpara_id.rule_assignment_id = rule_assignment_id
    ruleassignmentpara_id.rule_type_parameter_id = rule_type_parameter_id
    ruleassignmentpara_id.value = value

    db.session.commit()
    return RuleAssignmentParameter_schema.jsonify(ruleassignmentpara_id)




@app.route("/ruleassignmentpara", methods=["GET"])                 #dump entity table 6 data
def get_ruleassigpara():
    all_ruleassig_para = db.session.query(RuleAssignmentParameter).all()
    result_ruleassig_para = RuleAssignmentParameters_schema.dump( all_ruleassig_para)
    print(result_ruleassig_para)
    return jsonify(result_ruleassig_para.data)



@app.route("/ruleassignmentparas/<value>", methods=["GET"])
def get_ruleassignmentparas_name(value):                                        # dump all table 6 data with name
    expr = "%" + value + "%"
    result = db.session.query(RuleAssignmentParameter).filter(RuleAssignmentParameter.value.ilike(expr))
    result_ruleassignmentparas_name = RuleAssignmentParameters_schema.dump(result)
    return jsonify(result_ruleassignmentparas_name.data)


@app.route("/ruleassignmentpara/<id>", methods=["GET"])            #search in table 6
def ruleassigpara_details(id):
    ruleassig_para_id = db.session.query(RuleAssignmentParameter).get(id)
    return RuleAssignmentParameter_schema.jsonify(ruleassig_para_id)



@app.route("/ruleassignmentpara/<id>", methods=["DELETE"])                  #delete in table6
def ruleassigpara_delete(id):
    ruleassigpara_id = db.session.query(RuleAssignmentParameter).get(id)
    db.session.delete(ruleassigpara_id)
    db.session.commit()

    return RuleAssignmentParameter_schema.jsonify(ruleassigpara_id)

######################################crud for table 6 ends#####################################


class RuleSetSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id','name','create_ts','update_ts')


Ruleset_schema = RuleSetSchema(strict=True)
Rulesets_schema =  RuleSetSchema(many=True)




@app.route("/ruleset", methods=["POST"])
def add_ruleset():
    name = request.json['name']                  #insert data in table 7

    new_ruleset = RuleSet(name)

    db.session.add(new_ruleset)
    db.session.commit()

    return Ruleset_schema.jsonify(new_ruleset)



@app.route("/ruleset/<id>", methods=["PUT"])
def update_ruleset(id):
    ruleset_id = db.session.query(RuleSet).get(id)
    name = request.json['name']                      # update on id

    ruleset_id.name = name

    db.session.commit()
    return Ruleset_schema.jsonify(ruleset_id)







@app.route("/ruleset", methods=["GET"])                 #dump entity table 7 data
def get_ruleset():
    all_ruleset = db.session.query(RuleSet).all()
    result_rule_set = Rulesets_schema.dump(all_ruleset)
    print(result_rule_set)
    return jsonify(result_rule_set.data)




@app.route("/rulesets/<name>", methods=["GET"])
def get_rulesets_name(name):                                        # dump all table 7 data with name
    expr = "%" + name + "%"
    result = db.session.query(RuleSet).filter(RuleSet.name.ilike(expr))
    result_rulesets_name = Rulesets_schema.dump(result)
    return jsonify(result_rulesets_name.data)




@app.route("/ruleset/<id>", methods=["GET"])            #search in table 7
def ruleset_details(id):
    ruleset_id = db.session.query(RuleSet).get(id)
    return Ruleset_schema.jsonify(ruleset_id)



@app.route("/ruleset/<id>", methods=["DELETE"])                  #delete in table7
def ruleset_delete(id):
    ruleset_id_del = db.session.query(RuleSet).get(id)
    db.session.delete(ruleset_id_del)
    db.session.commit()

    return Ruleset_schema.jsonify(ruleset_id_del)




###########################################crudend fro table 7###################################


class RuleSetAssignmentSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id','rule_set_id','rule_assignment_id','active_flg','create_ts','update_ts')


RuleSetAssignment_schema = RuleSetAssignmentSchema(strict=True)
RuleSetAssignments_schema =  RuleSetAssignmentSchema(many=True)


@app.route("/rulesetassig", methods=["POST"])
def add_rulesetassig():
    rule_set_id = request.json['rule_set_id']                  #insert data in table 7

    rule_assignment_id = request.json['rule_assignment_id']
    active_flg = request.json['active_flg']
    new_rulesetassig = RuleSetAssignment(rule_set_id,rule_assignment_id,active_flg)

    db.session.add(new_rulesetassig)
    db.session.commit()

    return RuleSetAssignment_schema.jsonify(new_rulesetassig)




@app.route("/rulesetassig/<id>", methods=["PUT"])
def update_rulesetassig(id):
    rulesetassig_id = db.session.query(RuleSetAssignment).get(id)
    rule_set_id = request.json['rule_set_id']

    rule_assignment_id = request.json['rule_assignment_id']
    active_flg = request.json['active_flg']                              # update on id

    rulesetassig_id.rule_set_id = rule_set_id
    rulesetassig_id.rule_assignment_id = rule_assignment_id
    rulesetassig_id.active_flg = active_flg

    db.session.commit()
    return RuleSetAssignment_schema.jsonify(rulesetassig_id)


@app.route("/rulesetassig", methods=["GET"])                 #dump entity table 8 data
def get_rulesetassig():
    all_ruleset_assig = db.session.query(RuleSetAssignment).all()
    result_rule_set = RuleSetAssignments_schema.dump(all_ruleset_assig)
    print(result_rule_set)
    return jsonify(result_rule_set.data)



@app.route("/rulesetassig/<id>", methods=["GET"])            #search in table 8
def rulesetassig_details(id):
    rulesetassig_id = db.session.query(RuleSetAssignment).get(id)
    return RuleSetAssignment_schema.jsonify(rulesetassig_id)



@app.route("/rulesetassig/<id>", methods=["DELETE"])                  #delete in table8
def rulesetassig_delete(id):
    rulesetassig_id_del = db.session.query(RuleSetAssignment).get(id)
    db.session.delete(rulesetassig_id_del)
    db.session.commit()

    return RuleSetAssignment_schema.jsonify(rulesetassig_id_del)



#######################crundends for table 8###################################
class RuleLogSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id','rule_assignment_id','rule_set_assignment_id','data_dt','rule_start_ts','rule_end_ts','batch_dt', 'target_sql_query', 'source_sql_query','target_result_value','source_result_value','result','status','partition_type','seq_num','create_ts','update_ts')


RuleLog_schema = RuleLogSchema(strict=True)
RuleLogs_schema = RuleLogSchema(many=True)



@app.route("/rulelog", methods=["POST"])
def add_rulelog():
    id = request.json['id']
    rule_assignment_id = request.json['rule_assignment_id']
    rule_set_assignment_id = request.json['rule_set_assignment_id']
    rule_end_ts = request.json['rule_end_ts']
    batch_dt = request.json['batch_dt']
    target_sql_query = request.json['target_sql_query']
    source_sql_query = request.json['source_sql_query']
    target_result_value = request.json['target_result_value']
    source_result_value = request.json['source_result_value']
    result = request.json['result']
    status = request.json['status']
    partition_type = request.json['partition_type']
    seq_num = request.json['seq_num']



    new_rulelog = RuleLog(id,rule_assignment_id,rule_set_assignment_id,rule_end_ts,batch_dt,target_sql_query,source_sql_query,target_result_value,source_result_value,result,status,partition_type,seq_num)

    db.session.add(new_rulelog)
    db.session.commit()

    return RuleLog_schema.jsonify(new_rulelog)






@app.route("/rulelog", methods=["GET"])                 #dump entity table 9 data
def get_rulelog():
    all_rulelog = db.session.query(RuleLog).all()
    result_rule_log = RuleLogs_schema.dump(all_rulelog)
    return jsonify(result_rule_log.data)



@app.route("/rulelog/<id>", methods=["GET"])            #search in table 9
def rulelog_details(id):
    rulelog_id = db.session.query(RuleLog).filter_by(id=id)
    return RuleLogs_schema.jsonify(rulelog_id)



@app.route("/rulelog/<id>", methods=["DELETE"])                  #delete in table9
def rulelog_delete(id):
    rulelog_id_del = db.session.query(RuleLog).get(id)
    db.session.delete(rulelog_id_del)
    db.session.commit()

    return RuleLog_schema.jsonify(rulelog_id_del)




if __name__ == '__main__':
    app.run(debug=True)