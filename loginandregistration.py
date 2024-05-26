#pip install flask
#pip install Werkzeug
#pip install requests
#сначала запустите файл db.py(создание базы данных пользователей)

from flask import Flask, request, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)

@app.route('/authorization', methods=['GET', 'POST'])
def form_authorization():
   if request.method == 'POST':
       Login = request.form.get('username')
       Password = request.form.get('password')

       db_lp = sqlite3.connect('storage.db')
       cursor_db = db_lp.cursor()
       cursor_db.execute(('''SELECT password FROM passwords
                            WHERE login = '{}';''').format(Login))
       pas = cursor_db.fetchall()

       cursor_db.close()
       try:
           if check_password_hash(pas[0][0], Password) == False:
               return render_template('login.html', msg = 'Пароль или логин неверный')
       except:
           return render_template('login.html', msg = 'Пароль или логин неверный')

       db_lp.close()
       return render_template('login.html', msg = 'Вы успешно авторизированы')

   return render_template('login.html', msg = '')



@app.route('/registration', methods=['GET', 'POST'])
def form_registration():

   if request.method == 'POST':
       Login = request.form.get('username')
       Password = request.form.get('password')
       Password1 = request.form.get('password1')

       if Password1 == Password:
           Password = generate_password_hash(request.form.get('password'))
           db_lp = sqlite3.connect('storage.db')
           cursor_db = db_lp.cursor()
           sql_insert = '''INSERT INTO passwords VALUES('{}','{}');'''.format(Login, Password)
           cursor_db.execute(sql_insert)
           cursor_db.close()
           db_lp.commit()
           db_lp.close()
           return render_template('register.html', msg = 'Вы успешно зарегистрировались')
       else:
           return render_template('register.html', msg = 'Пароли не совпали. Повторите попытку')

   return render_template('register.html', msg = '')


@app.route('/homepage', methods=['GET', 'POST'])
def form_homepage():
    return render_template('homepage.html')


if __name__ == "__main__":
 app.run()