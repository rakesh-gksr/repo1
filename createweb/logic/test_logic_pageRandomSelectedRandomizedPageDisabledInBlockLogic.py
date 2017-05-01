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
                               "TestLogicPageRandom/",  # report_relative_location
                               "test_logic_pageRandom",  # report_file_name_prefix
                               "verify selected randomized pages aren't showing in block logic",  # test_suite_title
                               ("This test verifies selected randomized"
                                " pages aren't showing in block logic"),  # test_suite_description
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

@pytest.mark.pageRandomization
@pytest.mark.C212939
@pytest.mark.IB
def test_logic_pageRandomSelectedRandomizedPageDisabledInBlockLogic(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify selected randomized pages aren't showing in block logic")
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
            if i < 3:
                mySurvey.myBuilder.click_NewPageAddButton()

        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageRandomization()
        mySurvey.myLogic.pageRandom_randomizePages_selected([1, 3])
        ex = mySurvey.myLogic.checkPagesRandomizedIconSelected(2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page randomization icon appears",
                                 "checks to make sure that the selected page randomization icon appears.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of page randomization icon"

        mySurvey.myLogic.click_blockRandomizationButton()
        mySurvey.myLogic.click_blockRandom_newBlock()
        # call to function that verifies that page numbers are disables in block randomization or not
        # pass randomized pages in list
        ex = mySurvey.myLogic.verifyBlockRandomoizationOnRandomizedPages([1, 3])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that pages 1 and 3 are disabled",
                                 "checks to make sure that page skip logic cannot be applied to pages "
                                 "1 and 3 because they are already randomized",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify disabled pages in page skip logic"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
