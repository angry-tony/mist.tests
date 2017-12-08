from behave import step

from misttests.gui.steps.utils import safe_get_element_text
from misttests.gui.steps.buttons import clicketi_click


@step(u'there should be a message with text "{text}"')
def check_plan_overusage_message(context, text):
    plan_overusage = context.browser.find_element_by_tag_name('plan-overusage')
    assert safe_get_element_text(plan_overusage) == text, "Plan overusage message was not: %s, instead it was: %s" %(text, safe_get_element_text(plan_overusage))


@step(u'the current plan should be "{text}"')
def check_current_plan_message(context, text):
    plans = context.browser.find_elements_by_tag_name('plan-item')
    assert text in safe_get_element_text(plans[0]), "Current plan was not: %s, instead it was: %s" %(text, safe_get_element_text(plans[0]))


@step(u'I click the upgrade button under small plan')
def upgrate_to_small_plan(context):
    plans = context.browser.find_elements_by_tag_name('plan-item')
    small_plan = plans[1].find_element_by_tag_name('paper-button')
    clicketi_click(context, small_plan)


@step(u'I set the card details in the credit card required dialog')
def purchase_plan(context):
    purchase_plan = context.browser.find_element_by_id('ccRequired')
    form = purchase_plan.find_element_by_id('inAddCloud')
    insert_to_card_field('cc', '4242424242424242', form)
    insert_to_card_field('cvc', '123', form)
    insert_to_card_field('expirationMonth', '12', form)
    insert_to_card_field('expirationYear', '27', form)
    insert_to_card_field('zipCode', '17675', form)


def insert_to_card_field(field, value, form):
    _field = form.find_element_by_id(field)
    _input = _field.find_element_by_id('input')
    _input.send_keys(value)
    import ipdb; ipdb.set_trace()
