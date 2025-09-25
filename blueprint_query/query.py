import os
import re

from flask import Blueprint, render_template, request, current_app

from DB.sql_provider import SQLProvider
from DB.work_with_db import select_dict
from access import group_required, login_required

blueprint_query = Blueprint('bp_query', __name__, template_folder='templates', static_folder='static')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/menu_query', methods=['GET', 'POST'])
@group_required
@login_required
def query_menu():
    if request.method == 'GET':
        return render_template('menu_query.html')


@blueprint_query.route('/phone_number', methods=['GET', 'POST'])
@group_required
@login_required
def query_phone_number():
    if request.method == 'GET':
        return render_template('phone_number.html')
    else:
        phone_number = request.form.get('phone_number')
        if not phone_number or not phone_number.isdigit() or len(phone_number) != 11:
            return render_template('error.html')
        elif phone_number:
            _sql = provider.get('phone_number.sql', phone_number=phone_number)
        client = select_dict(current_app.config['db_config'], _sql)
        print(client)
        if client:
            title = 'Полученный результат'
            return render_template('dynamic_query.html', client=client, title=title)
        else:
            return render_template('error.html')


@blueprint_query.route('/adress', methods=['GET', 'POST'])
@group_required
@login_required
def query_adress():
    if request.method == 'GET':
        return render_template('adress.html')
    else:
        adress = request.form.get('adress')
        if adress:
            _sql = provider.get('adress.sql', adress=adress)
        elif not adress:
            return render_template('adress.html')
        client = select_dict(current_app.config['db_config'], _sql)
        if client:
            title = 'Полученный результат'
            return render_template('dynamic_query.html', client=client, title=title)
        else:
            return render_template('error.html')


@blueprint_query.route('/birthday', methods=['GET', 'POST'])
@group_required
@login_required
def query_birthday():
    if request.method == 'GET':
        return render_template("birthday.html")
    else:
        birthday = request.form.get('birthday')
        if birthday:
            pattern_str = r'^\d{4}-\d{2}-\d{2}$'
            if re.match(pattern_str, birthday):
                _sql = provider.get('birthday.sql',birthday=birthday)
        elif not birthday:
            return render_template("birthday.html")
        client = select_dict(current_app.config['db_config'], _sql)
        if client:
            title = 'Полученный результат'
            return render_template('dynamic_query.html', client=client, title=title)
        else:
            return render_template('error.html')


@blueprint_query.route('/surname', methods=['GET', 'POST'])
@group_required
@login_required
def query_surname():
    if request.method == 'GET':
        return render_template('surname.html')
    else:
        surname = request.form.get('surname')
        if surname:
            _sql = provider.get('surname.sql', surname=surname)
        elif not surname:
            return render_template('surname.html')
        client = select_dict(current_app.config['db_config'], _sql)
        if client:
            title = 'Полученный результат'
            return render_template('dynamic_query.html', client=client, title=title)
        else:
            return render_template('error.html')


@blueprint_query.route('/signing_date', methods=['GET', 'POST'])
@group_required
@login_required
def query_signing_date():
    if request.method == 'GET':
        return render_template("signing_date.html")
    else:
        signing_date = request.form.get('signing_date')
        if signing_date:
            pattern_str = r'^\d{4}-\d{2}-\d{2}$'
            if re.match(pattern_str, signing_date):
                _sql = provider.get('signing_date.sql',signing_date=signing_date)
        elif not signing_date:
            return render_template("signing_date.html")
        client = select_dict(current_app.config['db_config'], _sql)
        if client:
            title = 'Полученный результат'
            return render_template('dynamic_query.html', client=client, title=title)
        else:
            return render_template('error.html')


@blueprint_query.route('/termination_date', methods=['GET', 'POST'])
@group_required
@login_required
def query_termination_date():
    if request.method == 'GET':
        return render_template("termination_date.html")
    else:
        termination_date = request.form.get('termination_date')
        if termination_date:
            pattern_str = r'^\d{4}-\d{2}-\d{2}$'
            if re.match(pattern_str, termination_date):
                _sql = provider.get('termination_date.sql', termination_date=termination_date)
        elif not termination_date:
            return render_template("termination_date.html")
        client = select_dict(current_app.config['db_config'], _sql)
        if client:
            title = 'Полученный результат'
            return render_template('dynamic_query.html', client=client, title=title)
        else:
            return render_template('error.html')


@blueprint_query.route('/input', methods=['GET', 'POST'])
@group_required
@login_required
def query_index():
    if request.method == 'GET':
        return render_template('input_param.html')
    else:
        adress = request.form.get('adress')  # объект form - словарь, где ключ - название adress, извлекается методом get
        phone_number = request.form.get('phone_number')
        birthday = request.form.get('birthday')
        surname = request.form.get('surname')
        signing_date = request.form.get('signing_date')
        termination_date = request.form.get('termination_date')
        title = 'Полученный результат'

        if adress:
            return render_template('dynamic_query.html', client=adress, title=title)
        if phone_number:
            return render_template('dynamic_query.html', client=phone_number, title=title)
        if birthday:
            return render_template('dynamic_query.html', client=birthday, title=title)
        if surname:
            return render_template('dynamic_query.html', client=surname, title=title)
        if signing_date:
            return render_template('dynamic_query.html', client=signing_date, title=title)
        if termination_date:
            return render_template('dynamic_query.html', client=termination_date, title=title)
        else:
            return render_template('error.html')


@blueprint_query.route('/clients_and_bills')
@login_required
@group_required
def query_clients_and_bills():
    _sql = provider.get('clients_and_bills.sql')
    res = select_dict(current_app.config['db_config'], _sql)
    if res:
        return render_template('dynamic.html', result=res, key_list=res[0].keys())


@blueprint_query.route('/bills_with_no_transactions', methods=['GET', 'POST'])
@group_required
@login_required
def query_bills_with_no_transactions():
    if request.method == 'GET':
        return render_template("bills_with_no_transactions.html")
    else:
        bills_with_no_transactions = request.form.get('bills_with_no_transactions')
        #print(bills_with_no_transactions)
        if not bills_with_no_transactions:
            return render_template('bills_with_no_transactions.html', error='Отсутствуют входные данные')
        else:
            year = bills_with_no_transactions[0:4]
            month = bills_with_no_transactions[5:7]
            year_res = re.match("^\d{4}$", year)
            month_res = re.match("^\d{2}$", month)
            if (year_res is None or month_res is None):
                return render_template('bills_with_no_transactions.html', error='Неверные входные данные')
            year = int(year)
            month = int(month)
            if (year < 2000 or month < 1 or month > 12):
                return render_template('bills_with_no_transactions.html', error='Неверные входные данные')
            _sql = provider.get('bills_with_no_transactions.sql', year=year, month=month)

        client = select_dict(current_app.config['db_config'], _sql)
        print(client)
        if client:
            title = 'Полученный результат'
            return render_template('dynamic_no_bills.html', client=client, title=title)
        else:
            return render_template('error.html')


@blueprint_query.route('/bank_rate')
@login_required
@group_required
def query_bank_rate():
    _sql = provider.get('bank_rate.sql')
    res = select_dict(current_app.config['db_config'], _sql)
    if res:
        return render_template('dynamic.html', result=res, key_list=res[0].keys())
