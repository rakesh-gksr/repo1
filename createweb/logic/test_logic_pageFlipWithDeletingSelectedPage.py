from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest

__author__ = 'Rakesh'


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicPageFlipWithDeletingSelectedPage/",  # report_relative_location
                               "test_logic_pageFlipWithDeletingSelectedPages",  # report_file_name_prefix
                               "To verify page Flip after applying logic to all survey pages and deleting "
                               "a selected page",  # test_suite_title
                               ("This test applies page logic "
                                " page randomization, then delete page no 4 and then verify that page "
                                "randomization work fine without any error."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d,"
                                                                                                      " %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.pageRandomization
@pytest.mark.IB
@pytest.mark.C212992
def test_logic_pageFlipWithDeletingSelectedPages(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "To verify page Flip after applying logic to all "
                                                           "survey pages and deleting a selected page")
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
        # Code to delete the page no 4
        ex = mySurvey.myCreate.nuke_page(4)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page number 4 with all questions deleted "
                                                               "from survey",
                                 "checks to make sure that the page number 4 with all questions deleted "
                                                               "from survey.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to delete page no 4"
        if ex:
            # code to delete the question no 4 from stack
            ex = mySurvey.myLogic.deleteQuestionInQuestionStack("In what state or U.S. territory are you currently "
                                                                "registered to vote?")
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that question deleted from question stack",
                                     "checks to make sure that the question deleted from question stack.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify the question deleted from question stack"


        attemptCounter = 0
        while attemptCounter < 4:
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
            for x in xrange(4):
                ex = mySurvey.myLogic.verifyPreviewPage()
                # time.sleep(1)
                if not ex:
                    attemptCounter += 1
                    mySurvey.myDesign.return_from_preview_window()
                    break
                else:
                    report.add_report_record(ReportMessageTypes.TEST_STEP, "Successfully Verified Page " + str(x),
                                             "Sucessfully verified that this page is in the proper flipped order.",
                                             ex,
                                             True,
                                             not ex,
                                             driver)
                    assert ex, "Preview Page Verification failure"
                    if x != 3:
                        ex = mySurvey.myDesign.click_preview_next_button_noFrame()
                        report.add_report_record(ReportMessageTypes.TEST_STEP, "Successfully Moved to the next page ",
                                                 "Sucessfully Moved to the next page.",
                                                 ex,
                                                 True,
                                                 not ex,
                                                 driver)
                        assert ex, "Failed to move to next preview page"
                    # time.sleep(1)
            if len(mySurvey.myLogic.questionStack) == 0:
                previewBool = True
                break

        if attemptCounter < 4 and previewBool:
            myBool = True
        else:
            myBool = False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Successfully Verified All Pages ",
                                 "Sucessfully verified that all pages are in the proper flipped order.",
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
