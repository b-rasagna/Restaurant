# restaurant server

package for restaurant server

Installation:

1. Clone the repo
2. Install the package using ``python setup.py install``
3. Set APP_HOME variable. Application configuaration file need to be placed inside app home.
4. Create a PostgreSQL database and set the url in configuaration file. Please find the sample configuaration file in app_home directory.
4. Use "restaurant init_db" to initialize database schema.
5. Use "restaurant start_server" to login to modelops

Running testcases

1. When the testcases executed on an empty database, ideally all the testcases should pass.
2. Go to app folder
3. Run "python -m pytest ./" to execute testcases
