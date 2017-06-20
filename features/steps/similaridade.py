@given(u'que possuo {5,3,4,4} e {3,1,2,3}')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given que possuo {5,3,4,4} e {3,1,2,3}')

@when(u'realizo o calculo de similaridade')
def step_impl(context):
    raise NotImplementedError(u'STEP: When realizo o calculo de similaridade')

@then(u'deverá ser igual ao 0.85')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then deverá ser igual ao 0.85')
