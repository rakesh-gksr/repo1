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
                               "test_logic_pageRandomIconsWorking",  # report_file_name_prefix
                               "verify clicking on page randomization icon on multiple pages",  # test_suite_title
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
def test_logic_pageRandomIconsWorking(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE,
                             "Verify clicking on page randomization icon on multiple pages.")
    try:
        # add few pages
        pagewise_questions = [
            "How noisy is this neighborhood?",
            "In a typical month, about how much money, in U.S. dollars, do you spend on your cable service?",
            "What number would you use to rate all your health care in the last 12 months?",
            "In what state or U.S. territory are you currently registered to vote?",
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
        ex = mySurvey.myLogic.checkPagesRandomizedIcon(4)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page randomization icon appears",
                                 "checks to make sure that the page randomization icon appears for all pages.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of page randomization icon before adding page"

        ex = mySurvey.myLogic.checkPageRandomizationIconAppliedAndWorking([1, 2, 3, 4])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page randomization icon works",
                                 "checks to make sure that the page randomization icon appears and works for all pages.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence and working of page randomization icon for all pages"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
