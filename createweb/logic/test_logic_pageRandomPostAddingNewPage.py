from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicPageRandom/",  # report_relative_location
                               "test_logic_pageRandomPostAddingNewPage",  # report_file_name_prefix
                               "verify newly added page gets randomized when all pages are selected",  # test_suite_title
                               ("This test applies page logic "
                                " page randomization on all pages and then adds a page and then checks "
                                " if all page including newly added page is randomized."),  # test_suite_description
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
@pytest.mark.pagerandom
@pytest.mark.C212959
def test_logic_pageRandomPostAddingNewPage(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE,
                             "Verify newly added page gets randomized when all pages are selected.")
    try:
        # add few pages
        pagewise_questions = [
            "How noisy is this neighborhood?",
            "In a typical month, about how much money, in U.S. dollars, do you spend on your cable service?",
            "What number would you use to rate all your health care in the last 12 months?",
        ]
        # add questions and pages
        for i, question in enumerate(pagewise_questions):
            mySurvey.myBank.searchForQuestion(mySurvey.survey_id, question)
            mySurvey.myLogic.pushQuestionToStack(question)

            # dont add new page for last question
            if i != (len(pagewise_questions) - 1):
                mySurvey.myBuilder.unfold_BuilderRegion()
                mySurvey.myBuilder.click_NewPageAddButton()

        # apply page randomization for all pages
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageRandomization()
        mySurvey.myLogic.pageRandom_randomizePages()

        # check page randomization icon before adding new page
        ex = mySurvey.myLogic.checkPagesRandomizedIcon(3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page randomization icon appears",
                                 "checks to make sure that the page randomization icon appears before adding page.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of page randomization icon before adding page"

        # add new pages
        question = "In what state or U.S. territory are you currently registered to vote?"
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, question)
        mySurvey.myLogic.pushQuestionToStack(question)

        mySurvey.myLogic.unfold_LogicRegion()

        # check page randomization icon after adding page
        ex = mySurvey.myLogic.checkPagesRandomizedIcon(4)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page randomization icon appears",
                                 "checks to make sure that the page randomization icon appears after adding page.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of page randomization icon after adding page"

        # check if page randomization works for all pages added
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
        for y in xrange(3):
            if y > 0:
                mySurvey.myDesign.click_preview_button()
                mySurvey.myDesign.switch_to_preview_window()
                mySurvey.myDesign.click_off_preview_warning()
            mySurvey.myDesign.switch_to_preview_iframe()
            for x in xrange(4):
                ex = mySurvey.myLogic.verifyPreviewPageRandomize()
                # time.sleep(3)
                report.add_report_record(ReportMessageTypes.TEST_STEP,
                                         "Successfully Verified Page " + str(x + 1) + " pass # " + str(y),
                                         "Sucessfully verified that this page is randomized.",
                                         ex,
                                         True,
                                         not ex,
                                         driver)
                assert ex, "Preview Page Verification failure"
                if x < 3:
                    ex = mySurvey.myDesign.click_preview_next_button_noFrame()
                    report.add_report_record(ReportMessageTypes.TEST_STEP, "Successfully Moved to the next page ",
                                             "Sucessfully Moved to the next page.",
                                             ex,
                                             True,
                                             not ex,
                                             driver)
                    assert ex, "Failed to move to next preview page"
                    # time.sleep(3)
                if x == 3:
                    mySurvey.myDesign.return_from_preview_window()
        ex = mySurvey.myLogic.checkForRandomness(4)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Successfully verified page randomization ",
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
