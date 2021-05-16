import argparse
import sys

class RestaurantServer:
    """
    CLI commands to setup database and start the gunicorn server
    """
    def __init__(self):
        """
        Constructor function
        """
        parser = argparse.ArgumentParser(
            description='Restaurant Server',
            usage='''restaurant <command> [<args>]

        The available commands are:
           init_db                          Initialize database schema
           start_server                     Start a HTTP server to enable the APIs
        ''')
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        getattr(self, args.command)()

    @staticmethod
    def init_db():
        """
        Initialize the database
        """
        print("Inside Database initialization")
        from sqlalchemy import create_engine
        from restaurant.util import ConfigUtil
        from restaurant.entities import Base
        engine = create_engine(ConfigUtil().get_database_config()['url'])
        Base.metadata.create_all(engine)
        print("Database initialized!!!")

    @staticmethod
    def start_server():
        """
        Start a gunicorn http server.
        """
        parser = argparse.ArgumentParser(
            description='Start server')
        parser.add_argument('--port', type=int,
                            help="Give port no to start the services on", required=True)
        args = parser.parse_args(sys.argv[2:])
        from restaurant.apis import restaurant_api
        restaurant_api.start_services(port=args.port)

if __name__ == '__main__':
    RestaurantServer()
