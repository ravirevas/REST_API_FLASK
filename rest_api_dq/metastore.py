from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Date, text, PrimaryKeyConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
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
    create_ts = Column(DateTime, nullable=False, default=text('NOW()'))
    update_ts = Column(DateTime, nullable=False, default=text('NOW()'))
    zone = Column(String(250), nullable=False)
    conn_type = Column(String(50), nullable=False)


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
    create_ts = Column(DateTime, nullable=False, default=text('NOW()'))
    update_ts = Column(DateTime, nullable=False, default=text('NOW()'))
    datastore = relationship("Datastore", backref=backref("entities", uselist=False))


class RuleType(Base):
    __tablename__ = 'dq2_rule_type'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    template_query = Column(String(250), nullable=False)
    implementation_name = Column(String(100), nullable=False)
    create_ts = Column(DateTime, nullable=False, default=text('NOW()'))
    update_ts = Column(DateTime, nullable=False, default=text('NOW()'))


class RuleTypeParameter(Base):
    __tablename__ = 'dq2_rule_type_parameter'
    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_type_id = Column(Integer, ForeignKey("dq2_rule_type.id"))
    name = Column(String(250), nullable=False)
    mandatory_flg = Column(String(250), nullable=False)
    default_value = Column(String(250), nullable=False)
    create_ts = Column(DateTime, nullable=False, default=text('NOW()'))
    update_ts = Column(DateTime, nullable=False, default=text('NOW()'))
    ruletype = relationship("RuleType", foreign_keys=[rule_type_id],
                            backref=backref("ruletypeparameters", lazy='joined'))


class RuleAssignment(Base):
    __tablename__ = 'dq2_rule_assignment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(250), nullable=False)
    rule_type_id = Column(Integer, ForeignKey("dq2_rule_type.id"))
    send_alert_flg = Column(String(250), nullable=False)
    stop_job_flg = Column(String(250), nullable=False)
    target_entity_id = Column(Integer, ForeignKey("dq2_entity.id"))
    source_entity_id = Column(Integer, ForeignKey("dq2_entity.id"))
    create_ts = Column(DateTime, nullable=False, default=text('NOW()'))
    update_ts = Column(DateTime, nullable=False, default=text('NOW()'))
    store_result_to_db_flg = Column(String(1), nullable=False, default=text('N'))
    ruletype = relationship("RuleType", foreign_keys=[rule_type_id], backref=backref("ruleassignment", lazy='joined'))
    sourceentity = relationship("Entity", foreign_keys=[source_entity_id], lazy='joined')
    targetentity = relationship("Entity", foreign_keys=[target_entity_id], lazy='joined')


class RuleAssignmentParameter(Base):
    __tablename__ = 'dq2_rule_assignment_parameter'
    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_assignment_id = Column(Integer, ForeignKey("dq2_rule_assignment.id"))
    rule_type_parameter_id = Column(Integer, ForeignKey("dq2_rule_type_parameter.id"))
    value = Column(String(250), nullable=False)
    create_ts = Column(DateTime, nullable=False, default=text('NOW()'))
    update_ts = Column(DateTime, nullable=False, default=text('NOW()'))
    ruleassignment = relationship("RuleAssignment", foreign_keys=[rule_assignment_id],
                                  backref=backref("ruleassignmentparameters", lazy='joined'))
    ruletypeparameter = relationship("RuleTypeParameter", foreign_keys=[rule_type_parameter_id],
                                     backref=backref("ruleassignmentParameter", lazy='joined'))


class RuleSet(Base):
    __tablename__ = 'dq2_rule_set'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    create_ts = Column(DateTime, nullable=False, default=text('NOW()'))
    update_ts = Column(DateTime, nullable=False, default=text('NOW()'))


class RuleSetAssignment(Base):
    __tablename__ = 'dq2_rule_set_assignment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    rule_set_id = Column(Integer, ForeignKey("dq2_rule_set.id"))
    rule_assignment_id = Column(Integer, ForeignKey("dq2_rule_assignment.id"))
    active_flg = Column(String(250), nullable=False)
    create_ts = Column(DateTime, nullable=False, default=text('NOW()'))
    update_ts = Column(DateTime, nullable=False, default=text('NOW()'))
    ruleassignment = relationship("RuleAssignment", foreign_keys=[rule_assignment_id],
                                  backref=backref("rulesetassignment", uselist=False, lazy='joined'))
    ruleset = relationship("RuleSet", foreign_keys=[rule_set_id], backref=backref("rulesetassignment", lazy='joined'))


class RuleLog(Base):
    __tablename__ = 'dq2_rule_log'
    id = Column(String(500), nullable=False)
    rule_assignment_id = Column(Integer, ForeignKey("dq2_rule_assignment.id"))
    rule_set_assignment_id = Column(Integer, ForeignKey("dq2_rule_set_assignment.id"))
    data_dt = Column(Date, nullable=False, default=text('NOW()'))
    rule_start_ts = Column(DateTime, nullable=False, default=text('NOW()'))
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
    create_ts = Column(DateTime, nullable=False, default=text('NOW()'))
    update_ts = Column(DateTime, nullable=False, default=text('NOW()'))
    ruleassignment = relationship("RuleAssignment", foreign_keys=[rule_assignment_id], lazy='joined')

    __table_args__ = (PrimaryKeyConstraint("id", "rule_assignment_id", "rule_set_assignment_id"), )




# method that makes the session to the meta store available to the requester.
def getSession():
    """ Creating SQL Alchemy Engine with MySQL type and binding it to the base metadata class"""
    #gc = GlobalConf()
    #datastore_credentials_path = GlobalContext.get_param("datastoreCredentialsPath")
    conn_name = "MySQL_METASTORE"
    #dbc = gc.get_conf(config_name=conn_name, file_path=datastore_credentials_path)
    #credentials = dict(dbc.items(conn_name))
    engine = create_engine("mysql+pymysql://root:root@localhost:3306/test3")

    Base.metadata.bind = engine
    # Connecting to the DQ Framework meta store
    #engine.execute("use {c[databasename]}".format(c=credentials))
    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()
    # global session
    return session

#engine = "mysql+pymysql://root:root@localhost:3306/test3"