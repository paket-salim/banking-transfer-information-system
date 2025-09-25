import os
from datetime import datetime

from flask import Blueprint, render_template, request, current_app, session, redirect, url_for

from DB.DBconn import DBContextManager
from DB.sql_provider import SQLProvider
from DB.work_with_db import select_dict, insert_into_db
from access import group_required, login_required

blueprint_transfer = Blueprint('bp_transfer', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_transfer.route("/", methods=['GET', 'POST'])
@group_required
@login_required
def transfer():
    if request.method == 'GET':
        db_config = current_app.config['db_config']
        user_id = session.get('user_id')

        sql_get_accounts = provider.get('get_accounts.sql', user_id=user_id)
        accounts = select_dict(db_config, sql_get_accounts, user_id)

        sql_get_accounts2 = provider.get('get_accounts2.sql', user_id=user_id)
        accounts2 = select_dict(db_config, sql_get_accounts2, user_id)

        return render_template('transfer.html', accounts=accounts, accounts2=accounts2)

    elif request.method == 'POST':
        db_config = current_app.config['db_config']

        account_from = int(request.form['account_from'])
        print('account_from =', account_from)
        account_to = int(request.form['account_to'])
        print('account_to =', account_to)
        amount = float(request.form['amount'])
        print('amount =', amount)

        if account_from == account_to:
            error_message = 'Вы не можете перевести средства на тот же самый счет'
            return render_template('transfer.html', error_message=error_message)

        sql_get_rate = provider.get('get_rate.sql', account_from=account_from, account_to=account_to)
        rate_result = select_dict(db_config, sql_get_rate)
        if not rate_result:
            return 'Exchange rate not found'
        exchange_rate = float(rate_result[0]['rate'])
        print('exchange_rate =', exchange_rate)
        amount_received = amount * exchange_rate

        sql_get_currency = provider.get('get_currency.sql', account_from=account_from)
        currency_result = select_dict(db_config, sql_get_currency)
        if not currency_result:
            return 'currency not found'
        currency = currency_result[0]['currency']
        print('currency =', currency)

        with DBContextManager(db_config) as cursor:
            if not cursor:
                return 'Error connecting to the database'
            try:
                current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Создание записи в истории переводов
                sql_insert_transfer_history = provider.get('insert_transfer_history.sql', amount=amount,
                                                           amount_received=amount_received, exchange_rate=exchange_rate,
                                                           current_date=current_date, account_from=account_from,
                                                           account_to=account_to)
                insert_into_db(db_config, sql_insert_transfer_history)
                print('В таблице transfer_history добавлена строка о переводе в', current_date)

                # Обновление остатков на счетах
                sql_debit = provider.get('debit_account.sql', account_from=account_from, amount=amount,
                                         new_balance_date=current_date)
                insert_into_db(db_config, sql_debit)
                print('В таблице bill обновлён остаток на счете-отправителе', account_from)

                sql_credit = provider.get('credit_account.sql', account_to=account_to,
                                          amount_received=amount_received, new_balance_date=current_date)
                insert_into_db(db_config, sql_credit)
                print('В таблице bill обновлён остаток на счете-получателе', account_to)

                # Получение информации о счетах для вывода на странице transfer_success.html
                sql_get_updated_balance = provider.get('get_updated_balance.sql', account_from=account_from,
                                                       account_to=account_to)
                updated_balance_result = select_dict(db_config, sql_get_updated_balance)
                if not updated_balance_result:
                    return 'Error retrieving updated balance'

                return render_template("transfer_success.html",
                                       updated_balance_result=updated_balance_result, amount=amount, currency=currency)

            except Exception as e:
                error_message = f"An error occurred: {str(e)}"
                print('Exception error')
                return render_template('transfer.html', error_message=error_message)

    return render_template('transfer.html')


@blueprint_transfer.route("/transfer_success")
@group_required
@login_required
def transfer_success():
    bill_a = request.args.get('bill_a')
    bill_b = request.args.get('bill_b')
    amount = request.args.get('amount')
    return render_template("transfer_success.html", bill_a=bill_a, bill_b=bill_b, amount=amount)


@blueprint_transfer.route('/sec')
@login_required
@group_required
def menu():
    session.pop('transfer')
    return redirect(url_for('main_menu'))
