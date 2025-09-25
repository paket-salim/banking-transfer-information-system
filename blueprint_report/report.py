import os
import re

from flask import Blueprint, render_template, request, current_app

from DB.sql_provider import SQLProvider
from DB.work_with_db import select_dict, call_proc
from access import group_required, login_required

blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_report.route('/work')
@login_required
@group_required
def work_with_reports():
    config = current_app.config['report_config']
    print('config.keys() = ', config.keys())
    return render_template('report_menu.html', conf=config, key_list=config.keys())


@blueprint_report.route('/for_date/<proc>/<sql>', methods=['GET', 'POST'])
@login_required
@group_required
def create_report(proc, sql):
    if request.method == 'GET':
        return render_template('input_param_report.html')
    else:
        date_ = request.form.get('date')
        if not date_:
            return render_template('input_param_report.html', error='Недостаточно входных данных')
        else:
            year_ = date_[0:4]
            month_ = date_[5:7]
            year_res = re.match("^\d{4}$",year_)
            month_res = re.match("^\d{2}$", month_)
            if (year_res is None or month_res is None):
                return render_template('input_param_report.html', error='Неверные входные данные')
            year_ = int(year_)
            month_ = int(month_)
            if (year_ < 2000 or 1 > month_ or month_ > 12):
                return render_template('input_param_report.html', error='Неверные входные данные')
            _sql = provider.get(sql, month_=month_, year_=year_)
            res = select_dict(current_app.config['db_config'], _sql)
            print('res1 =', res)
            if not res:
                temp = call_proc(current_app.config['db_config'], proc, year_, month_)
                _sql = provider.get(sql, month_=month_, year_=year_)
                res = select_dict(current_app.config['db_config'], _sql)
                print('res2 =', res)
                if res:
                    return render_template('report.html', sql=sql, msg='Отчёт успешно создан',
                                           y=year_, m=month_)
                else:
                    return render_template('input_param_report.html',
                                           error='Невозможно создать отчёт за указанный месяц. Недостаточно данных')
            else:
                return render_template('report.html', sql=sql, msg='Отчёт уже присутствует',
                                       y=year_, m=month_)


@blueprint_report.route('/report_show/<sql>', methods=['GET', 'POST'])
@login_required
@group_required
def report_show(sql):
    title = 'Отчёт найден'
    print('request.args =', request.args)
    if 'year' in request.args.keys() and 'month' in request.args.keys():
        _sql = provider.get(sql, month_=request.args['month'], year_=request.args['year'])
        res = select_dict(current_app.config['db_config'], _sql)
        if res:
            return render_template('dynamic.html', title=title, result=res, key_list=res[0].keys())
    if request.method == 'GET':
        return render_template('input_param_report.html')
    else:
        date_ = request.form.get('date')
        if not date_:
            return render_template('input_param_report.html', error='Недостаточно входных данных')
        else:
            year_ = date_[0:4]
            month_ = date_[5:7]
            year_res = re.match("^\d{4}$", year_)
            month_res = re.match("^\d{2}$", month_)
            if (year_res is None or month_res is None):
                return render_template('input_param_report.html', error='Неверные входные данные')
            year_ = int(year_)
            month_ = int(month_)
            if (year_ < 2000 or 1 > month_ > 12):
                return render_template('input_param_report.html', error='Неверные входные данные')
            _sql = provider.get(sql, month_=month_, year_=year_)
            res = select_dict(current_app.config['db_config'], _sql)
            print(res)
            if res:
                return render_template('dynamic.html', result=res, key_list=res[0].keys())
            else:
                return render_template('input_param_report.html',
                                       error='Отчёт по данному периоду не существует')
