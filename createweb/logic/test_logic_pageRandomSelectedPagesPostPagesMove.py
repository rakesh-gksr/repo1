from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicPageRandomSelected/",  # report_relative_location
                               "test_logic_pageRandomSelectedPagesPostPagesMove",  # report_file_name_prefix
                               "verify page randomization with selected pages and then moving those pages",  # test_suite_title
                               ("This test applies page logic"
                                " page randomization for selected pages"
                                " checks if it gets updated"
                                " post moving those pages."),  # test_suite_description
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
@pytest.mark.C212958
def test_logic_pageRandomSelectedPagesPostPagesMove(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify page randomization with selected pages after moving pages.")
    try:
        pagewise_questions = [
            "How noisy is this neighborhood?",
            "In a typical month, about how much money, in U.S. dollars, do you spend on your cable service?",
            "What number would you use to rate all your health care in the last 12 months?",
            "In what state or U.S. territory are you currently registered to vote?"
        ]
        # add questions and pages
        for i, question in enumerate(pagewise_questions):
            mySurvey.myBank.searchForQuestion(mySurvey.survey_id, question)
            mySurvey.myLogic.pushQuestionToStack(question)

            # dont add new page for last question
            if i != (len(pagewise_questions) - 1):
                mySurvey.myBuilder.unfold_BuilderRegion()
                mySurvey.myBuilder.click_NewPageAddButton()

        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageRandomization()

        # pytest.set_trace()
        # set the page randomization on selected pages for page 1 and 3
        mySurvey.myLogic.pageRandom_randomizePages_selected([1, 3])

        # check for page randomization icons
        ex = mySurvey.myLogic.checkPagesRandomizedIconSelected(2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page randomization icon appears",
                                 "checks to make sure that the selected page randomization icon appears.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of page randomization icon"

        # move pages
        mySurvey.myLogic.movePage(1, 2, "after")
        mySurvey.myLogic.movePage(3, 4, "after")

        # check selected page randomization selected pages post moving pages
        mySurvey.myLogic.click_PageRandomization()
        ex = mySurvey.myLogic.pageRandom_randomizePages_verifySelected([2, 4], len(pagewise_questions))
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page randomization selected pages gets updated post move",
                                 "checks to make sure that after moving pages, selected page randomization list is updated.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify correct page list shown for page randomization option post moving pages."

        ex = mySurvey.myLogic.checkPagesRandomizedIconSelected(2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page randomization icon appears",
                                 "checks to make sure that the selected page randomization icon appears.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of page randomization icon"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
