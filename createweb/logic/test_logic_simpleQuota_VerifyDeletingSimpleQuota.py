"""
Quota type : Simple quota
Test case for verifying deletion of quota by click on delete quota button
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
                               "test_logic_simpleQuota_verify_deleting_simple_quota",  # report_file_name_prefix
                               "Verify simple quota delete",  # test_suite_title
                               ("This test applies a simple page quota "
                                " to verify that deletion of simple quota."),  # test_suite_description
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
@pytest.mark.C83903
@pytest.mark.IB
def test_logic_simpleQuota_verifyDeletingSimpleQuota(create_survey):
    """
    Test case name : simple quota: verify deleting simple quota clicking on 'Delete quota' button

    Args:
    create_survey: fixture to create survey

    """
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify simple quota delete")
    try:
        # parameters that has to be passed for searchForQuestion function
        answers = ["Very noisy", "Somewhat noisy", "not at all"]
        # parameters that has to be passes for selectAnswersForGroup function
        answers_for_group = [2, 3]
        # Add multiple choice question
        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "How noisy is this neighborhood?", answers)
        mySurvey.myLogic.pushQuestionToStack("How noisy is this neighborhood?")

        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_Quota()
        mySurvey.myLogic.quotaSetupWizard("simple", 1, 1, [1])
        ex = mySurvey.myLogic.checkQuotaIcon(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page quota icon appears",
                                 "checks to make sure that the Quota added.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of page quota icon"

        mySurvey.myLogic.deleteQuota()
        mySurvey.myLogic.click_QuotaFirstDoneButton()
        ex = mySurvey.myLogic.checkQuotaOff()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page quota is deleted",
                                 "checks to make sure that the Quota is deleted.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify quota status"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

