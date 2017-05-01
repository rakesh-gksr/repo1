"""
Quota type: Combination quota
Test case for verifying back navigation
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
                               "test_logic_comboQuota",  # report_file_name_prefix
                               "verify back navigation for combo quota",  # test_suite_title
                               ("This test verifies back navigation "
                                " on combo quota"),  # test_suite_description
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
@pytest.mark.C83906
@pytest.mark.C83909
@pytest.mark.IB
def test_logic_comboQuotaVerifyBackNavigation(create_survey):
    """
    Test Case Name : combination quota: verify back navigation on combination quota
    :param create_survey:
    :return:
    """
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify back navigation for combo quota.")
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
        mySurvey.myLogic.attempt_comboQuotaSetupWizard("combo", [1, 2], [1, 4], [1, 1])

        ex = mySurvey.myLogic.checkQuotaOff()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Combo quota back navigation",
                                 "checks to make sure that Quota is not added.(quota status off)",
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
