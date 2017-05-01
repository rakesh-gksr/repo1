"""
This test case verifies that piping is not enabled when page randomisation is on and after turning off randomisation
 the piping feature should be enabled
"""
from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest

__author__ = 'sushrut'


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicPageRandom/",  # report_relative_location
                               "test_logic_pageRandomWithPiping",  # report_file_name_prefix
                               "verify Randomizing all pages with piping",  # test_suite_title
                               ("This test applies page logic "
                                " page randomization, piping in page 2 question and as a random chance "
                                " to randomize the survey pages."),  # test_suite_description
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


@pytest.mark.pagelogic
@pytest.mark.IB
@pytest.mark.C213001
def test_logic_page_random_with_piping(create_survey):
    """
    Description: This test case verifies that piping is not enabled when page randomisation is on and after turning off randomisation
 the piping feature should be enabled. Page Randomisation for all pages.
    Args:
        create_survey: fixture to create empty survey

    Returns:

    """
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "To verify piping doesn't work "
                                                           " when all Survey pages are Randomized.")
    try:
        pagewise_questions = [
            "How noisy is this neighborhood?",
            "In a typical month, about how much money, in U.S. dollars, do you spend on your cable service?",
            "What number would you use to rate all your health care in the last 12 months?",
            "In what state or U.S. territory are you currently registered to vote?",
            "In what county (or counties) does your target customer live?",
        ]
        i = 0
        for question in pagewise_questions:
            mySurvey.myBank.searchForQuestion(mySurvey.survey_id, question)
            mySurvey.myLogic.pushQuestionToStack(question)
            mySurvey.myBuilder.unfold_BuilderRegion()
            i += 1
            if i < 5:
                mySurvey.myBuilder.click_NewPageAddButton()

        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageRandomization()
        mySurvey.myLogic.pageRandom_randomizePages()
        ex = mySurvey.myLogic.checkPagesRandomizedIcon()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page randomization icon appears",
                                 "checks to make sure that the page randomization icon appears.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of page randomization icon"

        # edit question on page 2 and try to insert piping
        mySurvey.myQuestion.click_on_question_to_edit(2)
        ex = mySurvey.myQuestion.check_question_piping_on_randomized_pages()

        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that piping does not works with "
                                                               "Page randomization",
                                 "It checks that when page randomization is enabled,"
                                 " the question piping is not allowed.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Piping when all Survey pages are Randomized"

        # remove  page randomisation and then add piping
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageRandomization()
        # delete page randomization
        mySurvey.myLogic.delete_pageRandomization()
        # check for randomize icon presence on each page
        ex = mySurvey.myLogic.checkPagesRandomizedIcon(False)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page randomization icon does not appear",
                                 "checks that the page randomization icon doesn't appear.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of page randomization icon"

        # add piping after removing page randomisation on all pages.
        mySurvey.myQuestion.click_on_question_to_edit(2)
        ex = mySurvey.myQuestion.addPipingtoQuestion(1, 0)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Successfully added piping when randomization "
                                                               "is removed",
                                 "Verifies that question piping is enabled when page randomization is removed",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add piping page when randomization of all pages are removed"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
