from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config.config import DevelopmentConfig
# import the psycopg2 package so that we can use it
# This line imports the psycopg2 module in our program.
# Using the classes and method defined psycopg2 module we can communicate with PostgreSQL.
import psycopg2
import pygal


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db = SQLAlchemy(app)


# create a connection between python flask app and your database 
# This is accomplished by creating a connection through the db user,password,host,port and the database itself
# To accomplish this we use the connect method in psycopg2

# The username you use to work with PostgreSQL, The default username for the PostgreSQL database is Postgres.
# Password – Password is given by the user at the time of installing the PostgreSQL.
# Host Name  – is the server name or Ip address on which PostgreSQL is running. if you are running on localhost, then you can use localhost, or it’s IP i.e., 127.0.0.0
# Database Name – Database name to which you want to connect. Here we are using Database named “postgres_db”.


connection = psycopg2.connect(user ="postgres", password ="wamzy", host ="127.0.0.1", port ="5432", database ="charts")


# We then create a cursor object connection using the connection object created above 
# This enables us to create a env to run our postgresSQL queries from python-flask

cursor = connection.cursor()
print ( connection.get_dsn_parameters(),"\n")

cursor.execute("SELECT version();")
record = cursor.fetchone()

print("You are connected to", record)

from models.inventories import Inventories
from models.sales import Sale
from models.stock import Stock

@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def home():    
   
    cursor.execute("SELECT * FROM cost;")
    # cursor.execute("SELECT COUNT(product) FROM IMS;")


    recordsEntered = cursor.fetchall()

    print(recordsEntered)

    connection.commit()
    # cursor.close()
    # connection.close()

    # create the line graph

    record1 = []
    record2 = []
    record3 = []

    for recordEntered in recordsEntered:

        record1.append(recordEntered[1])
        record2.append(recordEntered[2])
        record3.append(recordEntered[3])

    
    print("x-labels: ",record1)
    print("datapoints: ",record2)

    line_chart = pygal.Line()
    line_chart.title = 'Daily transport cost in the Month of March 2020'
    line_chart.x_labels = record1
    line_chart.add('day_amount',  record2)
    line_chart.add('night_amount', record3)
    line_chart.render()

    line = line_chart.render_data_uri()

    # CREATE A PIE CHART 

    pie_chart = pygal.Pie()
    pie_chart.title = 'Products vs Services'
    # pie_chart.add()
    # pie_chart.add()



    return render_template('home.html',line=line)

@app.route('/about')
def about():

    return render_template('about.html')

@app.route('/contact')
def contact():

    return render_template('contact.html')

@app.route('/inventories', methods=['GET','POST'])
def inventories():

    inventories = Inventories.fetch_records()
    # print(inventories)



    if request.method == 'POST':

        name = request.form['name']
        type = request.form['type']
        buying_price = request.form['buying_price']
        selling_price = request.form['selling_price']

        inventory = Inventories(name=name, type=type, buying_price=buying_price, selling_price=selling_price)
        inventory.create_record()
        return redirect(url_for('inventories'))



    return render_template('inventories.html', inventories=inventories)

if __name__ == '__main__':
    app.run()