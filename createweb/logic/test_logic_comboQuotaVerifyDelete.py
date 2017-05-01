"""
Quota type : combination quota
This test case checks the deletion of Quota via clicking on Delete Quota button
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
                               "TestLogicComboQuota/",  # report_relative_location
                               "test_logic_comboQuota_verify_delete",  # report_file_name_prefix
                               "verify deleting combo quota",  # test_suite_title
                               ("This test verifies deletion of combo quota"),  # test_suite_description
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
@pytest.mark.C83910
@pytest.mark.IB
def test_logic_comboQuotaVerifyDelete(create_survey):
    """
    Test case name : combination quota: delete via clicking on Delete Quota button
    :param create_survey:
    :return:
    """
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify deleting combo quota.")
    try:
        first_page_questions = [
            "How noisy is this neighborhood?",
            "In a typical month, about how much money, in U.S. dollars, do you spend on your cable service?",
            "Using any number from 0 to 10, where 0 is the worst health care possible and 10 is the best health care"
            " possible, what number would you use to rate all your health care in the last 12 months?",
        ]
        second_page_questions = [
            "In what state or U.S. territory are you currently registered to vote?",
            "In what county (or counties) does your target customer live?",
        ]

        # Add first page Questions
        for question in first_page_questions:
            mySurvey.myBank.searchForQuestion(mySurvey.survey_id, question)
            mySurvey.myLogic.pushQuestionToStack(question)

        # Next questions on page 2, start of Page 2
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_NewPageAddButton()

        # Add second page Questions
        for question in second_page_questions:
            mySurvey.myBank.searchForQuestion(mySurvey.survey_id, question)
            mySurvey.myLogic.pushQuestionToStack(question)

        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_Quota()
        mySurvey.myLogic.quotaSetupWizard("combo", [1, 2], [1, 4], [1, 1])
        ex = mySurvey.myLogic.checkQuotaIcon(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page quota icon appears page 1",
                                 "checks to make sure that the page quota icon appears.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of page quota icon"
        mySurvey.myCreate.go_to_page(2)
        ex = mySurvey.myLogic.checkQuotaIcon(4)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page quota icon appears page 2",
                                 "checks to make sure that the page quota icon appears.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of page quota icon"

        mySurvey.myLogic.deleteComboQuota()
        mySurvey.myLogic.click_QuotaFirstDoneButton()
        ex = mySurvey.myLogic.checkQuotaOff()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that Quota deleted or not",
                                 "checks to make sure that Quota is deleted.",
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
