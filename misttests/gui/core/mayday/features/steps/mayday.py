from misttests.gui.steps.email import *
from misttests.gui.steps.sso import *
from misttests.gui.steps.navigation import *
from misttests.gui.steps.landing import *
from misttests.gui.steps.clouds import *
from misttests.gui.steps.search import *
from misttests.gui.steps.graphs import *
from misttests.gui.steps.machines import *
from misttests.gui.steps.popups import *
from misttests.gui.steps.modals import *
from misttests.gui.steps.ssh import *
from misttests.gui.steps.browser import *
from misttests.gui.steps.dialog import *
from misttests.gui.steps.list import *
from misttests.gui.steps.utils import safe_get_element_text

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from behave import step
from time import sleep, time

import requests


@step(u'I search for the mayday machine')
def search_for_mayday_machine(context):
    search_bar = context.browser.find_element_by_css_selector("input.top-search")
    if context.mist_config.get('MAYDAY_MACHINE'):
        text = context.mist_config['MAYDAY_MACHINE']
    for letter in text:
        search_bar.send_keys(letter)
    sleep(2)


@step(u'I delete old mayday emails')
def delete_old_mayday_emails(context):

    box = imaplib.IMAP4_SSL("imap.gmail.com")
    box.login(context.mist_config['GOOGLE_TEST_EMAIL'],
                      context.mist_config['GOOGLE_TEST_PASSWORD'])
    box.select("INBOX")
    typ, data = box.search(None, 'ALL')
    if not data[0].split():
        return

    for num in data[0].split():
        box.store(num, '+FLAGS', '\\Deleted')
    box.expunge()
    logout_email(box)


@step(u'I should receive an email within {seconds} seconds')
def receive_mail(context, seconds):
    end_time = time() + int(seconds)
    error = ""

    while time() < end_time:
        log.info("Looking if email has arrived\n\n")
        try:
            box = imaplib.IMAP4_SSL("imap.gmail.com")
            box.login(context.mist_config['GOOGLE_TEST_EMAIL'],
                              context.mist_config['GOOGLE_TEST_PASSWORD'])
            if not box:
                error = "login failed"
                continue
            inbox = box.select("INBOX")
        except Exception as e:
            log.info("An exception occurred: %s\n\n" % str(e))
            continue

        log.info("Searching in inbox for email\n\n")
        typ, data = box.search(None, 'ALL')

        if data[0].split():
            return
        else:
            logout_email(box)
            log.info("Email has not arrived yet. Sleeping for 15 seconds\n\n")
            sleep(15)

    assert False, u'Did not receive an email within %s seconds. %s' % (seconds,
                                                                       error)

@step(u'I click the mayday machine')
def click_mayday_machine(context):
    """
    This function will try to click a button that says exactly the same thing as
    the text given. If it doesn't find any button like that then it will try
    to find a button that contains the text given. If text is a key inside
    mist_config dict then it's value will be used.
    """
    if context.mist_config.get('MAYDAY_MACHINE'):
        text = context.mist_config['MAYDAY_MACHINE']
    button = context.browser.find_element_by_xpath("//vaadin-grid-table-row[.//strong[text()='%s']]" % text)
    clicketi_click(context, button)


@step(u'Mayday machine state should be "{state}" within {seconds} seconds')
def assert_mayday_machine_state(context, state, seconds):
    if context.mist_config.get('MAYDAY_MACHINE'):
        name = context.mist_config.get('MAYDAY_MACHINE')
    end_time = time() + int(seconds)
    while time() < end_time:
        machine = get_machine(context, name)
        if machine:
            try:
                if state in safe_get_element_text(machine):
                    return
            except NoSuchElementException:
                pass
            except StaleElementReferenceException:
                pass
        sleep(2)

    assert False, u'%s state is not "%s"' % (name, state)


@step(u'I choose the mayday machine')
def reboot_mayday_machine(context):
    if context.mist_config.get('MAYDAY_MACHINE'):
        name = context.mist_config.get('MAYDAY_MACHINE')

    end_time = time() + 20
    while time() < end_time:
        machine = get_machine(context, name)
        if machine:
            checkbox = machine.find_element_by_class_name("mist-check")
            checkbox.click()
            return

        sleep(2)
    assert False, u'Could not choose/tick %s machine' % name


@step(u'I fill "{value}" as metric value')
def rule_value(context, value):
    value_input = context.browser.find_element_by_xpath("//paper-input[@id='metricValue']")
    actions = ActionChains(context.browser)
    actions.move_to_element(value_input)
    actions.click()
    actions.send_keys(Keys.BACK_SPACE)
    actions.perform()

    actions.move_to_element(value_input)
    actions.click()
    actions.send_keys("0")
    actions.perform()


@step(u'I should see the incident "{incident}"')
def check_for_incident(context, incident):
    incidents_list = context.browser.find_elements_by_css_selector('div.block div.list')

    for item in incidents_list:
        if incident in safe_get_element_text(item) :
            return

    assert False, "Incident %s was not found in the home page" % incident


@step(u'I add the MaydaySchedule via api')
def add_mayday_schedule(context):
    headers = {'Authorization': context.mist_config['MAYDAY_TOKEN']}
    conditions = [{'type': 'tags', 'tags': {'mayday-test': ''}}]

    payload = {
     'name': 'MaydayScheduler',
     'action':'stop',
     'schedule_type':'interval',
     'conditions': conditions,
     'schedule_entry': {'every': 4, 'period':'minutes'},
     'task_enabled': True
    }

    uri = context.mist_config['MIST_URL'] + '/api/v1/schedules'
    response = requests.post(uri, data=json.dumps(payload), headers=headers)
    assert response.status_code == 200, "Could not add MaydayScheduler schedule!"
