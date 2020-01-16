# Sterling
[![Build Status](https://travis-ci.com/jacobfelknor/sterling.svg?branch=master)](https://travis-ci.com/jacobfelknor/sterling)

## What is Sterling?
Sterling is a personal finance web application in which users can keep track of their personal finacial records. You can add accounts and then transactions to those accounts and view them in a simple, clean interface. Sterling also supports importing CSV files from your bank (currently only supports the CSV (Excel) format outputted by Elevations Credit Union. Will expand support in the future.) for easy import. And don't worry about duplicating transactions during the import - Sterling is smart enough to avoid this.

## How can I use Sterling?
Sterling is deployed and accessible at https://jacobfelknor.pythonanywhere.com 

## Future Plans
Right now, Sterling is simply a bookkeeping application. Beyond that, there is a very simple Dashboard that will display a graph representing you Net Worth based on the data you have entered. I plan to add many different analysis tools to Sterling in the future which will make it much more interesting and fun to use. This will include generating reports for your personal reference, budgeting ideas, etc. In addition, I plan to continuely update the application with new features and improvements. Those activley being attended to will be in the Issues tab of GitHub. Feel free to report issues you find to me on this page. 

# For Developers
## Local Installation/Development Server

Clone the sterling repository into a suitable directory. Create a virtual environment in this directory by using the following command:
```bash
python -m venv <venv_name>
```

Activate your virtual environment:\
Windows:
```bash
./<venv_name>/Scripts/activate
```
Linux/Mac:
```bash
source <venv_name>/bin/activate
```

Install requirements:
```bash
pip install -r requirements/base.txt
```

## Database Setup
Ensure you have a database management software installed. We recommend [PostgreSQL](https://www.postgresql.org/download/) or [MySQL](https://dev.mysql.com/downloads/).
We also recommend a DBMS GUI, such as [pgAdmin 4](https://www.pgadmin.org/download/) for PostgreSQL, or [MySQL Workbench](https://dev.mysql.com/downloads/) for MySQL

After your database manager of choice is installed, create a database named "sterling"\
**NOTE:** Creating the database and configuring passwords is beyond the scope of this documentation, however it is an important step. Please reference external sources for this information

Create a "keys.py" file in the config folder. Secret keys can be generated [here](https://miniwebtool.com/django-secret-key-generator/) 

Populate it as follows:

```python
secret_key = 'your_secret_key'
db_password = "your_password"
```

Update your database settings in config/settings/development.py if necessary. Consult the [Django's Database Documentation](https://docs.djangoproject.com/en/2.2/ref/settings/#databases)

## Usage

Make Database Migrations:
```bash
python manage.py makemigrations
```

Migrate changes to Database:
```bash
python manage.py migrate
```

Start Django Development Server:
```bash
python manage.py runserver
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
