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
                               "TestLogicQuestionFlip/",  # report_relative_location
                               "test_logic_QuestionFlip",  # report_file_name_prefix
                               "verify flipping all Questions",  # test_suite_title
                               ("This test applies page logic "
                                " question randomization and as a random chance "
                                " to invert the survey questions."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.BVT})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename

@pytest.mark.questionRandomization
@pytest.mark.C83926
@pytest.mark.IB
def test_logic_questionFlipQuestionNumberUpdateOnEachPage(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify applying question flip page logic.")
    try:
        # set survey question and option used for test case
        survey_questions = [
            [
                "How noisy is this neighborhood?",
                [
                    "Very Noisy",
                    "Silent",
                ],
            ],
            [
                "In a typical month, about how much money, in U.S. dollars, do you spend on your cable service?",
                [
                    "upto 10$",
                    "more than 10$",
                ],
            ],
            [
                "Using any number from 0 to 10, where 0 is the worst health care possible and 10"
                " is the best health care possible, what number would you use to rate all your health care in the last 12 months?",
                [
                    "0",
                    "1",
                ],
            ],
            [
                "In what state or U.S. territory are you currently registered to vote?",
                [
                    "LA",
                    "LV",
                ],
            ],
            [
                "In what county (or counties) does your target customer live?",
                [
                    "LA",
                    "LV",
                ],
            ],
        ]
        # Add questions on page 1
        for question, answer_rows in survey_questions:
            mySurvey.myBank.searchForQuestion(mySurvey.survey_id, question, answer_rows)
            mySurvey.myLogic.pushQuestionToStack(question)

        # start of Page 2
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_NewPageAddButton()

        # Add questions on page 2
        for question, answer_rows in survey_questions:
            mySurvey.myBank.searchForQuestion(mySurvey.survey_id, question, answer_rows)
            mySurvey.myLogic.pushQuestionToStack(question)

        mySurvey.myLogic.unfold_LogicRegion()
        numberOfPages = 2
        for pages in xrange(numberOfPages):
            pages += 1
            mySurvey.myLogic.click_QuestionRandomization()
            if pages > 1:
                mySurvey.myLogic.click_newQuestionRandom()
            mySurvey.myLogic.questionRandom_flipQuestions(pages)
            ex = mySurvey.myLogic.checkQuestionsRandomizedIcon()
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that Question randomization icon appears",
                                     "checks to make sure that the Question randomization icon appears.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify presence of Question randomization icon"

        mySurvey.myOptions.unfold_OptionsRegion()
        mySurvey.myLogic.selectQuestionNumberSetting(2)
        ex = mySurvey.myLogic.verifyQuestionNumbering()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that Question numbers are updated",
                                 "checks to make sure that the Question numbers are updated",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify updated numbers"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
