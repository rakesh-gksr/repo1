from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest
import time

'''
__author__ = 'rajat'
'''
# TESTRAIL ID - C83917
@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicRemovingQuestionRandomizationOnAllQuestionsOnSelectedPages.py/",  # report_relative_location
                               "test_logic_removingQuestionRandomizationOnAllQuestionsOnSelectedPages",  # report_file_name_prefix
                               "verify removing question randomization on all questions of selected pages",  # test_suite_title
                               ("This test applies question logic "
                                " removing question randomization on all questions of selected pages. "
                                " to remove question randomization on all questions of selected pages"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os

    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime(
        "%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()

    request.addfinalizer(fin)
    return report, testcasename

@pytest.mark.IB
def test_logic_removingQuestionRandomizationOnAllQuestionsOnSelectedPages(create_survey):
    driver, mySurvey, report = create_survey

    answer_rows = ["Fine", "Very Good", "Not well"]
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify removing question randomization on all questions of selected pages.")
    try:
        # Question 1

        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "Whassup?", answer_rows)
        mySurvey.myLogic.pushQuestionToStack("Whassup?")
        # Question 2
        mySurvey.myBank.searchForQuestion(mySurvey.survey_id,
                                          "How was new college?",answer_rows)
        mySurvey.myLogic.pushQuestionToStack(
            "IWhat is your monthly expenditure in dollars?")
        # Question 3
        mySurvey.myBank.searchForQuestion(
            mySurvey.survey_id,
            "Using any number from 0 to 10, where 0 is the worst health care possible and 10"
            " is the best health care possible, what number would you use to rate all your health care in the last 12 months?")
        mySurvey.myLogic.pushQuestionToStack(
            "Using any number from 0 to 10, where 0 is the worst health care possible and 10"
            " is the best health care possible, what number would you use to rate all your health care in the last 12 months?")
        # Question 4
        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "In what state or U.S. territory are you currently registered to vote?")
        mySurvey.myLogic.pushQuestionToStack("In what state or U.S. territory are you currently registered to vote?")
        # Question 5
        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "In what county (or counties) does your target customer live?")
        mySurvey.myLogic.pushQuestionToStack("In what county (or counties) does your target customer live?")

        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_QuestionRandomization()
        mySurvey.myLogic.questionRandom_randomQuestions(1)
        mySurvey.myLogic.delete_question_randomization(1)
        ex = mySurvey.myLogic.verifyQuestionrandomizationStatus('OFF')
        print ex
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify removing question randomization on all questions of selected pages.",
                                 "checks to verify removing question.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)

        assert ex, "True"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
