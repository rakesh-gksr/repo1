from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicQuestionRandomAll/",  # report_relative_location
                               "test_logic_questionRandomizationAllQuestionsOnAllPages",  # report_file_name_prefix
                               "verify Randomizing all Questions",  # test_suite_title
                               ("This test applies page logic "
                                " question randomization of all questions "
                                " on all pages."),  # test_suite_description
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
@pytest.mark.C83920
@pytest.mark.IB
def test_logic_questionRandomizationAllQuestionsOnAllPages(create_survey):
    driver, mySurvey, report = create_survey

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
            "Q8 - How noisy is your city?",
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

        # setup question randomization on page 1
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_QuestionRandomization()
        mySurvey.myLogic.questionRandom_randomQuestions(1)

        # TODO:: no way to check for Question Randomized Icon in case of ALL questions

        # setup question randomization on page 2
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_QuestionRandomization()
        mySurvey.myLogic.click_addNewQuestionRandomization()
        mySurvey.myLogic.questionRandom_randomQuestions(2)

        # take survey in preview mode and check for randomness
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

        it = []
        for x in xrange(3):
            if x > 0:
                mySurvey.myDesign.click_preview_button()
                mySurvey.myDesign.switch_to_preview_window()
            mySurvey.myDesign.switch_to_preview_iframe()
            it.append(mySurvey.myLogic.verify_multiple_question_randomization([page1_questions, page2_questions]))
            mySurvey.myDesign.return_from_preview_window()
        ex = mySurvey.myLogic.check_for_multi_randomness(it)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Successfully verified question randomization ",
                                 "Verifies that all questions were all randomized",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify randomization of questions"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
