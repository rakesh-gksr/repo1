from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicPageRotateSelected/",  # report_relative_location
                               "test_logic_pageRotateSelected",  # report_file_name_prefix
                               "verify Rotating all pages",  # test_suite_title
                               ("This test applies page logic "
                                " page randomization and as a random chance "
                                " to rotate selected survey pages."),  # test_suite_description
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


def test_logic_pageRotateSelected(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify applying page rotate page logic to selected pages.")
    try:
        # page1

        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "How noisy is this neighborhood?")
        mySurvey.myLogic.pushQuestionToStack("How noisy is this neighborhood?")
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_NewPageAddButton()
        # page2

        mySurvey.myBank.searchForQuestion(mySurvey.survey_id,
                                          "In a typical month, about how much money, in U.S. dollars, do you spend on your cable service?")
        mySurvey.myLogic.pushQuestionToStack(
            "In a typical month, about how much money, in U.S. dollars, do you spend on your cable service?")
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_NewPageAddButton()
        # page3

        mySurvey.myBank.searchForQuestion(
            mySurvey.survey_id,
            "Using any number from 0 to 10, where 0 is the worst health care possible and 10"
            " is the best health care possible, what number would you use to rate all your health care in the last 12 months?")
        mySurvey.myLogic.pushQuestionToStack(
            "Using any number from 0 to 10, where 0 is the worst health care possible and 10"
            " is the best health care possible, what number would you use to rate all your health care in the last 12 months?")
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_NewPageAddButton()
        # page4

        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "In what state or U.S. territory are you currently registered to vote?")
        mySurvey.myLogic.pushQuestionToStack("In what state or U.S. territory are you currently registered to vote?")
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_NewPageAddButton()
        # page5

        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "In what county (or counties) does your target customer live?")
        mySurvey.myLogic.pushQuestionToStack("In what county (or counties) does your target customer live?")

        page_counts = mySurvey.myCreate.get_num_pages()
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageRandomization()
        mySurvey.myLogic.pageRandom_rotatePages_selected([1, 3, 5])
        ex = mySurvey.myLogic.checkPagesRandomizedIconSelected()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page randomization icon appears",
                                 "checks to make sure that the page randomization icon appears.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of page randomization icon"
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
        for x in xrange(page_counts):
            if x == 0:
                mySurvey.myLogic.PageRotateStartingPageSelected([1, 3, 5], 5)
            # time.sleep(1)
            ex = mySurvey.myLogic.verifyPreviewPageRotate()
            # time.sleep(1)
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Successfully Verified Page " + str(x + 1),
                                     "Sucessfully verified that this page is in the proper rotated order.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Preview Page Verification failure"
            if x < (page_counts-1):
                ex = mySurvey.myDesign.click_preview_next_button_noFrame()
                report.add_report_record(ReportMessageTypes.TEST_STEP, "Successfully Moved to the next page ",
                                         "Sucessfully Moved to the next page.",
                                         ex,
                                         True,
                                         not ex,
                                         driver)
                assert ex, "Failed to move to next preview page"
                # time.sleep(1)
        if len(mySurvey.myLogic.pageRotate) == 0:
            testSuccess = True
        else:
            testSuccess = False
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Successfully verified page rotation for selected questions",
                                 "Verifies that all questions were in a proper rotated order",
                                 testSuccess,
                                 True,
                                 not testSuccess,
                                 driver)
        assert testSuccess, "Failed to verify rotation of selected questions"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()