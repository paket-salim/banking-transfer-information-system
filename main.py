import json

from flask import Flask, render_template

from blueprint_auth.auth import blueprint_auth
from blueprint_query.query import blueprint_query
from blueprint_report.report import blueprint_report
from blueprint_transfer.transfer import blueprint_transfer

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

with open('data_files/db_config.json') as f:
    app.config['db_config'] = json.load(f)

with open('data_files/access.json', encoding='utf-8') as f:
    app.config['access_config'] = json.load(f)

with open('data_files/reports.json') as f:
    app.config['report_config'] = json.load(f)

with open('data_files/secret_key.json') as f:
    app.secret_key = json.load(f)['secret_key']


app.register_blueprint(blueprint_auth, url_prefix='/')
app.register_blueprint(blueprint_query, url_prefix='/query')
app.register_blueprint(blueprint_report, url_prefix='/report')
app.register_blueprint(blueprint_transfer, url_prefix='/transfer')


@app.route('/')
def main_menu():
    return render_template('main_menu.html')


@app.route('/auth')
def auth():
    return render_template('auth.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002, debug=True)
