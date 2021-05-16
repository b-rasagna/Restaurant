import json

from bottle import run, request, get, post
from sqlalchemy.exc import SQLAlchemyError

from restaurant.service.item_service import Item
from restaurant.service.table_service import Table
from restaurant.service.order_service import Order
from restaurant.util import Validate

@post('/order/place')
def placeOrder():
    output=dict()
    try:
        body = request.body.read().decode('utf8')
        get_dict = json.loads(body)
        items = get_dict.get('items')
        table_id = get_dict.get('table_id')
        validate_obj = Validate()
        errors = validate_obj.validate_form(get_dict, ['items', 'table_id'])
        if len(errors) == 0:
            order_obj = Order()
            output = order_obj.placeOrder(items, table_id)
        else:
            output["errors"] = errors
        return json.dumps(output)
    except SQLAlchemyError as e:
        output["message"] = str(e)
        return output, 500
    except Exception as e:
        output["message"] = str(e)
        return output, 500

@get('/order/all')
def getAllOrders():
    output=dict()
    try:
        order_obj = Order()
        output = order_obj.getAllOrders()
        return json.dumps(output)
    except SQLAlchemyError as e:
        output["message"] = str(e)
        return output, 500
    except Exception as e:
        output["message"] = str(e)
        return output, 500

@post('/menu/create')
def createItem():
    output=dict()
    try:
        body = request.body.read().decode('utf8')
        get_dict = json.loads(body)
        name = get_dict.get('name')
        price = get_dict.get('price')
        time = get_dict.get('time')
        available = get_dict.get('available')
        validate_obj = Validate()
        errors = validate_obj.validate_form(get_dict, ['name', 'price', 'time', 'available'])
        if len(errors) == 0:
            item_obj = Item()
            output = item_obj.createItem(name, price, time, available)
        else:
            output["errors"] = errors
        return json.dumps(output)
    except SQLAlchemyError as e:
        output["message"] = str(e)
        return output, 500
    except Exception as e:
        output["message"] = str(e)
        return output, 500

@get('/menu')
def showMenu():
    output=dict()
    try:
        item_obj = Item()
        output = item_obj.getAllItems()
        return json.dumps(output)
    except SQLAlchemyError as e:
        output["message"] = str(e)
        return output, 500
    except Exception as e:
        output["message"] = str(e)
        return output, 500

@post('/table/create/<number_of_tables:int>')
def createTables(number_of_tables):
    output=dict()
    try:
        table_obj = Table()
        output = table_obj.createTables(number_of_tables)
        return json.dumps(output)
    except SQLAlchemyError as e:
        output["message"] = str(e)
        return output, 500
    except Exception as e:
        output["message"] = str(e)
        return output, 500

@post('/table/book')
def bookTable():
    output=dict()
    try:
        body = request.body.read().decode('utf8')
        get_dict = json.loads(body)
        customer_name = get_dict.get('name')
        customer_mobile = get_dict.get('mobile')
        validate_obj = Validate()
        errors = validate_obj.validate_form(get_dict, ['name', 'mobile'])
        if len(errors) == 0:
            table_obj = Table()
            output = table_obj.bookTable(customer_name, customer_mobile)
        else:
            output["errors"] = errors
        return json.dumps(output)
    except SQLAlchemyError as e:
        output["message"] = str(e)
        return output, 500
    except Exception as e:
        output["message"] = str(e)
        return output, 500

@get('/table/all')
def getAllTables():
    output=dict()
    try:
        table_obj = Table()
        output = table_obj.getAllTables()
        return json.dumps(output)
    except SQLAlchemyError as e:
        output["message"] = str(e)
        return output, 500
    except Exception as e:
        output["message"] = str(e)
        return output, 500

@get('/table/booked')
def getBookedTables():
    output=dict()
    try:
        table_obj = Table()
        output = table_obj.getBookedTables()
        return json.dumps(output)
    except SQLAlchemyError as e:
        output["message"] = str(e)
        return output, 500
    except Exception as e:
        output["message"] = str(e)
        return output, 500

@get('/table/available')
def getAvailableTables():
    output=dict()
    try:
        table_obj = Table()
        output = table_obj.getAvailableTables()
        return json.dumps(output)
    except SQLAlchemyError as e:
        output["message"] = str(e)
        return output, 500
    except Exception as e:
        output["message"] = str(e)
        return output, 500

def start_services(port):
    """
    Start server

    :param port: Port on which to run the server
    :type port: int
    """
    try:
        host = '0.0.0.0'
        run(host=host, port=port)
    except Exception as e:
        print("Error starting the service..\n", str(e))
