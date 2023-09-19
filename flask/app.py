import sqlite3
import os
from flask import Flask, render_template, request, g, flash, abort, url_for
from FDataBase import FDataBase

#config
DATABASE = 'tmp/app.db'
DEBUG = True
SECRET_KEY = 'IDDQD!idfka%123$'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'app.db')))

menu = [{"name": "Главная", "url": "/"}, 
        {"name": "О проекте", "url":"/about"}, 
        {"name": "Связь с разработчиком", "url":"/contact"}]

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.route("/")
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', menu = dbase.getMenu())

@app.route("/stations", methods=["POST", "GET"])
def stations():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        if len(request.form['name']) >= 4 :
            res = dbase.stations(request.form['name'], request.form['url'])
            if not res:
                flash('Ошибка добавления станции', category='error')
            else:
                flash('Станция успешно добавлена', category='success')
        else:
            flash('Ошибка добавления станции', category='error')
    
    return render_template('stations.html', menu=dbase.getMenu(), title="Станции", stations=dbase.getStationAnonce())

@app.route("/certificates", methods=["POST", "GET"])
def certificates():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        if len(request.form['name']) >= 4 :
            res = dbase.certificates(request.form['name'], request.form['length'], request.form['cadastr'], request.form['StationList'])
            if not res:
                flash('Ошибка добавления Сертификата', category='error')
            else:
                flash('Сертификат успешно добавлен', category='success')
        else:
            flash('Ошибка добавления Сертификата', category='error')
    
    return render_template('certificates.html', menu=dbase.getMenu(), title="Добавить Сертификат", stations=dbase.getStationAnonce())

@app.route("/agroprom", methods=["POST", "GET"])
def agroprom():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == "POST":
        res = dbase.objectsInCertificates(request.form['name'], request.form['number'], 2)
        if not res:
            flash('Ошибка добавления Объекта', category='error')
        else:
            flash('Объект успешно добавлен в Сертификат', category='success')

    return render_template('agroprom.html', menu=dbase.getMenu(), certificates=dbase.getCertificateAnonce(), propertyObjects=dbase.getObjectAnonce(), 
                           objectsInCertificate=dbase.getObjectInCertificatesAnonce(), title="Станция Агропром")

@app.route("/zarya", methods=["POST", "GET"])
def zarya():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == "POST":
        res = dbase.objectsInCertificates(request.form['name'], request.form['number'], 1)
        if not res:
            flash('Ошибка добавления Объекта', category='error')
        else:
            flash('Объект успешно добавлен в Сертификат', category='success')

    return render_template('zarya.html', menu=dbase.getMenu(), certificates=dbase.getCertificateAnonce(), propertyObjects=dbase.getObjectAnonce(), 
                           objectsInCertificate=dbase.getObjectInCertificatesAnonce(), title="Станция Заря")

@app.route("/objects", methods=["POST", "GET"])
def objects():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == "POST":
        if len(request.form['name']) >= 4 :
            res = dbase.propertyObjects(request.form['name'])
            if not res:
                flash('Ошибка добавления Объекта', category='error')
            else:
                flash('Объект успешно добавлен', category='success')
        else:
            flash('Ошибка добавления Объекта', category='error')

    return render_template('objects.html', menu=dbase.getMenu(), objects=dbase.propertyObjects, title="Добавить Объект")

@app.route("/tenants", methods =["POST", "GET"])
def tenants():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == "POST":
        if len(request.form['name']) >= 4 :
            res = dbase.tenants(request.form['name'])
            if not res:
                flash('Ошибка добавления Арендатора', category='error')
            else:
                flash('Арендатор успешно добавлен', category='success')
        else:
            flash('Ошибка добавления Арендатора', category='error')

    return render_template('tenants.html', menu=dbase.getMenu(), tenants=dbase.getTenantAnonce(), title="Добавить арендатора")

@app.route("/rent", methods=["POST", "GET"])
def rent():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == "POST":
        if len(request.form['name']) >= 4 :
            res = dbase.certificates(request.form['name'], request.form['price'], request.form['TenantList'])
            if not res:
                flash('Ошибка добавления Договора', category='error')
            else:
                flash('Договор успешно добавлен', category='success')
        else:
            flash('Ошибка добавления Договор', category='error')

    return render_template('rent.html', menu=dbase.getMenu(), rent=dbase.getRentAnonce(), tenants=dbase.getTenantAnonce(), title="Добавить Договор")

@app.route("/rentObject", methods=["POST", "GET"])
def rentObject():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == "POST":
        res = dbase.rentalObjects(request.form['rent'], request.form['object'])
        if not res:
            flash('Ошибка добавления Объекта', category='error')
        else:
            flash('Объект успешно добавлен в Договор', category='success')

    return render_template('rentObject.html', menu=dbase.getMenu(),  propertyObjects=dbase.getObjectAnonce(), rent=dbase.getRentAnonce(),
                           rentalObjects=dbase.getRentalObjectsAnonce(), title="Добавление объектов в Договора")

    

@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close

@app.route("/about")
def about():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('about.html', menu = dbase.getMenu())


#Метод убран за ненадобностью
#@app.route("/contact", methods=["POST", "GET"])
#def contact():
#    if request.method == 'POST':
#        if len(request.form['username']) >2:
#            flash('Сообщение отправлено')
#        else:
#            flash('Ошибка отправки')
#
#    
#    return render_template('contact.html', title = "Связь с разработчиком", menu = menu)

@app.errorhandler(404)
def PageNotFound(error):
    return render_template('page404.html', title="Страница не найдена", menu = menu)

if __name__ == "__main__":
        app.run(debug=True)