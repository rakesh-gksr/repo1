'''
test_SurveyDesignAccordion.py

test the Accordion control which holds the

Builder,
QuestionBank,
Logic,
Options,
Themes

    # get user
    # login
    # create a new survey
    # in the Design page:
    #   verify we start out with Builder Pleat selected
    #   click on and verify we have the QuestionBank Pleat
    #   click on and verify we have the Logic Pleat
    #   click on and verify we have the Options Pleat
    #   click on and verify we have the Themes Pleat
    #   click on and verify we have the Builder Pleat
'''

from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import pytest


@pytest.fixture(scope="module")
def get_report(request):

    report = reporting_wrapper("Create",  # report_feature_name
                               "AccordionTest/",  # report_relative_location
                               "accordion_test",  # report_file_name_prefix
                               # test_suite_title
                               "Testing the Accordion Controls that hold the banks of buttons",
                               ("Testing controls in the accordion "
                                "related to designing a survey"
                                " work as intended"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.BVT})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split(
        '.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.BVT
@pytest.mark.TC_BVT
def test_accordion_displayed(create_survey):

    driver, mySurvey, report = create_survey

    case_title = "Is Accordion Displayed?"
    case_description = "Checking that the accordion control is by default displayed and available."
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        case_title,
        case_description)

    step_title = "Check accordion"
    step_description = "Accordion should be visible and active"
    accordion_displayed_result = mySurvey.myAccordion.is_Accordion_displayed()
    add_console_log = True
    take_screenshot = True
    report.add_report_record(
        ReportMessageTypes.TEST_STEP,
        step_title,
        step_description,
        accordion_displayed_result,
        add_console_log,
        take_screenshot,
        driver)
    assert accordion_displayed_result

    case_title = "QuestionBank control works?"
    case_description = "Checking that the accordion control for QuestionBank opens when clicked upon."
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        case_title,
        case_description)

    section_codex_name = mySurvey.myAccordion.CreateAccordion.QuestionBank
    mySurvey.myAccordion.unfold_QuestionBank()
    section_open = mySurvey.myAccordion.is_section_open(section_codex_name)
    section_closed = mySurvey.myAccordion.is_section_closed(section_codex_name)
    result = (section_open and not section_closed)

    step_title = "Click on QuestionBank control"
    step_description = "QuestionBank should be visible and active"
    add_console_log = True
    take_screenshot = True
    report.add_report_record(
        ReportMessageTypes.TEST_STEP,
        step_title,
        step_description,
        result,
        add_console_log,
        take_screenshot,
        driver)

    assert section_open
    assert not section_closed


def test_Logic_Pleat(create_survey):
    driver, mySurvey, report = create_survey

    case_title = "Logic control works?"
    case_description = "Checking that the accordion control for Logic opens when clicked upon."
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        case_title,
        case_description)

    section_codex_name = mySurvey.myAccordion.CreateAccordion.Logic
    mySurvey.myAccordion.unfold_Logic()
    section_open = mySurvey.myAccordion.is_section_open(section_codex_name)
    section_closed = mySurvey.myAccordion.is_section_closed(section_codex_name)
    result = (section_open and not section_closed)

    step_title = "Click on Logic control"
    step_description = "Logic should be visible and active"
    add_console_log = True
    take_screenshot = True
    report.add_report_record(
        ReportMessageTypes.TEST_STEP,
        step_title,
        step_description,
        result,
        add_console_log,
        take_screenshot,
        driver)

    assert section_open
    assert not section_closed


def test_Options_Pleat(create_survey):
    driver, mySurvey, report = create_survey

    case_title = "Options control works?"
    case_description = "Checking that the accordion control for Options opens when clicked upon."
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        case_title,
        case_description)

    section_codex_name = mySurvey.myAccordion.CreateAccordion.Option
    mySurvey.myAccordion.unfold_Options()
    section_open = mySurvey.myAccordion.is_section_open(section_codex_name)
    section_closed = mySurvey.myAccordion.is_section_closed(section_codex_name)
    result = (section_open and not section_closed)

    step_title = "Options accordion"
    step_description = "Options controls in accordion should be visible and active"
    add_console_log = True
    take_screenshot = True
    report.add_report_record(
        ReportMessageTypes.TEST_STEP,
        step_title,
        step_description,
        result,
        add_console_log,
        take_screenshot,
        driver)
    assert section_open
    assert not section_closed


def test_Themes_Pleat(create_survey):
    driver, mySurvey, report = create_survey

    case_title = "Themes control works?"
    case_description = "Checking that the accordion control for Themes opens when clicked upon."
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        case_title,
        case_description)

    section_codex_name = mySurvey.myAccordion.CreateAccordion.Theme
    mySurvey.myAccordion.unfold_Themes()
    section_open = mySurvey.myAccordion.is_section_open(section_codex_name)
    section_closed = mySurvey.myAccordion.is_section_closed(section_codex_name)
    result = (section_open and not section_closed)

    step_title = "Themes accordion"
    step_description = "Themes controls in accordion should be visible and active"
    add_console_log = True
    take_screenshot = True
    report.add_report_record(
        ReportMessageTypes.TEST_STEP,
        step_title,
        step_description,
        result,
        add_console_log,
        take_screenshot,
        driver)
    assert section_open
    assert not section_closed


def test_Builder_Pleat(create_survey):
    driver, mySurvey, report = create_survey

    case_title = "Builder control works?"
    case_description = "Checking that the accordion control for Builder opens when clicked upon."
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        case_title,
        case_description)

    section_codex_name = mySurvey.myAccordion.CreateAccordion.Builder
    mySurvey.myAccordion.unfold_Builder()
    section_open = mySurvey.myAccordion.is_section_open(section_codex_name)
    section_closed = mySurvey.myAccordion.is_section_closed(section_codex_name)
    result = (section_open and not section_closed)

    step_title = "Builder accordion"
    step_description = "Builder controls in accordion should be visible and active"
    add_console_log = True
    take_screenshot = True
    report.add_report_record(
        ReportMessageTypes.TEST_STEP,
        step_title,
        step_description,
        result,
        add_console_log,
        take_screenshot,
        driver)
    assert section_open
    assert not section_closed
