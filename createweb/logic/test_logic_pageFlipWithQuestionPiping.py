from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest

__author__ = 'Rakesh Jain'


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicPageFlipWithQuestionPiping/",  # report_relative_location
                               "test_logic_pageFlipWithQuestionPiping",  # report_file_name_prefix
                               "To verify Page Randomization does not works with Piping when all Survey pages"
                               " are Fliped.",  # test_suite_title
                               ("This test verify page randomization does not works with quesiton piping when "
                                "all Survey pages are Fliped."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.pageRandomization
@pytest.mark.IB
@pytest.mark.C213003
def test_logic_pageFlip(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify Page Randomization does not works with Piping "
                                                           "when all Survey pages are Flipped.")
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
                "Test",
                [
                    "upto 10$",
                    "more than 10$",
                ],
            ],
            [
                "Using any number from 0 to 10, where 0 is the worst health care possible and 10"
                " is the best health care possible, what number would you use to rate all "
                "your health care in the last 12 months?",
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
                    "India",
                    "Pak",
                ],
            ],
        ]

        i = 0
        for question, answer_rows in survey_questions:
            # add one question on each page
            mySurvey.myBank.searchForQuestion(mySurvey.survey_id, question, answer_rows)
            mySurvey.myLogic.pushQuestionToStack(question)
            mySurvey.myBuilder.unfold_BuilderRegion()
            i += 1
            if i < 5:
                mySurvey.myBuilder.click_NewPageAddButton()

        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageRandomization()
        mySurvey.myLogic.pageRandom_flipPages()
        ex = mySurvey.myLogic.checkPagesRandomizedIcon()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page randomization icon appears",
                                 "checks to make sure that the page randomization icon appears.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of page randomization icon"
        # code to edit the second question
        mySurvey.myQuestion.click_on_question_to_edit(2)
        # code to check whether question piping can be applied on randomized page's question or not
        ex = mySurvey.myQuestion.check_question_piping_on_randomized_pages()

        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that Page Randomization does not works with "
                                                               "Question Piping when Selected Survey pages are Flipped",
                                 "checks to make sure that the page randomization does not works with question piping.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Page Randomization does not works with Question Piping when " \
                   "Selected Survey pages are Flipped"

        # code to remove page randomization and verify that question piping work fine

        mySurvey.myLogic.click_PageRandomization()
        # delete page randomization
        mySurvey.myLogic.delete_pageRandomization()
        # check for randomize icon not present on each page
        ex = mySurvey.myLogic.checkPagesRandomizedIcon(False)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page randomization icon do not appears",
                                 "checks to make sure that the page randomization do not icon appears.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of page randomization icon"
        # check for page randomization status
        ex = mySurvey.myLogic.verifyPageRandomizationStatus('Off')
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Page Randomization status.",
                                 "checks to verify Randomization status is off.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Unable to verify Page Randomization status"

        # code to edit the second question
        mySurvey.myQuestion.click_on_question_to_edit(2)
        # code to add question piping from question 1 to question 2
        ex = mySurvey.myQuestion.addPipingtoQuestion(1, 0)

        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that Question Piping works fine "
                                                               "if page is not randomized",
                                 "checks to make sure that the question piping works fine if page is not randomized",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Question Piping works fine if page is not randomized"


    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
