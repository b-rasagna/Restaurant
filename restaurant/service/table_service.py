from sqlalchemy.exc import SQLAlchemyError

from restaurant import entities
from restaurant.dao import DAO


class Table:
    """Class for table services"""

    def __init__(self):
        self.__dao_obj = DAO()

    def createTables(self, number_of_tables):
        """
        Create tables.

        :return: number of tables newly created
        :rtype: dict
        """
        session = None
        try:
            output = dict()
            for i in range(number_of_tables):
                table_obj = entities.Tables(available=True, customer_id=None, customer_name=None, customer_mobile=None, order_id=None)
                table_obj, session = self.__dao_obj.put(table_obj, transaction=True, current_session=session)
                session.commit()
            output["message"] = "Tables created successfully"
            return output
        except SQLAlchemyError as e:
            if session:
                session.rollback()
            print(str(e))
            raise
        except Exception as e:
            if session:
                session.rollback()
            print(str(e))
            raise
        finally:
            if session:
                session.close()

    def bookTable(self, customer_name, customer_mobile):
        """
        Book a table.

        :return: a dict with details of table
        :rtype: dict
        """
        session = None
        try:
            output = dict()
            table_objs, session = self.__dao_obj.get_where(entities.Tables, "available = True", return_session=True)
            if len(table_objs) == 0:
                output["message"] = "All the tables are booked right now. Please try again later."
            else:
                customer_obj = entities.Customers(name=customer_name, mobile=customer_mobile, order_id=None)
                customer_obj, session = self.__dao_obj.put(customer_obj, transaction=True, current_session=session)
                customer_obj = customer_obj.to_dict()
                table_obj = table_objs[0]
                table_obj.available = False
                table_obj.customer_id = customer_obj.get("id")
                table_obj.customer_name = customer_name
                table_obj.customer_mobile = customer_mobile
                table_obj = table_obj.to_dict()
                session.commit()
                output["message"] = "Table booked successfully"
                output["Table Number"] = table_obj.get("id")
            return output
        except SQLAlchemyError as e:
            if session:
                session.rollback()
            print(str(e))
            raise
        except Exception as e:
            if session:
                session.rollback()
            print(str(e))
            raise
        finally:
            if session:
                session.close()

    def getAllTables(self):
        """
        Get all Tables

        :return: dict of table objects
        :rtype: dict
        """
        try:
            output = dict()
            table_objs = self.__dao_obj.get_all(entities.Tables)
            if len(table_objs) == 0:
                output["message"] = "No tables found."
            else:
                output["Total Number of tables"] = len(table_objs)
            return output
        except SQLAlchemyError as e:
            print(str(e))
            raise
        except Exception as e:
            print(str(e))
            raise

    def getBookedTables(self):
        """
        Get booked Tables

        :return: dict of table objects
        :rtype: dict
        """
        session = None
        try:
            output = dict()
            table_objs, session = self.__dao_obj.get_where(entities.Tables, "available = False", return_session=True)
            if len(table_objs) == 0:
                output["message"] = "No tables are booked."
            else:
                output["Total number of booked tables"] = len(table_objs)
                output["Booked Table numbers"] = [table_obj.to_dict().get("id") for table_obj in table_objs]
            return output
        except SQLAlchemyError as e:
            if session:
                session.rollback()
            print(str(e))
            raise
        except Exception as e:
            if session:
                session.rollback()
            print(str(e))
            raise
        finally:
            if session:
                session.close()

    def getAvailableTables(self):
        """
        Get available Tables

        :return: dict of table objects
        :rtype: dict
        """
        session = None
        try:
            output = dict()
            table_objs, session = self.__dao_obj.get_where(entities.Tables, "available = True", return_session=True)
            if len(table_objs) == 0:
                output["message"] = "No tables are available."
            else:
                output["Total number of available tables"] = len(table_objs)
                output["Available Table numbers"] = [table_obj.to_dict().get("id") for table_obj in table_objs]
            return output
        except SQLAlchemyError as e:
            if session:
                session.rollback()
            print(str(e))
            raise
        except Exception as e:
            if session:
                session.rollback()
            print(str(e))
            raise
        finally:
            if session:
                session.close()