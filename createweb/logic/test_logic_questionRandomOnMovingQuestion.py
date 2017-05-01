from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from smsdk.qafw.rpage import pyramidsurveypage as Spage
import traceback
import pytest

import time


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicQuestionRandomSelected/",  # report_relative_location
                               "test_logic_questionRandomizationOnQuestionsMove",  # report_file_name_prefix
                               "verify Randomizing selected Questions",  # test_suite_title
                               ("This test applies page logic "
                                " question randomization and then question is moved "
                                " from another page to test if question is seen in "
                                " Question Randomization menu."),  # test_suite_description
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


@pytest.mark.question_random
@pytest.mark.C83925
@pytest.mark.IB
def test_logic_questionRandomizationOnQuestionsMove(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify applying page random question logic.")
    try:
        page1_questions = [
            "Q1 - How noisy is this neighborhood?",
            "Q2 - In a typical month, about how much money, in U.S. dollars, do you spend on your cable service?",
            "Q3 - In what state or U.S. territory are you currently registered to vote?",
            "Q4 - In what county (or counties) does your target customer live?",
            "Q5 - In a typical month, about how much money, in U.S. dollars, do you spend on your mobile service?",
        ]
        page2_questions = [
            "Q6 - Do you have any other comments, questions, or concerns?",
            "Q7 - How noisy is this neighborhood?",
        ]

        # Add questions in page 1
        for question in page1_questions:
            mySurvey.myBank.searchForQuestion(mySurvey.survey_id, question)
            mySurvey.myLogic.pushQuestionToStack(question)

        mySurvey.myBuilder.click_NewPageAddButton()

        # Add questions in page 2
        for question in page2_questions:
            mySurvey.myBank.searchForQuestion(mySurvey.survey_id, question)
            mySurvey.myLogic.pushQuestionToStack(question)

        # Add Question Randomization on selected questions
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_QuestionRandomization()
        mySurvey.myLogic.questionRandom_randomQuestions_selected([1, 3, 5], 1)

        ex = mySurvey.myLogic.checkQuestionsRandomizedIconSelected(3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that Question randomization icon appears",
                                 "checks to make sure that the Question randomization icon appears for selected page.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of Question randomization icon"

        # move one question from Page 2 to Page 1
        mySurvey.myQuestion.click_on_question_to_edit(6)
        mySurvey.myQuestion.click_question_move_tab()
        mySurvey.myLogic.moveQuestion(1, 1)

        # check if new question is available under Question Randomization menu
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_QuestionRandomization()
        expected_questions_on_page1 = [] + page1_questions
        expected_questions_on_page1.insert(1, page2_questions[0])
        ex = mySurvey.myLogic.questionRandom_randomQuestions_checkAvailableQuestions(1, expected_questions_on_page1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that Question randomization menu has question which is moved",
                                 "checks to make sure that the question appears in Question randomization menu post move.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of new question (moved from another page) in Question Randomization menu"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
