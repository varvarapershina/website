from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session


# ОЦЕНИТЕ, ПОЖАЛУЙСТА, СТРОКИ В ДРУГИХ ФАЙЛАХ!!!

def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()


SqlAlchemyBase = orm.declarative_base()

__factory = None


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)


app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/', methods=['POST', 'GET'])
@app.route('/enter_game/', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        msg = ''
        return render_template('enter_game.html', msg='')
    elif request.method == 'POST':
        pas = request.form['password']
        name = request.form['username']
        user = User()
        db_sess = create_session()
        r = db_sess.query(User).filter_by(name=name).first()
        real_password = str(r.hashed_password)
        if check_password_hash(real_password, pas):
            return redirect('/site_apteka')
        return 'Неправильный пароль!'


@app.route('/new_person/', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        msg = ''
        return render_template('new_person.html', msg='')
    elif request.method == 'POST':
        em = request.form['email']
        pas = request.form['password']
        name = request.form['username']
        user = User()
        user.name = name
        user.email = em
        hash = generate_password_hash(pas)
        user.hashed_password = hash
        db_sess = create_session()
        db_sess.add(user)
        db_sess.commit()
        return redirect('/enter_game/')


@app.route('/about_us/')
def about_us():
    return render_template('about_us.html')


@app.route('/work_for_us/')
def work_for_us():
    return render_template('work_for_us.html')


@app.route('/site_apteka')
def apteka():
    return '''<!doctype html>
                <html lang="en">
                    <head>
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
                        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
                        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>

                        <title>Фармкомпания</title>

                        <style>
                            body {
                                background-color: LightSteelBlue;
                                border: 10px solid DarkSlateGrey;
                            }

                            h1 {
                                font-family: 'Arial', 'Verdana', sans-serif;
                                font-weight: 100;
                                color: Black;
                                height: 100
                                font-size: 40px;
                                font-size: 100%;
                                text-align: center;
                                line-height: 4em;
                                border: 10px solid DarkSlateGrey;
                                border-radius: 10px;
                                margin: 10px;
                            }

                            h2 {
                                color: Black;
                                text-align: center;
                            }

                            h3 {
                                color: Black;
                                text-align: center;
                            }

                            p {
                              margin: 10px;
                              padding: 10px;
                              font-size: 40px;
                              font-size: 100%;
                              line-height: 4em;
                            }

                            .markers {
                                color: DarkSlateGrey;
                                font-size: 20px;
                                margin: 30px;
                            }

                            * {box-sizing: border-box;}
                            form {
                              position: relative;
                              width: 700px;
                              margin: 10px 530px 20px;
                            }

                            input {
                              width: 100%;
                              height: 42px;
                              padding-left: 10px;
                              border: 2px solid Teal;
                              border-radius: 5px;
                              outline: none;
                              background: AliceBlue;
                              font-family: 'Arial', 'Verdana', sans-serif;
                              color: DimGrey;
                            }

                            button {
                              position: absolute;
                              top: 50;
                              right: 0px;
                              width: 60px;
                              height: 42px;
                              border: none;
                              background: Teal;
                              border-radius: 0 5px 5px 0;
                              cursor: pointer;
                            }

                            .ser-button:before {
                              content: "\f002";
                              font-family: FontAwesome;
                              font-size: 16px;
                              color: AliceBlue;
                            }
                            .container {
                              color: White
                              text-align: center
                              border-radius: 10px;
                              }

                            h1 {
                              font-family: 'Arial', 'Verdana', sans-serif;
                              font-weight: 200;
                              font-size: 40px;
                            }
                            .small-caps {
                              font-variant: small-caps;
                              font-style
                            }

                            h2 {
                              font-family: 'Arial', 'Verdana', sans-serif;
                              font-weight: 200;
                              font-size: 40px;
                            }

                            .small-caps {
                              font-variant: small-caps;
                              font-style
                            }

                            .main-subtitle {
                              font-family: 'Arial', 'Verdana', sans-serif;
                              font-weight: 100;
                              font-size: 25px;
                              font-variant: small-caps;
                            }

                            @import url('https://fonts.googleapis.com/css?family=Arimo');
                            .top-menu {
                              background: AliceBlue;
                              box-shadow: 3px 0 7px rgba(0,0,0,.3);
                              padding: 20px;
                            }

                            .top-menu:after {
                              content: "";
                              display: table;
                              clear: both;
                            }

                            .navbar-logo {display: inline-block;}
                            .menu-main {
                              list-style: none;
                              margin: 0;
                              padding: 0;
                              float: right;
                            }

                            .menu-main li {display: inline-block;}
                            .menu-main a {
                              text-decoration: none;
                              display: block;
                              position: relative;
                              line-height: 65px;
                              padding-left: 30px;
                              font-size: 35px;
                              letter-spacing: 2px;
                              font-family: 'Arial', 'Verdana', sans-serif;
                              font-weight: bold;
                              color: DarkSlateGrey;
                              transition:.3s linear;
                            }

                            .menu-main a:before {
                              content: "";
                              width: 9px;
                              height: 9px;
                              background: DarkSlateGrey;
                              position: absolute;
                              left: 50%;
                              transform: rotate(45deg) translateX(6.5px);
                              opacity: 0;
                              transition: .3s linear;
                            }

