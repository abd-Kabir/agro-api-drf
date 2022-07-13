import calendar
from copy import deepcopy
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Count, Sum

from apps.leasing_agreem.models import LeasingAgreement
from apps.orders.models import Order
from apps.payment_graph.models import PaymentTable
from config.utils.date_utils import check_days_year


# COMPANY SIDE
def get_order_company_province_data(queryset, data):
    order = Order.objects.filter(district__region_id_id=queryset[data].id)
    technics_count = order.aggregate(tech_count=Sum('expertassessment__leasingagreement__number_of_techs'))[
        'tech_count']
    tech_price_sum = order.aggregate(tech_price_sum=Sum('technique__price'))['tech_price_sum']
    contract_price_sum = order.aggregate(contract_price_sum=Sum('expertassessment__leasingagreement__contract_price'))[
        'contract_price_sum']
    order_company_data = {
        'id': queryset[data].id,
        'province': queryset[data].name,
        'order_count': order.count(),
        'tech_count': technics_count,
        'tech_price_sum': tech_price_sum,
        'contract_price_sum': contract_price_sum
    }
    return order_company_data


def get_order_company_district_data(queryset, data):
    order = Order.objects.filter(district_id=queryset[data].id)
    technics_count = order.aggregate(tech_count=Sum('expertassessment__leasingagreement__number_of_techs'))[
        'tech_count']
    tech_price_sum = order.aggregate(tech_price_sum=Sum('technique__price'))['tech_price_sum']
    contract_price_sum = order.aggregate(contract_price_sum=Sum('expertassessment__leasingagreement__contract_price'))[
        'contract_price_sum']
    order_company_data = {
        'id': queryset[data].id,
        'district': queryset[data].name,
        'order_count': order.count(),
        'tech_count': technics_count,
        'tech_price_sum': tech_price_sum,
        'contract_price_sum': contract_price_sum
    }
    return order_company_data


def get_order_company_data(queryset, data):
    order_company_data = {
        'id': queryset[data].id,
        'order_num': queryset[data].order_num,
        'order_date': queryset[data].order_date,
        'technique': {
            'id': queryset[data].technique.id,
            'name': queryset[data].technique.name.name,
            'model': queryset[data].technique.model,
            'number_of_techs': queryset[data].expertassessment_set.first().leasingagreement_set.first().number_of_techs,
            'price': queryset[data].technique.price,
            'yearly_leasing_percent': queryset[data].technique.yearly_leasing_percent,
            'subsidy': queryset[data].technique.subsidy,
            'leasing_term': queryset[data].technique.leasing_term,
            'prepaid_percent': queryset[data].technique.prepaid_percent,
            'contract_price': queryset[data].expertassessment_set.first().leasingagreement_set.first().contract_price,
        },
        'expert_assessment': {
            'id': queryset[data].expertassessment_set.first().id,
            'expert_assessment_num': queryset[data].expertassessment_set.first().expert_assessment_num,
            'expert_assessment_date': queryset[data].expertassessment_set.first().expert_assessment_date,
        }
    }
    return order_company_data


def get_expert_a_company_data(queryset, data):
    expert_assessment_company_data = {
        'id': queryset[data].id,
        'order_num': queryset[data].order_model.order_num,
        'order_date': queryset[data].order_model.order_date,
        'expert_assessment_date': queryset[data].expert_assessment_date
    }
    return expert_assessment_company_data


def get_guarantee_company_province_data(queryset, data):
    leasing_agreem = LeasingAgreement.objects.filter(
        expert_assessment__order_model__district__region_id_id=queryset[data].id)
    technics_count = leasing_agreem.aggregate(tech_count=Sum('number_of_techs'))['tech_count']
    tech_price_sum = leasing_agreem.aggregate(tech_price_sum=Sum('expert_assessment__order_model__technique__price'))[
        'tech_price_sum']
    contract_price_sum = leasing_agreem.aggregate(contract_price_sum=Sum('contract_price'))['contract_price_sum']
    guarantee_company_data = {
        'id': queryset[data].id,
        'province': queryset[data].name,
        'leasing_count': leasing_agreem.count(),
        'tech_count': technics_count,
        'tech_price_sum': tech_price_sum,
        'contract_price_sum': contract_price_sum
    }
    return guarantee_company_data


def get_guarantee_company_district_data(queryset, data):
    leasing_agreem = LeasingAgreement.objects.filter(expert_assessment__order_model__district_id=queryset[data].id)
    technics_count = leasing_agreem.aggregate(tech_count=Sum('number_of_techs'))['tech_count']
    tech_price_sum = leasing_agreem.aggregate(tech_price_sum=Sum('expert_assessment__order_model__technique__price'))[
        'tech_price_sum']
    contract_price_sum = leasing_agreem.aggregate(contract_price_sum=Sum('contract_price'))['contract_price_sum']
    guarantee_company_data = {
        'id': queryset[data].id,
        'district': queryset[data].name,
        'leasing_count': leasing_agreem.count(),
        'tech_count': technics_count,
        'tech_price_sum': tech_price_sum,
        'contract_price_sum': contract_price_sum
    }
    return guarantee_company_data


def get_guarantee_company_data(queryset, data):
    guarantee_company_data = {
        'guarantee_id': queryset[data].id,
        'leasing_num': queryset[data].leasing_agreem.leasing_num,
        'leasing_date': queryset[data].leasing_agreem.leasing_date,
        'technique': {
            'name': queryset[data].leasing_agreem.expert_assessment.order_model.technique.name.name,
            'model': queryset[data].leasing_agreem.expert_assessment.order_model.technique.model,
            'number_of_techs': queryset[data].leasing_agreem.number_of_techs,
            'price': queryset[data].leasing_agreem.expert_assessment.order_model.technique.price,
            'contract_price': queryset[data].leasing_agreem.contract_price
        }
    }
    return guarantee_company_data


def get_guarantor_company_data(queryset, data):
    guarantee_company_data = {
        'guarantor': {
            'id': queryset[data].id,
            'stir': queryset[data].farmer_stir.stir,
            'full_name': queryset[data].farmer_stir.full_name,
            'legal_address': queryset[data].farmer_stir.legal_address,
            'director': queryset[data].farmer_stir.director,
            'phone_number': queryset[data].farmer_stir.phone_number,
            'payment_obligation': queryset[data].payment_obligation
        },
        'guarantee': {
            'id': queryset[data].guarantee_agreem.id,
            'guarantee_num': queryset[data].guarantee_agreem.guarantee_num,
            'guarantee_date': queryset[data].guarantee_agreem.guarantee_date
        },
        'contract_price': queryset[data].guarantee_agreem.leasing_agreem.contract_price
    }
    return guarantee_company_data


def get_leasing_company_province_data(queryset, data):
    order = Order.objects.filter(district__region_id_id=queryset[data].id)
    technics_count = order.aggregate(tech_count=Sum('expertassessment__leasingagreement__number_of_techs'))[
        'tech_count']
    statements_count = order.aggregate(statements_count=Count('statement'))['statements_count']
    contract_price_sum = order.aggregate(contract_price_sum=Sum('expertassessment__leasingagreement__contract_price'))[
        'contract_price_sum']
    order_company_data = {
        'id': queryset[data].id,
        'province': queryset[data].name,
        'order_count': order.count(),
        'tech_count': technics_count,
        'statements_count': statements_count,
        'contract_price_sum': contract_price_sum
    }
    return order_company_data


def get_leasing_company_district_data(queryset, data):
    order = Order.objects.filter(district_id=queryset[data].id)
    technics_count = order.aggregate(tech_count=Sum('expertassessment__leasingagreement__number_of_techs'))[
        'tech_count']
    statements_count = order.aggregate(statements_count=Count('statement'))['statements_count']
    contract_price_sum = order.aggregate(contract_price_sum=Sum('expertassessment__leasingagreement__contract_price'))[
        'contract_price_sum']
    leasing_company_data = {
        'id': queryset[data].id,
        'district': queryset[data].name,
        'order_count': order.count(),
        'tech_count': technics_count,
        'statements_count': statements_count,
        'contract_price_sum': contract_price_sum
    }
    return leasing_company_data


def get_leasing_company_data(queryset, data):
    leasing_company_data = {
        'leasing_id': queryset[data].id,
        'order': {
            'order_date': queryset[data].expert_assessment.order_model.order_date,
            'order_num': queryset[data].expert_assessment.order_model.order_num,
        },
        'statement': {
            'statement_date': queryset[data].expert_assessment.order_model.statement_set.first().statement_date,
            'statement_num': queryset[data].expert_assessment.order_model.statement_set.first().statement_num,
        },
        'leasing': {
            'leasing_num': queryset[data].leasing_num,
            'leasing_date': queryset[data].leasing_date,
        },
        'technique': {
            'name': queryset[data].expert_assessment.order_model.technique.name.name,
            'model': queryset[data].expert_assessment.order_model.technique.model,
            'number_of_techs': queryset[data].number_of_techs,
            'price': queryset[data].expert_assessment.order_model.technique.price,
            'yearly_leasing_percent': queryset[data].expert_assessment.order_model.technique.yearly_leasing_percent,
            'subsidy': queryset[data].expert_assessment.order_model.technique.subsidy,
            'leasing_term': queryset[data].expert_assessment.order_model.technique.leasing_term,
            'prepaid_percent': queryset[data].expert_assessment.order_model.technique.prepaid_percent,
            'contract_price': queryset[data].contract_price
        }
    }
    return leasing_company_data


def get_act_company_province_data(queryset, data):
    all_leasing_agreem = LeasingAgreement.objects.filter(
        expert_assessment__order_model__district__region_id_id=queryset[data].id)
    technics_count = all_leasing_agreem.aggregate(tech_count=Sum('number_of_techs'))['tech_count']
    tech_prepaid_price_sum = \
        all_leasing_agreem.aggregate(
            tech_prepaid_price_sum=Sum('expert_assessment__order_model__technique__prepaid_price'))[
            'tech_prepaid_price_sum']
    contract_price_sum = all_leasing_agreem.aggregate(contract_price_sum=Sum('contract_price'))['contract_price_sum']

    delivered_tech_leasing_agreem = LeasingAgreement.objects.filter(
        act__is_delivered=True,
        expert_assessment__order_model__district__region_id_id=queryset[data].id)
    delivered_technics_count = delivered_tech_leasing_agreem.aggregate(
        delivered_tech_count=Sum('number_of_techs'))['delivered_tech_count']
    delivered_tech_contract_price_sum = delivered_tech_leasing_agreem.aggregate(
        delivered_tech_contract_price_sum=Sum('contract_price'))['delivered_tech_contract_price_sum']
    guarantee_company_data = {
        'id': queryset[data].id,
        'province': queryset[data].name,
        'leasing_count': all_leasing_agreem.count(),
        'tech_count': technics_count,
        'tech_prepaid_price_sum': tech_prepaid_price_sum,
        'contract_price_sum': contract_price_sum,
        'delivered_tech_count': delivered_technics_count,
        'delivered_tech_contract_price_sum': delivered_tech_contract_price_sum
    }
    return guarantee_company_data


def get_act_company_district_data(queryset, data):
    all_leasing_agreem = LeasingAgreement.objects.filter(
        expert_assessment__order_model__district_id=queryset[data].id)
    technics_count = all_leasing_agreem.aggregate(tech_count=Sum('number_of_techs'))['tech_count']
    tech_prepaid_price_sum = \
        all_leasing_agreem.aggregate(
            tech_prepaid_price_sum=Sum('expert_assessment__order_model__technique__prepaid_price'))[
            'tech_prepaid_price_sum']
    contract_price_sum = all_leasing_agreem.aggregate(contract_price_sum=Sum('contract_price'))['contract_price_sum']

    delivered_tech_leasing_agreem = LeasingAgreement.objects.filter(
        act__is_delivered=True,
        expert_assessment__order_model__district_id=queryset[data].id)
    delivered_technics_count = delivered_tech_leasing_agreem.aggregate(
        delivered_tech_count=Sum('number_of_techs'))['delivered_tech_count']
    delivered_tech_contract_price_sum = delivered_tech_leasing_agreem.aggregate(
        delivered_tech_contract_price_sum=Sum('contract_price'))['delivered_tech_contract_price_sum']
    guarantee_company_data = {
        'id': queryset[data].id,
        'province': queryset[data].name,
        'leasing_count': all_leasing_agreem.count(),
        'tech_count': technics_count,
        'tech_prepaid_price_sum': tech_prepaid_price_sum,
        'contract_price_sum': contract_price_sum,
        'delivered_tech_count': delivered_technics_count,
        'delivered_tech_contract_price_sum': delivered_tech_contract_price_sum
    }
    return guarantee_company_data


def get_act_company_data_contract(queryset, data):
    act_company_data = {
        'act_id': queryset[data].id,
        'leasing': {
            'leasing_num': queryset[data].leasing_agreem.leasing_num,
            'leasing_date': queryset[data].leasing_agreem.leasing_date,
        },
        'technique': {
            'name': queryset[data].leasing_agreem.expert_assessment.order_model.technique.name.name,
            'model': queryset[data].leasing_agreem.expert_assessment.order_model.technique.model,
            'number_of_techs': queryset[data].leasing_agreem.number_of_techs,
            'price': queryset[data].leasing_agreem.expert_assessment.order_model.technique.price,
            'contract_price': queryset[data].leasing_agreem.contract_price,
            'prepaid_price': queryset[data].leasing_agreem.expert_assessment.order_model.technique.prepaid_price,
            'prepaid_percent': queryset[data].leasing_agreem.expert_assessment.order_model.technique.prepaid_percent,
        }
    }
    return act_company_data


def get_act_company_data(instance):
    act_company_data = {
        'act': {
            'id': instance.id,
            'act_num': instance.act_num,
            'act_date': instance.act_date,
        },
        'technique': {
            'name': instance.leasing_agreem.expert_assessment.order_model.technique.name.name,
            'model': instance.leasing_agreem.expert_assessment.order_model.technique.model,
            'number_of_techs': instance.leasing_agreem.number_of_techs,
            'price': instance.leasing_agreem.expert_assessment.order_model.technique.price,
            'contract_price': instance.leasing_agreem.contract_price,
            'prepaid_price': instance.leasing_agreem.expert_assessment.order_model.technique.prepaid_price,
            'prepaid_percent': instance.leasing_agreem.expert_assessment.order_model.technique.prepaid_percent,
        },
        'seller_fullname': instance.seller_stir.full_name
    }
    return act_company_data


# FARMER SIDE
def get_order_data(queryset, data):
    leasing_agreem = LeasingAgreement.objects.filter(expert_assessment__order_model=queryset[data].id).first()
    if leasing_agreem:
        order_data = {
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
    else:
        order_data = {
            'id': queryset[data].technique.id,
            'name': queryset[data].technique.name.name,
            'model': queryset[data].technique.model,
            'price': queryset[data].technique.price,
            'number_of_techs': None,
            'yearly_leasing_percent': queryset[data].technique.yearly_leasing_percent,
            'subsidy': queryset[data].technique.subsidy,
            'leasing_term': queryset[data].technique.leasing_term,
            'prepaid_percent': queryset[data].technique.prepaid_percent,
            'contract_price': None
        }
    return order_data


def get_leasing_data(queryset, data):
    leasing_data = {
        'technique': {
            'id': queryset[data].expert_assessment.order_model.technique.id,
            'name': queryset[data].expert_assessment.order_model.technique.name.name,
            'model': queryset[data].expert_assessment.order_model.technique.model,
            'price': queryset[data].expert_assessment.order_model.technique.price,
            'yearly_leasing_percent': queryset[data].expert_assessment.order_model.technique.yearly_leasing_percent,
            'subsidy': queryset[data].expert_assessment.order_model.technique.subsidy,
            'leasing_term': queryset[data].expert_assessment.order_model.technique.leasing_term,
            'prepaid_percent': queryset[data].expert_assessment.order_model.technique.prepaid_percent
        },
        'order': {
            'order_num': queryset[data].expert_assessment.order_model.order_num,
            'order_date': queryset[data].expert_assessment.order_model.order_date
        }
    }
    return leasing_data


def get_guarantee_data(queryset, data):
    guarantee_data = {
        'guarantee': {
            'id': queryset[data].id,
        },
        'leasing': {
            'id': queryset[data].leasing_agreem.id,
            'leasing_num': queryset[data].leasing_agreem.leasing_num,
            'leasing_date': queryset[data].leasing_agreem.leasing_date
        },
        'technique': {
            'id': queryset[data].leasing_agreem.expert_assessment.order_model.technique.id,
            'name': queryset[data].leasing_agreem.expert_assessment.order_model.technique.name.name,
            'model': queryset[data].leasing_agreem.expert_assessment.order_model.technique.model,
            'price': queryset[data].leasing_agreem.expert_assessment.order_model.technique.price,
            'contract_price': queryset[data].leasing_agreem.contract_price,
            'number_of_techs': queryset[data].leasing_agreem.number_of_techs
        }
    }
    return guarantee_data


def get_guarantor_data(queryset, data):
    farmer_stir = queryset[data].farmer_stir
    if farmer_stir:
        guarantor_data = {
            'leasing': {
                'id': queryset[data].guarantee_agreem.leasing_agreem.id,
                'contract_price': queryset[data].guarantee_agreem.leasing_agreem.contract_price
            },
            'guarantee': {
                'id': queryset[data].guarantee_agreem.id,
                'guarantee_num': queryset[data].guarantee_agreem.guarantee_num,
                'guarantee_date': queryset[data].guarantee_agreem.guarantee_date
            },
            'guarantor': {
                'id': queryset[data].id,
                'stir': queryset[data].farmer_stir.stir,
                'full_name': queryset[data].farmer_stir.full_name,
                'legal_address': queryset[data].farmer_stir.legal_address,
                'director': queryset[data].farmer_stir.director,
                'phone_number': queryset[data].farmer_stir.phone_number
            }
        }
    else:
        guarantor_data = {
            'leasing': {
                'id': queryset[data].guarantee_agreem.leasing_agreem.id,
                'contract_price': queryset[data].guarantee_agreem.leasing_agreem.contract_price
            },
            'guarantee': {
                'id': queryset[data].guarantee_agreem.id,
                'guarantee_num': queryset[data].guarantee_agreem.guarantee_num,
                'guarantee_date': queryset[data].guarantee_agreem.guarantee_date
            },
            'guarantor': {
                'id': None,
                'stir': None,
                'full_name': None,
                'legal_address': None,
                'director': None,
                'phone_number': None
            }
        }
    return guarantor_data


def get_payment_table_other_data(queryset):
    payment_table_technique_data = {
        'name': queryset[0].payment_graph.act.leasing_agreem.expert_assessment.order_model.technique.name.name,
        'model': queryset[0].payment_graph.act.leasing_agreem.expert_assessment.order_model.technique.model,
        'price': queryset[0].payment_graph.act.leasing_agreem.expert_assessment.order_model.technique.price,
        'yearly_leasing_percent': queryset[
            0].payment_graph.act.leasing_agreem.expert_assessment.order_model.technique.yearly_leasing_percent,
        'leasing_term': queryset[
            0].payment_graph.act.leasing_agreem.expert_assessment.order_model.technique.leasing_term,
        'prepaid_percent': queryset[
            0].payment_graph.act.leasing_agreem.expert_assessment.order_model.technique.prepaid_percent,
        'prepaid_price': queryset[
            0].payment_graph.act.leasing_agreem.expert_assessment.order_model.technique.prepaid_price,
        'contract_price': queryset[0].payment_graph.act.leasing_agreem.contract_price,
        'act_date': queryset[0].payment_graph.act.act_date,
    }
    return payment_table_technique_data


def get_payment_table_data(queryset):
    technique_price = queryset.act.leasing_agreem.expert_assessment.order_model.technique.price * \
                      queryset.act.leasing_agreem.number_of_techs
    yearly_leasing_percent = queryset.act.leasing_agreem.expert_assessment.order_model.technique.yearly_leasing_percent
    leasing_term = queryset.act.leasing_agreem.expert_assessment.order_model.technique.leasing_term
    # leasing_term = 5
    prepaid_price = queryset.act.leasing_agreem.expert_assessment.order_model.technique.prepaid_price
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
