from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestMaxMultiTextboxLabel/",  # report_relative_location
                               "test_max_multiTextboxLabel",  # report_file_name_prefix
                               "text length of multi textbox label",  # test_suite_title
                               ("This test adds a multiple textbox question with greater than max length label"
                                " and verifies that question saved with max length label."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_max_multiTextboxLabel(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "text length of multi textbox label")
    try:
        mySurvey.myBuilder.click_MultipleTextboxesAddButton()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, mySurvey.myLogic.RNG(3001))
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = True if mySurvey.myQuestion.verify_multiTextbox_answerRow_length(1, 1) == 3000 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question label is max length",
                                 "checks to make sure that label is length 3000",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify max length of multi textbox label."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
