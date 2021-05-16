from sqlalchemy.exc import SQLAlchemyError

from restaurant import entities
from restaurant.dao import DAO


class Order:
    """Class for Order services"""

    def __init__(self):
        self.__dao_obj = DAO()

    def placeOrder(self, items, table_id):
        """
        Place an order.

        :return: order details
        :rtype: dict
        """
        session = None
        try:
            output = dict()
            if len(items) == 0:
                output["message"] = "Please provide item names to place an order."
                return output
            amount = 0
            item_objs = self.__dao_obj.get_all(entities.Items)
            if len(item_objs) == 0:
                output["message"] = "No items are available currently."
                return output
            available_items = [item_obj.to_dict().get("name") for item_obj in item_objs]
            max_time_in_mins = max([item_obj.to_dict().get("time") for item_obj in item_objs])
            hours = max_time_in_mins//60
            minutes = max_time_in_mins % 60
            time_string = "{} hours {} minutes".format(hours, minutes)
            for item_name in items:
                if item_name not in available_items:
                    output["message"] = "{0} not available.".format(str(item_name))
                    return output
                for item_obj in item_objs:
                    item_obj = item_obj.to_dict()
                    if item_name == item_obj.get("name"):
                        if item_obj.get("available"):
                            amount+=item_obj.get("price")
                        else:
                            output["message"] = "{0} not available currently.".format(str(item_name))
                            return output
                        
            table_obj, session = self.__dao_obj.get_item(entities.Tables, table_id, return_session=True)
            if table_obj != None:
                table_objs, session = self.__dao_obj.get_where(entities.Tables, "id = {0} and available = False".format(str(table_id)), return_session=True, current_session=session)
                if len(table_objs) != 0:
                    order_obj = entities.Orders(status="Preparing", items=items, amount=amount, payment=False, table_id=table_id, time=time_string)
                    order_obj, session = self.__dao_obj.put(order_obj, transaction=True, current_session=session)
                    session.commit()
                    order_obj = order_obj.to_dict()
                    table_obj = table_objs[0]
                    table_obj.order_id = order_obj.get("id")
                    table_obj = table_obj.to_dict()
                    session.commit()
                    customer_obj, session = self.__dao_obj.get_item(entities.Customers, table_obj.get("customer_id"), return_session=True)
                    customer_obj.order_id = order_obj.get("id")
                    session.commit()
                    output["message"] = "Order placed successfully"
                    output["Table ID"] = table_id
                    output["Order ID"] = order_obj.get("id")
                    output["Ordered Items"] = items
                    output["Order will be delivered in"] = time_string
                    return output
                else:
                    output["message"] = "Please book a table before placing order."
                    return output
            else:
                output["message"] = "Table with ID {0} is not available.".foramt(str(table_id))
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

    def getAllOrders(self):
        """
        Get all Orders

        :return: dict of order objects
        :rtype: dict
        """
        try:
            output = dict()
            order_objs = self.__dao_obj.get_all(entities.Orders)
            if len(order_objs) == 0:
                output["message"] = "No orders found."
            else:
                output["Total Number of orders"] = len(order_objs)
            return output
        except SQLAlchemyError as e:
            print(str(e))
            raise
        except Exception as e:
            print(str(e))
            raise