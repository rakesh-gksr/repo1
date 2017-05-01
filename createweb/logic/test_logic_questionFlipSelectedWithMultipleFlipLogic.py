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
                               "TestLogicQuestionFlipSelected/",  # report_relative_location
                               "test_logic_QuestionFlipSelected",  # report_file_name_prefix
                               "verify flipping Selected Questions with multiple flip",  # test_suite_title
                               ("This test applies question flip logic"
                                " to selected question with multiple flips"),  # test_suite_description
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

@pytest.mark.questionRandomization
@pytest.mark.C83924
@pytest.mark.IB
def test_logic_questionFlipSelectedWithMultipleFlipLogic(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify applying selected question"
                                                           " flip page logic with multiple flips.")
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
                " is the best health care possible, what number would you use to rate all your"
                " health care in the last 12 months?",
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

        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_QuestionRandomization()
        mySurvey.myLogic.questionRandom_flipQuestions_selected([1, 3, 5], 1, 5)
        ex = mySurvey.myLogic.checkQuestionsRandomizedIconSelected()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that Question randomization icon appears",
                                 "checks to make sure that the Question randomization icon appears.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of Question randomization icon"

        # Add page 2, start of Page 2
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_NewPageAddButton()

        # Add questions on page 2
        for question, answer_rows in survey_questions:
            mySurvey.myBank.searchForQuestion(mySurvey.survey_id, question, answer_rows)
            mySurvey.myLogic.pushQuestionToStack(question)

        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_QuestionRandomization()
        mySurvey.myLogic.click_newQuestionRandom()
        mySurvey.myLogic.questionRandom_flipQuestions_selected([6, 8, 10], 2, 5)
        ex = mySurvey.myLogic.checkQuestionsRandomizedIconSelected(6)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that Question randomization icon appears",
                                 "checks to make sure that the Question randomization icon appears.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of Question randomization icon"

        attemptCounter = 0
        flag = 0
        while attemptCounter < 5:
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
            mySurvey.myDesign.switch_to_preview_iframe()
            if flag == 0:
                for x in xrange(5):
                    # time.sleep(1)
                    ex = mySurvey.myLogic.verifyPreviewPageQuestionsSelected(x)
                    # time.sleep(1)
                    if not ex:
                        attemptCounter += 1
                        mySurvey.myLogic.resetPageRotateCounter()
                        mySurvey.myDesign.return_from_preview_window()
                        break
                    else:
                        flag = 1
                        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                                 "Successfully Verified Page 1 Question " + str(x + 1),
                                                 "Sucessfully verified that this Question is in the proper flipped order.",
                                                 ex,
                                                 True,
                                                 not ex,
                                                 driver)
                        assert ex, "Preview Page Verification failure"
            if flag == 1:
                ex = mySurvey.myDesign.click_preview_next_button_noFrame()
                report.add_report_record(ReportMessageTypes.TEST_STEP, "Successfully Moved to the next page ",
                                         "Sucessfully Moved to the next page.",
                                         ex,
                                         True,
                                         not ex,
                                         driver)
                assert ex, "Failed to move to next preview page"

                for x in xrange(5):
                    ex = mySurvey.myLogic.verifyPreviewPageQuestionsSelected(x)
                    if not ex:
                        attemptCounter += 1
                        mySurvey.myDesign.return_from_preview_window()
                        break
                    else:
                        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                                 "Successfully Verified Page 2 Question " + str(x + 1),
                                                 "Sucessfully verified that this Question is in the proper flipped order.",
                                                 ex,
                                                 True,
                                                 not ex,
                                                 driver)
                        assert ex, "Preview Page Verification failure"

            if len(mySurvey.myLogic.pageRotate) == 0:
                previewBool = True
                break
        if attemptCounter < 5 and previewBool:
            myBool = True
        else:
            myBool = False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Successfully Verified All Questions ",
                                 "Sucessfully verified that all Questions are in the proper flipped order.",
                                 myBool,
                                 True,
                                 not myBool,
                                 driver)
        assert myBool, "Verification failure, too many attempts failed to check for page flip"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
