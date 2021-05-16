import sqlalchemy as sy

from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from restaurant.util import ConfigUtil

conf_util = ConfigUtil()
class DAO:
    """
    Data Access Object
    """
    if "pool_size" in conf_util.get_database_config() :
        pool_size = conf_util.get_database_config()["pool_size"]
    else:
        pool_size = 5

    engine = sy.create_engine(conf_util.get_database_config()['url'], pool_pre_ping=True, pool_size=pool_size, poolclass=QueuePool)
    sessionmaker = sessionmaker(bind=engine)
    session = sessionmaker()

    def get_all(self, cls):
        """
        get all the objects of a particular entity

        :param cls: Class for which objects need to be extracted from database
        :return:
        """
        try:
            return DAO.session.query(cls).all()
        except:
            DAO.session.rollback()
            raise

    def get_where(self, cls, condition, return_session=False, current_session=None):
        """
        Get objects of a particular class along with filtering using condition specified
        :param cls: Class of objects to be extracted
        :param condition: Conditions for filtering
        :param return_session: Whether to return session(used in case of update)
        :return: Object for the class specified which met the critiria specified and
        session in case of return_session=True
        """
        session_obj=None
        try:
            if return_session == False:
                session_obj = DAO.session
                return session_obj.query(cls).filter(sy.text(condition)).all()
            elif current_session == None:
                session_obj = self.sessionmaker()
                return session_obj.query(cls).filter(sy.text(condition)).all(), session_obj
            else:
                session_obj = current_session
                return session_obj.query(cls).filter(sy.text(condition)).all(), session_obj
        except:
            session_obj.rollback()
            raise

    def get_item(self, cls, id, return_session=False):
        """
        Get single object of a particular class given the primary key value.
        :param cls: The class for which object need to be extracted
        :param id: Primary key value for filtering
        :return: Get an object that
        """
        session_obj=None
        try:
            if (return_session):
                session_obj = self.sessionmaker()
                return session_obj.query(cls).filter_by(id=id).first(), session_obj
            else:
                session_obj = DAO.session
                return session_obj.query(cls).filter_by(id=id).first()
        except:
            session_obj.rollback()
            raise

    def put(self, object, transaction=False, current_session=None):
        """
        Put a object in the database
        :param object: The object to be written to database
        :param transaction: Whether to return the session
        :return: Object after insertion to the database and session object if transaction = True
        """
        session_obj=None
        try:
            if transaction == False:
                session_obj = DAO.session
                session_obj.add(object)
                session_obj.commit()
                return object
            elif current_session == None:
                session_obj = self.sessionmaker()
                session_obj.add(object)
                session_obj.flush()
                return object, session_obj
            else:
                session_obj = current_session
                session_obj.add(object)
                session_obj.flush()
                return object, session_obj
        except:
            session_obj.rollback()
            raise