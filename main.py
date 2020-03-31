from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config.config import DevelopmentConfig,ProductionConfig
from flask_login import LoginManager,login_user,login_required, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
# import the psycopg2 package so that we can use it
# This line imports the psycopg2 module in our program.
# Using the classes and method defined psycopg2 module we can communicate with PostgreSQL.
import psycopg2
import pygal


app = Flask(__name__)
app.config.from_object(ProductionConfig)

db = SQLAlchemy(app)
login_manager = LoginManager(app)


# create a connection between python flask app and your database 
# This is accomplished by creating a connection through the db user,password,host,port and the database itself
# To accomplish this we use the connect method in psycopg2

# The username you use to work with PostgreSQL, The default username for the PostgreSQL database is Postgres.
# Password – Password is given by the user at the time of installing the PostgreSQL.
# Host Name  – is the server name or Ip address on which PostgreSQL is running. if you are running on localhost, then you can use localhost, or it’s IP i.e., 127.0.0.0
# Database Name – Database name to which you want to connect. Here we are using Database named “postgres_db”.


connection = psycopg2.connect(user ="pcdqdnreapwvmm", 
                             password ="15b3f90225665ba6512e182b97863bdbcbcc574503e03622ce856f573439aacd", 
                             host ="ec2-54-159-112-44.compute-1.amazonaws.com", 
                             port ="5432", 
                             database ="d848k7580t8pdn")


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
from models.users import User


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

@login_manager.request_loader
def request_loader(request):

    users = User.query.all()
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user


@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/signup', methods=['GET','POST'])
def signup():

    if request.method == 'POST':

        username = request.form['username'] 
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            print('Email already exists')
            return redirect(url_for('signup'))
        else:
            hashed_password = generate_password_hash(password)

            user = User(username=username, email=email, password=hashed_password)
            user.create_record()
            print('Account created successfully')
            return redirect(url_for('signup'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('inventories'))
            
            print('Invalid Username or Password')
            return redirect(url_for('login'))

        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/')
def home():    
   
    # cursor.execute("SELECT * FROM cost;")
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
# @login_required 
def inventories():

    inventories = Inventories.fetch_records()
    # print(inventories)

    cursor.execute("""SELECT inv_id, sum(stock) as "stock"
            FROM ((SELECT st.inv_id, sum(stock) as "stock"
            FROM public.stocks as st
            GROUP BY inv_id) union all
                (SELECT sa.inv_id, - sum(quantity) as "quantity"
            FROM public.sales as sa
            GROUP BY inv_id) 
                ) stsa
            GROUP BY inv_id
            ORDER BY inv_id;""")
    
    available_stock = cursor.fetchall()
   

    if request.method == 'POST':

        name = request.form['name']
        type = request.form['type']
        buying_price = request.form['buying_price']
        selling_price = request.form['selling_price']

        inventory = Inventories(name=name, type=type, buying_price=buying_price, selling_price=selling_price)
        inventory.create_record()
        return redirect(url_for('inventories'))

    return render_template('inventories.html', inventories=inventories, available_stock=available_stock)

# deleting an item 
@app.route('/inventories/delete/<int:id>', methods=['GET','POST'] )
def deleteInventory(id):

    delete_inventory = Inventories.fetch_by_id(id)

    if delete_inventory:

        print('Record deleted successfully')
        return redirect(url_for('inventories'))
    else:

        print('record not found')
        return redirect(url_for('inventories'))


@app.route('/make_sale/<id>', methods=['GET','POST'])
def make_sale(id):

    if request.method == 'POST':


        quantity = request.form['quantity']

        sale = Sale(inv_id=id, quantity=quantity)
        sale.create_record()

        return redirect(url_for('inventories'))

@app.route('/addstock/<id>', methods=['GET','POST'])
def add_stock(id):

    if request.method == 'POST':


        stock = request.form['stock']

        new_stock = Stock(inv_id=id, stock=stock)
        new_stock.create_record()
        return redirect(url_for('inventories'))

@app.route('/viewsales/<id>', methods=['GET','POST'])
def viewsales(id):

    sales = Sale.fetch_by_id(id)

    return render_template('viewsales.html', sales=sales)

# edit Inventory
@app.route('/inventories/update/<int:id>', methods=['POST'])
def edit_employees(id):

    record = Inventories.query.filter_by(id=id).first()
    

    if request.method == 'POST':
        record.name = request.form['name']
        record.type = request.form['newtype']
        record.buying_price = request.form['buying_price']
        record.selling_price = request.form['selling_price']

        db.session.commit()
    return redirect(url_for('inventories'))
        

      




# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()