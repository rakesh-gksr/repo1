"""
Quota type : Simple quota
Test case for verifying error messages for required field
"""

from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest

__author__ = 'mangesh'

@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicSimpleQuota/",  # report_relative_location
                               "test_logic_simpleQuota_verify_error_message",  # report_file_name_prefix
                               "verify Quota logic",  # test_suite_title
                               ("This test applies a simple page quota "
                                " to verify that error messages by not entering answer"
                                " group label, quota value and not selecting answer choices"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename

@pytest.mark.quota
@pytest.mark.C83899
@pytest.mark.IB
def test_logic_simpleQuota_verifyErrorMessage(create_survey):
    """
    Test case name : Verify error messages by not entering answer group label and quota value, not selecting answer choices
    :param create_survey: fixture to create survey
    """
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify error messages")
    try:
        # parameters that has to be passed for searchForQuestion function
        answers = ["Very noisy", "Somewhat noisy", "not at all"]
        # Add multiple choice question
        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "How noisy is this neighborhood?", answers)
        mySurvey.myLogic.pushQuestionToStack("How noisy is this neighborhood?")

        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_Quota()
        # call to function to verify error messages when attempt to save quota without filling group label and answer
        ex = mySurvey.myLogic.quotaVerifyErrorMessage("simple", 1, 1, [])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that it should give proper error message",
                                 "checks to make sure that the Quota Group do not created.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify error message"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
