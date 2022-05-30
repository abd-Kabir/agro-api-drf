import calendar
from copy import deepcopy
from datetime import datetime
from dateutil.relativedelta import relativedelta

from apps.leasing_agreem.models import LeasingAgreement
from apps.payment_graph.models import PaymentTable
from config.utils.date_utils import check_days_year


def get_order_data(queryset, data):
    leasing_agreem = LeasingAgreement.objects.filter(order_model=queryset[data].id)[0]
    tech_data = {
        'id': queryset[data].technique.id,
        'name': queryset[data].technique.name.name,
        'model': queryset[data].technique.model,
        'price': queryset[data].technique.price,
        'number_of_techs': leasing_agreem.number_of_techs,
        'yearly_leasing_percent': queryset[data].technique.yearly_leasing_percent,
        'subsidy': queryset[data].technique.subsidy,
        'leasing_term': queryset[data].technique.leasing_term,
        'prepaid_percent': queryset[data].technique.prepaid_percent,
        'contract_price': leasing_agreem.contract_price
    }
    return tech_data


def get_leasing_data(queryset, data):
    leasing_data = {
        'technique': {
            'id': queryset[data].order_model.technique.id,
            'name': queryset[data].order_model.technique.name.name,
            'model': queryset[data].order_model.technique.model,
            'price': queryset[data].order_model.technique.price,
            'yearly_leasing_percent': queryset[data].order_model.technique.yearly_leasing_percent,
            'subsidy': queryset[data].order_model.technique.subsidy,
            'leasing_term': queryset[data].order_model.technique.leasing_term,
            'prepaid_percent': queryset[data].order_model.technique.prepaid_percent
        },
        'order': {
            'order_num': queryset[data].order_model.order_num,
            'order_date': queryset[data].order_model.order_date
        }
    }
    return leasing_data


def get_guarantee_data(queryset, data, page):
    if page == 1:
        guarantee_data = {
            'leasing': {
                'id': queryset[data].leasing_agreem.id,
                'leasing_num': queryset[data].leasing_agreem.leasing_num,
                'leasing_date': queryset[data].leasing_agreem.leasing_date
            },
            'technique': {
                'id': queryset[data].leasing_agreem.order_model.technique.id,
                'name': queryset[data].leasing_agreem.order_model.technique.name.name,
                'model': queryset[data].leasing_agreem.order_model.technique.model,
                'price': queryset[data].leasing_agreem.order_model.technique.price,
                'contract_price': queryset[data].leasing_agreem.contract_price,
                'number_of_techs': queryset[data].leasing_agreem.number_of_techs
            },
            'guarantee': {
                'id': queryset[data].id,
                'guarantors_signed_count': queryset[data].guarantors_signed_count
            }
        }
    else:
        guarantee_data = {
            'leasing': {
                'id': queryset[data].leasing_agreem.id,
                'contract_price': queryset[data].leasing_agreem.contract_price,
                'lessor_sign': queryset[data].leasing_agreem.lessor_sign,
                'lessee_sign': queryset[data].leasing_agreem.lessee_sign,
                'guarantor_sign': queryset[data].leasing_agreem.guarantor_sign,
            },
            'order': {
                'order_num': queryset[data].leasing_agreem.order_model.order_num,
                'order_date': queryset[data].leasing_agreem.order_model.order_date
            },
            'guarantee': {
                'id': queryset[data].id,
                'guarantor': queryset[data].guarantor
            }
        }
    return guarantee_data


# def get_payment_graph_data(queryset, data):
#     payment_graph_data = {
#         'id': queryset[data].id,
#         'name': queryset[data].act.leasing_agreem.order_model.technique.name.name,
#         'model': queryset[data].act.leasing_agreem.order_model.technique.model,
#         'price': queryset[data].act.leasing_agreem.order_model.technique.price,
#         'yearly_leasing_percent': queryset[data].act.leasing_agreem.order_model.technique.yearly_leasing_percent,
#         'leasing_term': queryset[data].act.leasing_agreem.order_model.technique.leasing_term,
#         'prepaid_percent': queryset[data].act.leasing_agreem.order_model.technique.prepaid_percent,
#         'prepaid_price': queryset[data].act.leasing_agreem.order_model.technique.prepaid_price,
#         'contract_price': queryset[data].act.leasing_agreem.contract_price,
#         'act_date': queryset[data].act.act_date,
#         'table': [{}]
#     }
#     technique_price = queryset[data].act.leasing_agreem.order_model.technique.price * queryset[
#         data].act.leasing_agreem.number_of_techs
#     yearly_leasing_percent = queryset[data].act.leasing_agreem.order_model.technique.yearly_leasing_percent
#     leasing_term = queryset[data].act.leasing_agreem.order_model.technique.leasing_term
#     # leasing_term = 5
#     prepaid_price = queryset[data].act.leasing_agreem.order_model.technique.prepaid_price
#     starting_residual_amount = technique_price - prepaid_price
#     start_payment_day = queryset[data].act.act_date
#     source_start_payment_day = deepcopy(queryset[data].act.act_date)
#     first_month_day = calendar.monthrange(start_payment_day.year, start_payment_day.month)[1] - start_payment_day.day
#     last_payment_day = start_payment_day.replace(day=calendar.monthrange(start_payment_day.year,
#                                                                          start_payment_day.month)[1])
#     payment_graph_data['table'][0]['days_count'] = first_month_day
#
#     all_days_count = 0
#     # Count of all leasing_term - months
#     for i in range(1, leasing_term + 1):
#         start_payment_day = start_payment_day + relativedelta(months=1)
#         start_payment_day = start_payment_day.replace(day=calendar.monthrange(start_payment_day.year,
#                                                                               start_payment_day.month)[1])
#         all_days_count += start_payment_day.day
#     all_days_count += first_month_day
#     quarterly_lease_term_part_of_value = starting_residual_amount / all_days_count * first_month_day
#     quarterly_percent_lease_term_payment = (yearly_leasing_percent * starting_residual_amount / check_days_year(
#         datetime.now()) * first_month_day) / 100
#     quarterly_lease_term_payment = quarterly_lease_term_part_of_value + quarterly_percent_lease_term_payment
#
#     payment_graph_data['table'][0]['residual_amount'] = starting_residual_amount
#     payment_graph_data['table'][0]['date'] = last_payment_day.strftime('%d.%m.%Y')
#     payment_graph_data['table'][0]['quarterly_lease_term_part_of_value'] = quarterly_lease_term_part_of_value
#     payment_graph_data['table'][0]['quarterly_percent_lease_term_payment'] = quarterly_percent_lease_term_payment
#     payment_graph_data['table'][0]['quarterly_lease_term_payment'] = quarterly_lease_term_payment
#
#     for data in range(1, leasing_term + 1):
#         source_start_payment_day += relativedelta(months=1)
#         source_start_payment_day = source_start_payment_day.replace(day=calendar.monthrange(
#             source_start_payment_day.year,
#             source_start_payment_day.month)[1])
#         residual_amount = payment_graph_data['table'][data - 1]['residual_amount'] - \
#             payment_graph_data['table'][data - 1]['quarterly_lease_term_part_of_value']
#         quarterly_lease_term_part_of_value = starting_residual_amount / all_days_count * source_start_payment_day.day
#         quarterly_percent_lease_term_payment = residual_amount * yearly_leasing_percent / \
#             (check_days_year(source_start_payment_day)) * \
#             source_start_payment_day.day
#         quarterly_lease_term_payment = quarterly_lease_term_part_of_value + quarterly_percent_lease_term_payment
#
#         data_storage = {'residual_amount': residual_amount,
#                         'date': source_start_payment_day.strftime('%d.%m.%Y'),
#                         'days_count': source_start_payment_day.day,
#                         'quarterly_lease_term_part_of_value': quarterly_lease_term_part_of_value,
#                         'quarterly_percent_lease_term_payment': quarterly_percent_lease_term_payment,
#                         'quarterly_lease_term_payment': quarterly_lease_term_payment}
#         payment_graph_data['table'].append(data_storage)
#     return payment_graph_data
def get_payment_table_data(queryset, data):
    technique_price = queryset.act.leasing_agreem.order_model.technique.price * \
                      queryset.act.leasing_agreem.number_of_techs
    yearly_leasing_percent = queryset.act.leasing_agreem.order_model.technique.yearly_leasing_percent
    leasing_term = queryset.act.leasing_agreem.order_model.technique.leasing_term
    # leasing_term = 5
    prepaid_price = queryset.act.leasing_agreem.order_model.technique.prepaid_price
    starting_residual_amount = technique_price - prepaid_price
    start_payment_day = queryset.act.act_date
    source_start_payment_day = deepcopy(queryset.act.act_date)
    first_month_day = calendar.monthrange(start_payment_day.year, start_payment_day.month)[1] - start_payment_day.day
    last_payment_day = start_payment_day.replace(day=calendar.monthrange(start_payment_day.year,
                                                                         start_payment_day.month)[1])
    source_first_month_day = deepcopy(first_month_day)

    all_days_count = 0
    # Count of all leasing_term - months
    for i in range(1, leasing_term + 1):
        start_payment_day = start_payment_day + relativedelta(months=1)
        start_payment_day = start_payment_day.replace(day=calendar.monthrange(start_payment_day.year,
                                                                              start_payment_day.month)[1])
        all_days_count += start_payment_day.day
    all_days_count += first_month_day
    quarterly_lease_term_part_of_value = starting_residual_amount / all_days_count * first_month_day
    quarterly_percent_lease_term_payment = (yearly_leasing_percent * starting_residual_amount / check_days_year(
        datetime.now()) * first_month_day) / 100
    quarterly_lease_term_payment = quarterly_lease_term_part_of_value + quarterly_percent_lease_term_payment
    payment_graph_data = {
        'table': [{
            'residual_amount': starting_residual_amount,
            'date': last_payment_day,
            'days_count': source_first_month_day,
            'quarterly_lease_term_part_of_value': quarterly_lease_term_part_of_value,
            'quarterly_percent_lease_term_payment': quarterly_percent_lease_term_payment,
            'quarterly_lease_term_payment': quarterly_lease_term_payment
        }]
    }
    PaymentTable.objects.create(residual_amount=starting_residual_amount,
                                date=last_payment_day,
                                days_count=source_first_month_day,
                                quarterly_lease_term_part_of_value=quarterly_lease_term_part_of_value,
                                quarterly_percent_lease_term_payment=quarterly_percent_lease_term_payment,
                                quarterly_lease_term_payment=quarterly_lease_term_payment,
                                payment_graph=queryset,
                                is_paid=0)
    objs = []
    for data in range(1, leasing_term + 1):
        source_start_payment_day += relativedelta(months=1)
        source_start_payment_day = source_start_payment_day.replace(day=calendar.monthrange(
            source_start_payment_day.year,
            source_start_payment_day.month)[1])
        residual_amount = payment_graph_data['table'][data - 1]['residual_amount'] - \
            payment_graph_data['table'][data - 1]['quarterly_lease_term_part_of_value']
        quarterly_lease_term_part_of_value = starting_residual_amount / all_days_count * source_start_payment_day.day
        quarterly_percent_lease_term_payment = residual_amount * yearly_leasing_percent / \
            (check_days_year(source_start_payment_day)) * \
            source_start_payment_day.day
        quarterly_lease_term_payment = quarterly_lease_term_part_of_value + quarterly_percent_lease_term_payment

        data_storage = {'residual_amount': residual_amount,
                        'date': source_start_payment_day,
                        'days_count': source_start_payment_day.day,
                        'quarterly_lease_term_part_of_value': quarterly_lease_term_part_of_value,
                        'quarterly_percent_lease_term_payment': quarterly_percent_lease_term_payment,
                        'quarterly_lease_term_payment': quarterly_lease_term_payment}
        payment_graph_data['table'].append(data_storage)
        obj = PaymentTable(residual_amount=residual_amount,
                           date=source_start_payment_day,
                           days_count=source_start_payment_day.day,
                           quarterly_lease_term_part_of_value=quarterly_lease_term_part_of_value,
                           quarterly_percent_lease_term_payment=quarterly_percent_lease_term_payment,
                           quarterly_lease_term_payment=quarterly_lease_term_payment,
                           payment_graph=queryset,
                           is_paid=0)
        objs.append(obj)
    PaymentTable.objects.bulk_create(objs)

    return payment_graph_data
