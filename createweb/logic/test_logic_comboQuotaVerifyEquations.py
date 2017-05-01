"""
Quota type : combination quota
Test case for verifying equations are getting saved correctly or not
"""

from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest
import time

__author__ = 'mangesh'

@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicComboQuota/",  # report_relative_location
                               "test_logic_comboQuota_verify_group_equation",  # report_file_name_prefix
                               "verify group equations saved correctly or not",  # test_suite_title
                               ("This test verifies group equations saved properly or not "),  # test_suite_description
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
@pytest.mark.C83911
@pytest.mark.Infobeans
def test_logic_comboQuotaVerifyEquations(create_survey):
    """
    Test case name : combination quota: check that equations are getting saved correctly
    :param create_survey:
    :return:
    """
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify group equations saved correctly or not.")
    try:

        first_page_questions = [
            "How noisy is this neighborhood?",
            "In a typical month, about how much money, in U.S. dollars, do you spend on your cable service?",
            "Using any number from 0 to 10, where 0 is the worst health care possible and 10 is the best health care"
            " possible, what number would you use to rate all your health care in the last 12 months?",
        ]
        # parameters that has to be passed for searchForQuestion function
        answers = ["Very noisy", "Somewhat noisy", "not at all"]
        new_groups = [1, 2]
        answers_for_group = [2, 3]
        second_page_questions = [
            "In what state or U.S. territory are you currently registered to vote?",
            "In what county (or counties) does your target customer live?",
        ]

        # Add first page Questions
        for question in first_page_questions:
            mySurvey.myBank.searchForQuestion(mySurvey.survey_id, question, answers)
            mySurvey.myLogic.pushQuestionToStack(question)

        # Next questions on page 2, start of Page 2
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_NewPageAddButton()

        # Add second page Questions
        for question in second_page_questions:
            mySurvey.myBank.searchForQuestion(mySurvey.survey_id, question, answers)
            mySurvey.myLogic.pushQuestionToStack(question)

        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_Quota()
        mySurvey.myLogic.quotaSetupWizard_verifyEquations([1, 2], [1, 4], [1, 1])
        for i in new_groups:
            mySurvey.myLogic.addAnotherAnswerGroup(i)
            mySurvey.myLogic.selectAnswersForGroup(answers_for_group)
        mySurvey.myLogic.click_assignValuesButton()
        mySurvey.myLogic.quotaSetupChooseQnswergroup([1, 4], "Group 1")
        mySurvey.myLogic.click_EditEquationButton(2)
        ex = mySurvey.myLogic.verifySelectedGroup("Group 1")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that combination quota equations are get save or not",
                                 "checks to make sure that combination quota equations are getting saved correctly.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to equations values"
        mySurvey.myLogic.click_AddEquationButton()
        mySurvey.myLogic.quotaSetupChooseQnswergroup([1, 4], "Group 2")
        mySurvey.myLogic.click_EditEquationButton(3)
        ex = mySurvey.myLogic.verifySelectedGroup("Group 2")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that combination quota equations are get save or not",
                                 "checks to make sure that combination quota equations are getting saved correctly.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)

        assert ex, "Failed to equations values"


    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
