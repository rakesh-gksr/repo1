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
                               "TestLogicPageRandomSelected/",  # report_relative_location
                               "test_logic_pageRandomOnSelectedWithPiping",  # report_file_name_prefix
                               "verify Randomizing selected pages with piping",  # test_suite_title
                               ("This test applies page logic "
                                " page randomization on selected pages, piping in page 2 question "
                                "and as a random chance to randomize the survey pages."), # test_suite_description
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
@pytest.mark.C213002
def test_logic_page_random_on_selected_with_piping(create_survey):
    """
    Description: This test case verifies that piping is not enabled when page randomisation is on and after turning off randomisation
 the piping feature should be enabled. Page Randomisation for selected pages.
    Args:
        create_survey: fixture to create empty survey

    Returns:

    """
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify applying page random page logic for selected pages.")
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
        # Add questions on page 1
        i = 0
        for question, answer_rows in survey_questions:
            mySurvey.myBank.searchForQuestion(mySurvey.survey_id, question, answer_rows)
            mySurvey.myLogic.pushQuestionToStack(question)
            mySurvey.myBuilder.unfold_BuilderRegion()
            i += 1
            if i < 5:
                mySurvey.myBuilder.click_NewPageAddButton()

        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageRandomization()
        mySurvey.myLogic.pageRandom_randomizePages_selected([1, 3, 5])
        ex = mySurvey.myLogic.checkPagesRandomizedIconSelected()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page randomization icon appears",
                                 "It checks that on selected pages randomization icon appears.",
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
                                 "It checks that the question piping is disabled when page randomization on.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Piping when selected Survey pages are Randomized"

        # remove page randomisation on selected pages
        mySurvey.myLogic.click_PageRandomization()
        # delete page randomization
        mySurvey.myLogic.delete_pageRandomization()
        # check for randomize icon presence on each page
        ex = mySurvey.myLogic.checkPagesRandomizedIconSelected(0)
        # ex = mySurvey.myLogic.checkPageRandomizedIconNotSelected()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page randomization icon "
                                                               "do not appears for any page",
                                 "It checks that the page randomization icon doesn't appear now.",
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

        # add piping after removing page randomisation on selected pages.
        mySurvey.myQuestion.click_on_question_to_edit(2)
        ex = mySurvey.myQuestion.addPipingtoQuestion(1, 0)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Successfully added piping when randomization "
                                                               "is removed",
                                 "Verifies that all questions piping is enabled when randomization is removed",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add piping when randomization of selected pages are removed"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
