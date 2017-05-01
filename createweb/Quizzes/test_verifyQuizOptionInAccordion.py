from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestVerifyQuizOptionInAccordion/",  # report_relative_location
                               "test_verifyQuizOptionInAccordion",  # report_file_name_prefix
                               # test_suite_title
                               ("verify adding star question from clicking on 'add a new question button' and then "
                                "switch to star"),
                               ("Test to verify adding star question from clicking on 'add a new question button' and "
                                "then switch to star"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().\
        strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.quiz
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C12809380
def test_verify_quiz_option_in_accordion(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify the Quiz option present in the Accordion and user is able to Enable & Disable the option")
    try:
        mySurvey.myOptions.unfold_OptionsRegion()
        mySurvey.myOptions.toggle_quiz_mode(display_quiz_result=False, show_collect_answers=False)
        ex = mySurvey.myOptions.verify_quiz_toggle(is_toggle_on=True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Quiz Mode is On",
                                 "Verifies that quiz mode is on",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify quiz mode is on."
        ex = mySurvey.myOptions.check_quiz_selected_options(display_quiz_result=True, show_collect_answers=True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Quiz Results and Answers Checkboxes",
                                 "Verifies that quiz results and answers checkboxes are checked",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify quiz results and answers checkboxes are checked."

        mySurvey.myOptions.toggle_quiz_mode(display_quiz_result=False, show_collect_answers=False)
        ex = mySurvey.myOptions.verify_quiz_toggle( is_toggle_on=False)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Quiz Mode is Off",
                                 "Verifies that quiz mode is off",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify quiz mode is off."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
