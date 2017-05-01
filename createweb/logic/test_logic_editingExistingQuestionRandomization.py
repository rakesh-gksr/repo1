from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest
import time
import pdb

'''
__author__ = 'rajat'
'''


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicEditingExistingQuestionRandomization.py/",  # report_relative_location
                               "test_logic_editingExistingQuestionRandomization",  # report_file_name_prefix
                               "verify editing existing question randomization",  # test_suite_title
                               ("This test applies question logic "
                                " editing existing question randomization "
                                " to randomize the selected survey questions."),  # test_suite_description
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
def test_logic_editingExistingQuestionRandomization(create_survey):
    driver, mySurvey, report = create_survey

    answer_rows = ["Fine", "Very Good", "Not well"]
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify editing existing question randomization.")
    try:
        # Question 1

        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "How are you doing?", answer_rows)
        mySurvey.myLogic.pushQuestionToStack("How are you doing?")
        # Question 2
        mySurvey.myBank.searchForQuestion(mySurvey.survey_id,
                                          "How was the examination paper?",answer_rows)
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
        mySurvey.myLogic.questionRandom_randomQuestions_selected([1, 3, 5], 1)

        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Open a new survey and click the preview button",
                                 "Opens a new Survey and clicks the preview button.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)

        mySurvey.myDesign.click_off_preview_warning()

        ex = mySurvey.myLogic.verifyPreviewPageRandomQuestions(1)
        mySurvey.myDesign.return_from_preview_window()
        mySurvey.myLogic.click_QuestionRandomization()
        mySurvey.myLogic.click_addNewQuestionRandomization()

        mySurvey.myLogic.questionRandom_randomQuestions_selected([1, 3, 4], 1)
        #pdb.set_trace()
        ex = mySurvey.myLogic.checkQuestionsRandomizedIconSelected(2)
        assert ex, "True"

    except:
        assert False, traceback.format_exc()
