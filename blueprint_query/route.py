import os

from flask import Blueprint, request, render_template, current_app
from access import group_required
from db_work import select
from sql_provider import SQLProvider

blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_query.route('/queries', methods=['GET', 'POST'])
@group_required
def queries():
    if request.method == 'GET':
        return render_template('product_form.html')
    else:
        input_product = request.form.get('product_name')
        if input_product:
            _sql = provider.get('product.sql', input_product=input_product)
            product_result, schema = select(current_app.config['db_config'], _sql)
            if len(product_result) != 0:
                return render_template('product_form.html', schema=schema, result=product_result)
            else:
                return render_template('product_form.html', message="Ничего не найдено")
        else:
            return render_template('product_form.html', error="Ошибка. Повторите запрос!")
