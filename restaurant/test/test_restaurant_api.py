import unittest

from restaurant.service.item_service import Item
from restaurant.service.table_service import Table
from restaurant.service.order_service import Order

class TestRestaurant(unittest.TestCase):

    # create table 
    def test_1(self):
        table_obj = Table()
        response = table_obj.createTables(5)
        self.assertEqual(response["message"], "Tables created successfully")

    # book table
    def test_2(self):
        table_obj = Table()
        response = table_obj.bookTable("Rasagna", "9553599947")
        self.assertEqual(response["message"], "Table booked successfully")

    # get all tables
    def test_3(self):
        table_obj = Table()
        response = table_obj.getAllTables()
        self.assertEqual(response["Total Number of tables"], 5)

    # get booked tables
    def test_4(self):
        table_obj = Table()
        response = table_obj.getBookedTables()
        self.assertEqual(response["Total number of booked tables"], 1)

    # get available tables
    def test_5(self):
        table_obj = Table()
        response = table_obj.getAvailableTables()
        self.assertEqual(response["Total number of available tables"], 4)

    # create item
    def test_6(self):
        item_obj = Item()
        response = item_obj.createItem("Soup", 100.00, 20, True)
        self.assertEqual(response["message"], "Item created successfully")

    # get all items
    def test_7(self):
        item_obj = Item()
        item_obj.createItem("Biryani", 500.00, 60, True)
        item_obj.createItem("Curry", 250.00, 30, True)
        item_obj.createItem("Juice", 50.00, 10, True)
        item_obj.createItem("Ice Cream", 100.00, 15, True)
        response = item_obj.getAllItems()
        self.assertEqual(response["Available items"], ["Soup", "Biryani", "Curry", "Juice", "Ice Cream"])

    # place order
    def test_8(self):
        order_obj = Order()
        response = order_obj.placeOrder(["Soup", "Biryani"], 1)
        self.assertEqual(response["message"], "Order placed successfully")
        self.assertEqual(response["Ordered Items"], ["Soup", "Biryani"])
        self.assertEqual(response["Order will be delivered in"], "1 hours 0 minutes")

    # get orders
    def test_9(self):
        order_obj = Order()
        response = order_obj.getAllOrders()
        self.assertEqual(response["Total Number of orders"], 1)
