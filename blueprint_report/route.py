import os
from flask import render_template, request, Blueprint, redirect, url_for, current_app
from db_work import call_proc, select, select_dict, insert
from sql_provider import SQLProvider
from access import group_required

blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_report.route('/', methods=['GET'])
@group_required
def start_report():
    report_url = current_app.config['report_url']
    report_list = current_app.config['report_list']
    return render_template('menu_report.html', report_list=report_list, endcoding='UTF-8', report_url=report_url)


@blueprint_report.route('/create_rep/1', methods=['GET', 'POST'])
@group_required
def create_rep1():
    if request.method == 'GET':
        return render_template('report_base.html')
    else:
        input_year = request.form.get('input_year')
        input_month = request.form.get('input_month')
        if input_year and input_month:
            _sql = provider.get('summ_report.sql', input_month=input_month, input_year=input_year)
            product_result = select_dict(current_app.config['db_config'], _sql)
            if len(product_result) != 0:
                return render_template('report_base.html', message='Отчет уже существует')
            else:
                    _sql = provider.get('info_of_sale.sql', input_year=input_year, input_month=input_month)
                    info_result = select_dict(current_app.config['db_config'], _sql)
                    if len(info_result) != 0:
                        res = call_proc(current_app.config['db_config'], 'summ', int(input_year), int(input_month))
                        return render_template('report_base.html', message='Отчет создан')
                    else:
                        return render_template('report_base.html', message='Продаж в этом месяце не было')

        else:
            return render_template('report_base.html', message='Повторите ввод')


@blueprint_report.route('/view_rep/1', methods=['GET', 'POST'])
@group_required
def view_rep1():
    if request.method == 'GET':
        return render_template('report_base.html')
    else:
        input_year = request.form.get('input_year')
        input_month = request.form.get('input_month')
        if input_year and input_month:
            _sql = provider.get('info_of_sale.sql', input_year=input_year, input_month=input_month)
            info_result = select_dict(current_app.config['db_config'], _sql)
            if len(info_result) == 0:
                return render_template('report_base.html', message='Продаж в этом месяце не было')
            else:
                _sql = provider.get('summ_report.sql', input_month=input_month, input_year=input_year)
                product_result, schema = select(current_app.config['db_config'], _sql)

                if len(product_result) == 0:
                    return render_template('report_base.html', message='Перед просмотром отчета требуется его создать')
                else:
                    list_name=['Сумма', 'Количество проданных товаров', 'Месяц создания отчета', 'Год создания отчета']
                    return render_template('report_base.html', schema=list_name, result=product_result)
        else:
            return render_template('report_base.html', error_message='Повторите ввод')


@blueprint_report.route('/delete_rep/1', methods=['GET', 'POST'])
@group_required
def delete_rep1():
    if request.method == 'GET':
        return render_template('report_base.html')
    else:
        input_year = request.form.get('input_year')
        input_month = request.form.get('input_month')
        if input_year and input_month:
            _sql = provider.get('check_for_report.sql', input_year=input_year, input_month=input_month)
            info_result = select_dict(current_app.config['db_config'], _sql)
            if len(info_result) == 0:
                return render_template('report_base.html', message='Отчёта на этот месяц еще нет')
            else:
                _sql = provider.get('delete.sql', input_month=input_month, input_year=input_year)
                insert(current_app.config['db_config'], _sql)
                return render_template('report_base.html', message='Отчет удален')
        else:
            return render_template('report_base.html', message='Повторите ввод')


@blueprint_report.route('/create_rep/2', methods=['GET', 'POST'])
@group_required
def create_rep2():
    if request.method == 'GET':
        return render_template('report_base.html')
    else:
        input_year = request.form.get('input_year')
        input_month = request.form.get('input_month')
        if input_year and input_month:
            _sql = provider.get('categories_report.sql', input_month=input_month, input_year=input_year)
            product_result = select_dict(current_app.config['db_config'], _sql)
            if len(product_result) != 0:
                return render_template('report_base.html', message='Отчет уже существует')
            else:
                    _sql = provider.get('info_of_sale.sql', input_year=input_year, input_month=input_month)
                    info_result = select_dict(current_app.config['db_config'], _sql)
                    if len(info_result) != 0:
                        call_proc(current_app.config['db_config'], 'categories', int(input_year), int(input_month))
                        return render_template('report_base.html', message='Отчет создан')
                    else:
                        return render_template('report_base.html', message='Продаж в этом месяце не было')

        else:
            return render_template('report_base.html', message='Повторите ввод')


@blueprint_report.route('/view_rep/2', methods=['GET', 'POST'])
@group_required
def view_rep2():
    if request.method == 'GET':
        return render_template('report_base.html')
    else:
        input_year = request.form.get('input_year')
        input_month = request.form.get('input_month')
        if input_year and input_month:
            _sql = provider.get('info_of_sale.sql', input_year=input_year, input_month=input_month)
            info_result = select_dict(current_app.config['db_config'], _sql)
            if len(info_result) == 0:
                return render_template('report_base.html', message='Продаж в этом месяце не было')
            else:
                _sql = provider.get('categories_report.sql', input_month=input_month, input_year=input_year)
                product_result, schema = select(current_app.config['db_config'], _sql)

                if len(product_result) == 0:
                    return render_template('report_base.html', message='Перед просмотром отчета требуется его создать')
                else:
                    list_name=['Категория', 'Количество проданных товаров', "Cумма", 'Месяц создания отчета', 'Год создания отчета']
                    return render_template('report_base.html', schema=list_name, result=product_result)
        else:
            return render_template('report_base.html', error_message='Повторите ввод')


@blueprint_report.route('/delete_rep/2', methods=['GET', 'POST'])
@group_required
def delete_rep2():
    if request.method == 'GET':
        return render_template('report_base.html')
    else:
        input_year = request.form.get('input_year')
        input_month = request.form.get('input_month')
        if input_year and input_month:
            _sql = provider.get('check_cat_report.sql', input_year=input_year, input_month=input_month)
            info_result = select_dict(current_app.config['db_config'], _sql)
            if len(info_result) == 0:
                return render_template('report_base.html', message='Отчёта на этот месяц еще нет')
            else:
                _sql = provider.get('delete_cat.sql', input_month=input_month, input_year=input_year)
                insert(current_app.config['db_config'], _sql)
                return render_template('report_base.html', message='Отчет удален')
        else:
            return render_template('report_base.html', message='Повторите ввод')
