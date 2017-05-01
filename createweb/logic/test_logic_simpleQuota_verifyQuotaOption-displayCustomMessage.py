"""
Quota type : Simple quota
Test case for verifying 'display a custom message' of quota option
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
                               "TestLogicCustomOption/",  # report_relative_location
                               "test_logic_CustomOption_display_custom_message",  # report_file_name_prefix
                               "Verify quota option Display custom message",  # test_suite_title
                               ("This test verifies quota option Display custom message"
                                " to verify quota option Display custom option"),  # test_suite_description
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
@pytest.mark.C83900
@pytest.mark.Infobeans
@pytest.mark.IB
def test_logic_simpleQuota_verifyQuotaOption_displayCustomMessage(create_survey):
    """
    Test case name : verify quota option - display a custom message

    Args:
    create_survey: fixture to create survey

    """
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify quota option Display custom message.")
    try:
        # parameters that has to be passed for searchForQuestion function
        answers = ["Very noisy", "Somewhat noisy", "not at all"]
        # custom message that has to be pass for
        custom_message = "This is custom message"
        # Add multiple choice question
        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "How noisy is this neighborhood?", answers)
        mySurvey.myLogic.pushQuestionToStack("How noisy is this neighborhood?")

        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_Quota()
        mySurvey.myLogic.quotaSetupWizard("simple", 1, 1, [1])
        mySurvey.myLogic.click_QuotaOptions()
        ex = mySurvey.myLogic.click_selectingOption_displayCustomOption(custom_message)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify quota option Display Custom Message.",
                                 "checks to verify quota option Display Custom Message is selected.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)

        assert ex, "Unable to verify Display Custom Message quota option"

        ex = mySurvey.myLogic.verifyComboQuotaStatus("On")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Quota status.",
                                 "checks to verify quota status is on.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)

        assert ex, "Unable to verify quota status"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

