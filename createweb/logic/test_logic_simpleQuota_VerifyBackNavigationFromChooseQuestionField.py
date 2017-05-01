"""
Quota type : Simple quota
Test case for verifying deletion of quota by using bach navigation from choose question field
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
                               "test_logic_simpleQuota_back_navigation_from_chooseQuestionField",  # report_file_name_prefix
                               "Verify back navigation from choose question field",  # test_suite_title
                               ("This test verifies back navigation on simple quota"),  # test_suite_description
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
@pytest.mark.C83912
@pytest.mark.IB
def test_logic_simpleQuota_verifyBackNavigationFromChooseQuestionField(create_survey):
    """
    Test case name : simple quota: verify back navigation from simple quota by clicking on Cancel button on choose question field
    :param create_survey: fixture to create survey
    """
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify back navigation from choose question field.")
    try:
        # parameters that has to be passed for searchForQuestion function
        answers = ["Very noisy", "Somewhat noisy", "not at all"]
        # Add multiple choice question
        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "How noisy is this neighborhood?", answers)
        mySurvey.myLogic.pushQuestionToStack("How noisy is this neighborhood?")

        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_Quota()
        # call to function to verify error messages when attempt to save quota without filling group label and answer
        mySurvey.myLogic.quotaVerifyNavigationFromChooseQuestionField("simple", 1, 1)
        mySurvey.myLogic.click_Quota()

        ex = mySurvey.myLogic.checkQuotaOff()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify back navigation",
                                 "checks to make sure that User navigate to the logic accordian from question select field.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify the quota status"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
