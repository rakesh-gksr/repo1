from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestMaxTextbox/",  # report_relative_location
                               "test_max_textbox",  # report_file_name_prefix
                               "verify text length for static text",  # test_suite_title
                               ("This test adds a textbox with max text length"
                                " and then checks to make sure that we can not add anymore characters past the max limit"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver

    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_max_textbox(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify text length for static text.")
    try:
        mySurvey.myBuilder.click_SingleTextboxAddButton()
        wallOfText = mySurvey.myLogic.RNG(4001)
        mySurvey.myQuestion.enter_question_title(wallOfText)
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.check_q_title_in_preview(1, wallOfText[:-1])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify maximum textbox length",
                                 "checks to make sure that we can not add more than the maximum textbox length",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify maximum textbox length."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
