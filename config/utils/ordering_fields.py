def ordering_technique_model(ordering_name, queryset, ordering_technique_fields):
    if ordering_technique_fields and \
            ((ordering_name in ordering_technique_fields) or (ordering_name[1:] in ordering_technique_fields)):
        return queryset.order_by(f'{ordering_name}')
    return queryset


def ordering_order_model(ordering_name, queryset, ordering_technique_fields, ordering_order_fields):
    if ordering_name[:1] != '-':
        if (ordering_name in ordering_order_fields) or (ordering_name[1:] in ordering_order_fields):
            return queryset.order_by(f'{ordering_name}')
        elif ordering_name in ordering_technique_fields:
            return queryset.order_by(f'technique__{ordering_name}')
    else:
        if ordering_name[1:] in ordering_order_fields:
            return queryset.order_by(f'{ordering_name}')
        elif ordering_name[1:] in ordering_technique_fields:
            return queryset.order_by(f'-technique__{ordering_name[1:]}')
    return queryset


def ordering_leasing_model(ordering_name, queryset, ordering_technique_fields,
                           ordering_order_fields, ordering_leasing_fields):
    if ordering_name[:1] != '-':
        if ordering_name in ordering_leasing_fields:
            return queryset.order_by(f'{ordering_name}')
        elif ordering_name in ordering_order_fields:
            return queryset.order_by(f'expert_assessment__order_model__{ordering_name}')
        elif ordering_name in ordering_technique_fields:
            return queryset.order_by(f'expert_assessment__order_model__technique__{ordering_name}')
    else:
        if ordering_name[1:] in ordering_leasing_fields:
            return queryset.order_by(f'{ordering_name}')
        elif ordering_name[1:] in ordering_order_fields:
            return queryset.order_by(f'-expert_assessment__order_model__{ordering_name[1:]}')
        elif ordering_name[1:] in ordering_technique_fields:
            return queryset.order_by(f'-expert_assessment__order_model__technique__{ordering_name[1:]}')
    return queryset


def ordering_guarantee_model(ordering_name, queryset, ordering_technique_fields, ordering_leasing_fields,
                             ordering_guarantee_fields):
    if ordering_name[:1] != '-':
        if ordering_name in ordering_guarantee_fields:
            return queryset.order_by(f'{ordering_name}')
        elif ordering_name in ordering_leasing_fields:
            return queryset.order_by(f'leasing_agreem__{ordering_name}')
        elif ordering_name in ordering_technique_fields:
            return queryset.order_by(f'leasing_agreem__expert_assessment__order_model__technique__{ordering_name}')
    else:
        if ordering_name[1:] in ordering_guarantee_fields:
            return queryset.order_by(f'{ordering_name}')
        elif ordering_name[1:] in ordering_leasing_fields:
            return queryset.order_by(f'-leasing_agreem__{ordering_name[1:]}')
        elif ordering_name[1:] in ordering_technique_fields:
            return queryset.order_by(f'-leasing_agreem__expert_assessment__order_model__technique__{ordering_name[1:]}')
    return queryset


def ordering_guarantor_model(ordering_name, queryset, ordering_technique_fields, ordering_leasing_fields,
                             ordering_guarantor_fields):
    if ordering_name[:1] != '-':
        if ordering_name in ordering_guarantor_fields:
            return queryset.order_by(f'{ordering_name}')
        elif ordering_name in ordering_leasing_fields:
            return queryset.order_by(f'guarantee_agreem__leasing_agreem__{ordering_name}')
        elif ordering_name in ordering_technique_fields:
            return queryset.order_by(
                f'guarantee_agreem__leasing_agreem__expert_assessment__order_model__technique__{ordering_name}')
    else:
        if ordering_name[1:] in ordering_guarantor_fields:
            return queryset.order_by(f'{ordering_name}')
        elif ordering_name[1:] in ordering_leasing_fields:
            return queryset.order_by(f'-guarantee_agreem__leasing_agreem__{ordering_name[1:]}')
        elif ordering_name[1:] in ordering_technique_fields:
            return queryset.order_by(
                f'-guarantee_agreem__leasing_agreem__expert_assessment__order_model__technique__{ordering_name[1:]}')
    return queryset


def ordering_act_model(ordering_name, queryset, ordering_technique_fields, ordering_leasing_fields,
                       ordering_act_fields):
    if ordering_name[:1] != '-':
        if ordering_name in ordering_act_fields:
            return queryset.order_by(f'{ordering_name}')
        elif ordering_name in ordering_leasing_fields:
            return queryset.order_by(f'leasing_agreem__{ordering_name}')
        elif ordering_name in ordering_technique_fields:
            return queryset.order_by(f'leasing_agreem__expert_assessment__order_model__technique__{ordering_name}')
    else:
        if ordering_name[1:] in ordering_act_fields:
            return queryset.order_by(f'{ordering_name}')
        elif ordering_name[1:] in ordering_leasing_fields:
            return queryset.order_by(f'-leasing_agreem__{ordering_name[1:]}')
        elif ordering_name[1:] in ordering_technique_fields:
            return queryset.order_by(f'-leasing_agreem__expert_assessment__order_model__technique__{ordering_name[1:]}')
    return queryset


def ordering_payment_graph_model(ordering_name, queryset, ordering_technique_fields, ordering_leasing_fields, ):
    if ordering_name[:1] != '-':
        if ordering_name in ordering_leasing_fields:
            return queryset.order_by(f'act__leasing_agreem__{ordering_name}')
        elif ordering_name in ordering_technique_fields:
            return queryset.order_by(f'act__leasing_agreem__expert_assessment__order_model__technique__{ordering_name}')
    else:
        if ordering_name[1:] in ordering_leasing_fields:
            return queryset.order_by(f'-act__leasing_agreem__{ordering_name[1:]}')
        elif ordering_name[1:] in ordering_technique_fields:
            return queryset.order_by(
                f'-act__leasing_agreem__expert_assessment__order_model__technique__{ordering_name[1:]}')
    return queryset
