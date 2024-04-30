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

                            .menu-main a:hover:before {opacity: 1;}
                            @media (max-width: 660px) {
                            .menu-main {
                              float: none;
                              padding-top: 20px;
                            }

                            .top-menu {
                              text-align: center;
                              padding: 20px 0 0 0;
                            }
                            
                            .menu-main a {padding: 0 10px;}
                            .menu-main a:before {transform: rotate(45deg) translateX(-6px);}
                            }

                            @media (max-width: 600px) {
                            .menu-main li {display: block;}
                            }

                            .card-container {
                              display: flex;
                              flex-wrap: wrap;
                              justify-content: center;
                              gap: 16px;
                              padding: 16px;
                            }

                            .card {
                              background-color: AliceBlue;
                              box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                              width: 300px;
                              border-radius: 10px;
                              overflow: hidden;
                              padding: 16px;
                            }

                            .card img {
                              width: 100%;
                              height: auto;
                            }

                            .card h3 {
                              margin-top: 16px;
                              margin-bottom: 10px;
                              font-style: italic;
                            }

                            .card p {
                              color: #777;
                            }
                        </style>

                    </head>
                    <body>
                        <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
                          <symbol id="check-circle-fill" fill="currentColor" viewBox="0 0 16 16">
                            <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
                          </symbol>
                          <symbol id="info-fill" fill="currentColor" viewBox="0 0 16 16">
                            <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm.93-9.412-1 4.705c-.07.34.029.533.304.533.194 0 .487-.07.686-.246l-.088.416c-.287.346-.92.598-1.465.598-.703 0-1.002-.422-.808-1.319l.738-3.468c.064-.293.006-.399-.287-.47l-.451-.081.082-.381 2.29-.287zM8 5.5a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/>
                          </symbol>
                          <symbol id="exclamation-triangle-fill" fill="currentColor" viewBox="0 0 16 16">
                            <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
                          </symbol>
                        </svg>
                        <nav class="top-menu">
                          <a class="navbar-logo" href=""><img src="https://yt3.googleusercontent.com/ytc/AOPolaT_Ladu1VMq4fJ6va2dpeQEdg1d9D0WFaUTX5jW=s900-c-k-c0x00ffffff-no-rj" alt="Лого"
                          style="display: block; width: 115px;"></a>
                          <ul class="menu-main">
                            <li><a href="http://127.0.0.1:8080/site_apteka">Главная</a></li>
                            <li><a href="http://127.0.0.1:8080/work_for_us/">Работа</a></li>
                            <li><a href="http://127.0.0.1:8080/about_us/">О нас</a></li>
                          </ul>
                        </nav>
                        <form>
                            <input type="text" placeholder="Поиск по сайту">
                            <button value="" title="Найти" alt="Найти" class="fa ser-button" type="submit">Найти</button>
                        </form>
                        <section class="main-section">
                            <div class="container">
                                <h1 class="small-caps">Добро пожаловать, сотрудник!</h1>
                                <p class="main-subtitle">Дороже лекарств может быть только здоровье...</p>
                            </div>

                        <div class="card-container">
                          <div class="card">
                            <img src="https://citatnica.ru/wp-content/uploads/2019/06/897701440575bfed599a8b0.89490139.jpg" alt="Image 1">
                            <h3>"Наша медицина двигается
                            вместе с такими компаниями"</h3>
                            <p>Ведущий специалист</p>
                          </div>

                          <div class="card">
                            <img src="https://fraufluger.ru/wp-content/uploads/2021/04/j_lqasli650.jpg" alt="Image 2">
                            <h3>"Хороший коллектив сотрудников"</h3>
                            <p>Сотрудник</p>
                          </div>

                          <div class="card">
                            <img src="https://mykaleidoscope.ru/x/uploads/posts/2022-09/1663177004_52-mykaleidoscope-ru-p-deti-v-vostorge-vkontakte-59.jpg" alt="Image 2">
                            <h3>"Спасибо! Ваше лекарство помогло
                            Моему ребенку!"</h3>
                            <p>Покупательница</p>
                          </div>
                        </div>

                        </section>
                        <div class="alert alert-success d-flex align-items-center" role="alert">
                          <svg class="bi flex-shrink-0 me-2" width="24" height="24" role="img" aria-label="Success:"><use xlink:href="#check-circle-fill"/></svg>
                          <div>
                            <h3 class="small-caps">Наша компания «Фармик» предоставляет лекарства для всех больниц города</h3>
                          </div>
                        </div>
                        <h2 class="small-caps">Мы известны такими лекарствами, как:</h2>

                        <div class="container">
                            <div id="myCarousel" class="carousel slide" data-ride="carousel">

                                <ol class="carousel-indicators">
                                    <li data-target="#myCarousel" data-slide-to="0" class="active"></li>
                                    <li data-target="#myCarousel" data-slide-to="1"></li>
                                    <li data-target="#myCarousel" data-slide-to="2"></li>
                                    <li data-target="#myCarousel" data-slide-to="3" class="active"></li>
                                    <li data-target="#myCarousel" data-slide-to="4"></li>
                                    <li data-target="#myCarousel" data-slide-to="5"></li>
                                    <li data-target="#myCarousel" data-slide-to="6" class="active"></li>
                                    <li data-target="#myCarousel" data-slide-to="7"></li>
                                    <li data-target="#myCarousel" data-slide-to="8"></li>
                                    <li data-target="#myCarousel" data-slide-to="9"></li>
                                </ol>

                                <div class="carousel-inner">
                                    <div class="item active">
                                        <img src="https://api.biocadless.com/uploads/biocadru/1689602248350.png" alt="Lekarstvo1" style="width:50%;">
                                        <div class="carousel-caption">
                                            <h3>Ковада</h3>
                                            <p>Онкологические заболевания</p>
                                            <form action="https://biocad.ru/products/autoimmune/tribuvia" target="_blank">
                                            <button class="btn btn-primary">На сайт...</button>
                                        </div>
                                    </div>

                                    <div class="item">
                                        <img src="https://api.biocadless.com/uploads/biocadru/1685451718152.png" alt="Lekarstvo2" style="width:50%;">
                                        <div class="carousel-caption">
                                            <h3>Инфликсимаб</h3>
                                            <p>Аутоиммунные заболевания</p>
                                            <form action="https://biocad.ru/products/autoimmune/infliksimab" target="_blank">
                                            <button class="btn btn-primary">На сайт...</button>
                                        </div>
                                    </div>

                                    <div class="item">
                                        <img src="https://api.biocadless.com/uploads/biocadru/1696842217764.png" alt="Lekarstvo3" style="width:50%;">
                                        <div class="carousel-caption">
                                            <h3>Платикад</h3>
                                            <p>Онкологические заболевания</p>
                                            <form action="https://biocad.ru/products/onco/platikad" target="_blank">
                                            <button class="btn btn-primary">На сайт...</button>
                                        </div>
                                    </div>

                                    <div class="item">
                                        <img src="https://api.biocadless.com/uploads/biocadru/1689602248658.png" alt="Lekarstvo4" style="width:50%;">
                                        <div class="carousel-caption">
                                            <h3>Пеметрексед</h3>
                                            <p>Онкологические заболевания</p>
                                            <form action="https://biocad.ru/products/onco/pemetreksed" target="_blank">
                                            <button class="btn btn-primary">На сайт...</button>
                                        </div>
                                    </div>

                                    <div class="item">
                                        <img src="https://api.biocadless.com/uploads/biocadru/1696842218256.png" alt="Lekarstvo5" style="width:50%;">
                                        <div class="carousel-caption">
                                            <h3>Бортезомиб</h3>
                                            <p>Онкологические заболевания</p>
                                            <form action="https://biocad.ru/products/onco/bortezomib" target="_blank">
                                            <button class="btn btn-primary">На сайт...</button>
                                        </div>
                                    </div>

                                    <div class="item">
                                        <img src="https://api.biocadless.com/uploads/biocadru/1709122602443.png" alt="Lekarstvo6" style="width:50%;">
                                        <div class="carousel-caption">
                                            <h3>Ацверис</h3>
                                            <p>Аутоиммунные заболевания</p>
                                            <form action="https://biocad.ru/products/autoimmune/acveris" target="_blank">
                                            <button class="btn btn-primary">На сайт...</button>
                                        </div>
                                    </div>

                                    <div class="item">
                                        <img src="https://api.biocadless.com/uploads/biocadru/1689602545557.png" alt="Lekarstvo7" style="width:50%;">
                                        <div class="carousel-caption">
                                            <h3>Гемцитар</h3>
                                            <p>Онкологические заболевания</p>
                                            <form action="https://biocad.ru/products/onco/gemcitar" target="_blank">
                                            <button class="btn btn-primary">На сайт...</button>
                                        </div>
                                    </div>

                                    <div class="item">
                                        <img src="https://api.biocadless.com/uploads/biocadru/1714115735680.png" alt="Lekarstvo8" style="width:50%;">
                                        <div class="carousel-caption">
                                            <h3>Трибувиа</h3>
                                            <p>Аутоиммунные заболевания</p>
                                            <form action="https://biocad.ru/products/autoimmune/tribuvia" target="_blank">
                                            <button class="btn btn-primary">На сайт...</button>
                                        </div>
                                    </div>

                                    <div class="item">
                                        <img src="https://api.biocadless.com/uploads/biocadru/1709122602447.png" alt="Lekarstvo9" style="width:50%;">
                                        <div class="carousel-caption">
                                            <h3>Нурдати</h3>
                                            <p>Онкологические заболевания</p>
                                            <form action="https://biocad.ru/products/onco/nurdati" target="_blank">
                                            <button class="btn btn-primary">На сайт...</button>
                                        </div>
                                    </div>

                                    <div class="item">
                                        <img src="https://api.biocadless.com/uploads/biocadru/1685451718654.png" alt="Lekarstvo10" style="width:50%;">
                                        <div class="carousel-caption">
                                            <h3>Фортека</h3>
                                            <p>Онкологические заболевания</p>
                                            <form action="https://biocad.ru/products/onco/forteka" target="_blank">
                                            <button class="btn btn-primary">На сайт...</button>
                                        </div>
                                    </div>
                                </div>

                                <a class="left carousel-control" href="#myCarousel" data-slide="prev">
                                    <span class="glyphicon glyphicon-chevron-left"></span>
                                    <span class="sr-only">Previous</span>
                                </a>

                                <a class="right carousel-control" href="#myCarousel" data-slide="next">
                                    <span class="glyphicon glyphicon-chevron-right"></span>
                                    <span class="sr-only">Next</span>
                                </a>
                            </div>
                        </div>

                        <h2>Наши основные партнеры:</h2>
                            <hr>
                            <ul class="markers">
                                <li><a href="https://pharmproject.com/">Фармпроект</a></li>
                                <li><a href="https://ns03.ru/">Северная звезда</a></li>
                                <li><a href="https://geropharm.ru/">Герофарм</a></li>
                            </ul>
                            <hr>

                        <h2>Наши контакты и адрес:</h2>

                        <p class="success-message"><a class="text-success" href="https://t.me/ne_liashka">Хамзина Неля</a></p>
                        <p class="success-message"><a class="text-success" href="https://t.me/varvarapershina">Першина Варвара</a></p>
                        <p class="success-message"><a class="text-success" href="tel:+79999999999">Контактный номер: +79999999999</a></p>

                        <div id="YMapsID"></div>
                        <script src="https://api-maps.yandex.ru/services/constructor/1.0/js/?um=constructor%3A276fec3c7cccade2d03b467149636659a41a5aa895d0e447399a3650d9d4d11d&amp;width=554&amp;height=401&amp;lang=ru_RU&amp;scroll=true"></script>
                        <script type="text/javascript">

                        <style type="text/css">
                            #YMapsID {
                                width: 520px;
                                height: 500px;
                            }
                        </style>

                    </body>
                </html>'''

if __name__ == '__main__':
    global_init("db/users.db")
    app.run(port=8080, host='127.0.0.1')