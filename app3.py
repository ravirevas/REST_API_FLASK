from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Date, text, PrimaryKeyConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from conf.config_manager import GlobalConf
#from conf.global_context import GlobalContext

Base = declarative_base()

""" 
--> All the metastore objects have been defined below. 
--> SQL Alchemy would automatically map the objects below to the database 
    that SQLAlchemy engine is configured to connect to and makes the data 
    available in these objects for querying. 
--> All the relations between the objects are maintained by SQLAlchemy which 
    makes it easy to access related data from the respective objects
"""


class Datastore(Base):
    __tablename__ = 'dq2_datastore'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    create_ts = Column(DateTime, nullable=False, default=datetime.datetime.now)
    update_ts = Column(DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    zone = Column(String(250), nullable=False)
    conn_type = Column(String(50), nullable=False)

    def __init__(self, name,zone,conn_type):
        self.name = name
        self.zone = zone
        self.conn_type = conn_type

class Entity(Base):
    __tablename__ = 'dq2_entity'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    subsidiary_name = Column(String(250), nullable=False)
    domain_name = Column(String(100), nullable=False)
    zone = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    location = Column(String(250), nullable=False)
    datastore_id = Column(Integer, ForeignKey("dq2_datastore.id"))
    unq_row_id = Column(String(250), nullable=False)
    create_ts = Column(DateTime, nullable=False, default=datetime.datetime.now)
    update_ts = Column(DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    datastore = relationship("Datastore", backref=backref("entities", uselist=False,cascade="all,delete"))

    def __init__(self, name, subsidiary_name, domain_name, zone,type,location,datastore_id,unq_row_id):
         self.name = name
         self.subsidiary_name=subsidiary_name
         self.domain_name=domain_name
         self.zone=zone
         self.type=type
         self.location=location
         self.datastore_id=datastore_id
         self.unq_row_id=unq_row_id


class RuleType(Base):
    __tablename__ = 'dq2_rule_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    template_query = Column(String(250), nullable=False)
    implementation_name = Column(String(100), nullable=False)
    create_ts = Column(DateTime, nullable=False, default=datetime.datetime.now)
    update_ts = Column(DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __init__(self, name,template_query,implemetation_name):
        self.name = name
        self.template_query = template_query
        self.implementation_name = implemetation_name




class RuleTypeParameter(Base):
    __tablename__ = 'dq2_rule_type_parameter'
    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_type_id = Column(Integer, ForeignKey("dq2_rule_type.id"))
    name = Column(String(250), nullable=False)
    mandatory_flg = Column(String(250), nullable=False)
    default_value = Column(String(250), nullable=False)
    create_ts = Column(DateTime, nullable=False, default=datetime.datetime.now)
    update_ts = Column(DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    ruletype = relationship("RuleType", foreign_keys=[rule_type_id],
                            backref=backref("ruletypeparameters", lazy='joined',cascade="all,delete"))


    def __init__(self, rule_type_id, name, mandatory_flg, default_value):
         self.rule_type_id = rule_type_id
         self.name=name
         self.mandatory_flg=mandatory_flg
         self.default_value=default_value




class RuleAssignment(Base):
    __tablename__ = 'dq2_rule_assignment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(250), nullable=False)
    rule_type_id = Column(Integer, ForeignKey("dq2_rule_type.id"))
    send_alert_flg = Column(String(250), nullable=False)
    stop_job_flg = Column(String(250), nullable=False)
    target_entity_id = Column(Integer, ForeignKey("dq2_entity.id"))
    source_entity_id = Column(Integer, ForeignKey("dq2_entity.id"))
    create_ts = Column(DateTime, nullable=False, default=datetime.datetime.now)
    update_ts = Column(DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    store_result_to_db_flg = Column(String(1), nullable=False, default=text('N'))
    ruletype = relationship("RuleType", foreign_keys=[rule_type_id], backref=backref("ruleassignment", lazy='joined',cascade="all,delete"))
    sourceentity = relationship("Entity", foreign_keys=[source_entity_id], lazy='joined')
    targetentity = relationship("Entity", foreign_keys=[target_entity_id], lazy='joined')


    def __init__(self, description,rule_type_id,send_alert_flg,stop_job_flg,target_entity_id,source_entity_id,store_result_to_db_flg):
         self.description = description
         self.rule_type_id=rule_type_id
         self.send_alert_flg=send_alert_flg
         self.stop_job_flg=stop_job_flg
         self.target_entity_id = target_entity_id
         self.source_entity_id = source_entity_id
         self.store_result_to_db_flg = store_result_to_db_flg





class RuleAssignmentParameter(Base):
    __tablename__ = 'dq2_rule_assignment_parameter'
    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_assignment_id = Column(Integer, ForeignKey("dq2_rule_assignment.id"))
    rule_type_parameter_id = Column(Integer, ForeignKey("dq2_rule_type_parameter.id"))
    value = Column(String(250), nullable=False)
    create_ts = Column(DateTime, nullable=False, default=datetime.datetime.now)
    update_ts = Column(DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    ruleassignment = relationship("RuleAssignment", foreign_keys=[rule_assignment_id],
                                  backref=backref("ruleassignmentparameters", lazy='joined',cascade="all,delete"))
    ruletypeparameter = relationship("RuleTypeParameter", foreign_keys=[rule_type_parameter_id],
                                     backref=backref("ruleassignmentParameter", lazy='joined',cascade="all,delete"))



    def __init__(self,  rule_assignment_id, rule_type_parameter_id, value):
         self.rule_assignment_id = rule_assignment_id
         self.rule_type_parameter_id=rule_type_parameter_id
         self.value=value





class RuleSet(Base):
    __tablename__ = 'dq2_rule_set'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    create_ts = Column(DateTime, nullable=False, default=datetime.datetime.now)
    update_ts = Column(DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)


    def __init__(self,name):
         self.name = name


class RuleSetAssignment(Base):
    __tablename__ = 'dq2_rule_set_assignment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_set_id = Column(Integer, ForeignKey("dq2_rule_set.id"))
    rule_assignment_id = Column(Integer, ForeignKey("dq2_rule_assignment.id"))
    active_flg = Column(String(250), nullable=False)
    create_ts = Column(DateTime, nullable=False, default=datetime.datetime.now)
    update_ts = Column(DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    ruleassignment = relationship("RuleAssignment", foreign_keys=[rule_assignment_id],
                                  backref=backref("rulesetassignment", uselist=False, lazy='joined',cascade="all,delete"))
    ruleset = relationship("RuleSet", foreign_keys=[rule_set_id], backref=backref("rulesetassignment", lazy='joined',cascade="all,delete"))

    def __init__(self, rule_set_id,rule_assignment_id,active_flg):
        self.rule_set_id = rule_set_id
        self.rule_assignment_id = rule_assignment_id
        self.active_flg = active_flg



class RuleLog(Base):
    __tablename__ = 'dq2_rule_log'
    id = Column(String(500), nullable=False)
    rule_assignment_id = Column(Integer, ForeignKey("dq2_rule_assignment.id"))
    rule_set_assignment_id = Column(Integer, ForeignKey("dq2_rule_set_assignment.id"))
    data_dt = Column(Date, nullable=False, default=datetime.datetime.now)
    rule_start_ts = Column(DateTime, nullable=False, default=datetime.datetime.now)
    rule_end_ts = Column(DateTime, nullable=True)
    batch_dt = Column(String(45), nullable=True)
    target_sql_query = Column(String(5000), nullable=True)
    source_sql_query = Column(String(5000), nullable=True)
    target_result_value = Column(String(500), nullable=True)
    source_result_value = Column(String(500), nullable=True)
    result = Column(String(45), nullable=True)
    status = Column(String(45), nullable=True)
    partition_type = Column(String(250), nullable=True)
    seq_num = Column(Integer)
    create_ts = Column(DateTime, nullable=False, default=datetime.datetime.now)
    update_ts = Column(DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    ruleassignment = relationship("RuleAssignment", foreign_keys=[rule_assignment_id], lazy='joined')

    __table_args__ = (PrimaryKeyConstraint("id", "rule_assignment_id", "rule_set_assignment_id"), )

    def __init__(self,id, rule_assignment_id,rule_set_assignment_id,rule_end_ts,batch_dt,target_sql_query,source_sql_query,target_result_value,source_result_value,result,status,partition_type,seq_num):
        self.id=id
        self.rule_assignment_id = rule_assignment_id
        self.rule_set_assignment_id = rule_set_assignment_id
        self.rule_end_ts = rule_end_ts
        self.batch_dt = batch_dt
        self.target_sql_query = target_sql_query
        self.source_sql_query = source_sql_query
        self.target_result_value = target_result_value
        self.source_result_value = source_result_value
        self.result = result
        self.status = status
        self.partition_type =partition_type
        self.seq_num=seq_num



