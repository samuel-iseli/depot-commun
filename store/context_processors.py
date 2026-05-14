def selected_customer(request):
    if not request.user.is_authenticated:
        return {'selected_customer': None}

    customers = request.user.customers.order_by('name', 'id')
    selected_customer_id = request.session.get('selected_customer_id')

    selected = None
    if selected_customer_id is not None:
        selected = customers.filter(id=selected_customer_id).first()

    if selected is None:
        selected = customers.first()
        if selected is not None:
            request.session['selected_customer_id'] = selected.id

    return {'selected_customer': selected}