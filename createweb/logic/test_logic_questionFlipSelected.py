from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicQuestionFlipSelected/",  # report_relative_location
                               "test_logic_QuestionFlipSelected",  # report_file_name_prefix
                               "verify flipping Selected Questions",  # test_suite_title
                               ("This test applies page logic "
                                " question randomization and as a random chance "
                                " to invert the selected survey questions."),  # test_suite_description
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


def test_logic_questionFlipSelected(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify applying selected question flip page logic.")
    try:
        # Question 1
        # pylint:disable=similarities

        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "How noisy is this neighborhood?")
        mySurvey.myLogic.pushQuestionToStack("How noisy is this neighborhood?")
        # Question 2
        mySurvey.myBank.searchForQuestion(mySurvey.survey_id,
                                          "In a typical month, about how much money, in U.S. dollars, do you spend on your cable service?")
        mySurvey.myLogic.pushQuestionToStack(
            "In a typical month, about how much money, in U.S. dollars, do you spend on your cable service?")
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
        mySurvey.myLogic.questionRandom_flipQuestions_selected([1, 3, 5], 1, 5)
        ex = mySurvey.myLogic.checkQuestionsRandomizedIconSelected()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that Question randomization icon appears",
                                 "checks to make sure that the Question randomization icon appears.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of Question randomization icon"
        attemptCounter = 0
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
            if attemptCounter == 0:
                mySurvey.myDesign.click_off_preview_warning()
            mySurvey.myDesign.switch_to_preview_iframe()
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
                    report.add_report_record(ReportMessageTypes.TEST_STEP,
                                             "Successfully Verified Question " + str(x + 1),
                                             "Sucessfully verified that this Question is in the proper flipped order.",
                                             ex,
                                             True,
                                             not ex,
                                             driver)
                    assert ex, "Preview Page Verification failure"
                    # time.sleep(1)
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
