from sqlalchemy.exc import SQLAlchemyError

from restaurant import entities
from restaurant.dao import DAO


class Item:
    """Class for Menu services"""

    def __init__(self):
        self.__dao_obj = DAO()

    def createItem(self, name, price, time, available):
        """
        create an item.

        :return: item details
        :rtype: dict
        """
        session = None
        try:
            output = dict()
            item_objs, session = self.__dao_obj.get_where(entities.Items, "name = '{0}'".format(str(name)), return_session=True)
            if len(item_objs) != 0:
                output["message"] = "Item already exists"
            else:
                item_obj = entities.Items(name, price, time, available)
                item_obj, session = self.__dao_obj.put(item_obj, transaction=True, current_session=session)
                session.commit()
                output["message"] = "Item created successfully"
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

    def getAllItems(self):
        """
        Get all Items

        :return: dict of item objects
        :rtype: dict
        """
        session=None
        try:
            output = dict()
            item_objs, session = self.__dao_obj.get_where(entities.Items, "available = True", return_session=True)
            if len(item_objs) == 0:
                output["message"] = "No items found."
            else:
                output["Available items"] = [item_obj.to_dict().get("name") for item_obj in item_objs]
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