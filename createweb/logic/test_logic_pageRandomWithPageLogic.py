"""
This test case verifies that page skip logic can not be applied on randomised pages.
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
                               "test_logic_pageRandomWithPageLogic",  # report_file_name_prefix
                               "verify Randomizing all pages with page skip logic",  # test_suite_title
                               ("This test applies page skip logic "
                                " page randomization can be applied at the same time on same page"),  # test_suite_description
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
@pytest.mark.C212994
def test_logic_page_random_with_page_logic(create_survey):
    """
    Description: This test case verifies that page skip logic can not be applied on randomised pages.
    Args:
        create_survey: fixture to create empty survey

    Returns:

    """
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "To verify page skip logic can not be applied "
                                                           " on randomised pages when all Survey pages are Randomized.")
    try:
        pagewise_questions = [
            "How noisy is this neighborhood?",
            "In a typical month, about how much money, in U.S. dollars, do you spend on your cable service?",
            # "What number would you use to rate all your health care in the last 12 months?",
            # "In what state or U.S. territory are you currently registered to vote?",
            # "In what county (or counties) does your target customer live?",
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

        # add page skip logic
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        # check notice message
        ex = mySurvey.myLogic.check_exclude_random_pages_notice_shown()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that Notice is shown to notify that "
                                                               "randomised pages are not available for page skip logic",
                                 "checks that notice is displayed or not",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify notice is shown or not"

        actual_option_list = mySurvey.myLogic.get_page_skip_type_dropdown_options()
        expected_option_list = [u'-- Choose Page --', u'End of Survey', u'Disqualify Respondent']
        ex = actual_option_list == expected_option_list
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that randomised pages are not available for "
                                                               "page skip logic",
                                 "checks that randomised pages are not available for page skip logic",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify randomised pages are available for page skip logic or not"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
