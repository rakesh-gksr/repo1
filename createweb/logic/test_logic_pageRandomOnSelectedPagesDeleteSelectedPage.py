from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest
import time

__author__ = 'mangesh'

@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicPageRandomSelected/",  # report_relative_location
                               "test_logic_pageRandomSelected",  # report_file_name_prefix
                               "To verify page randomization after applying logic and deleting selected page.",  # test_suite_title
                               ("This test verifies remove page randomization with selected pages"),  # test_suite_description
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
@pytest.mark.IB
@pytest.mark.C212988
def test_logic_pageRandomOnSelectedPagesDeleteSelectedPage(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "To verify page randomization after "
                                                           "applying logic and deleting selected page.")
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
        # pytest.set_trace()
        mySurvey.myLogic.pageRandom_randomizePages_selected([2, 4, 5])
        ex = mySurvey.myLogic.checkPagesRandomizedIconSelected()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page randomization icon appears",
                                 "checks to make sure that the selected page randomization icon appears.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of page randomization icon"

        mySurvey.myLogic.pageRandom_deletePageFromMoreActionTab(4)
        mySurvey.myLogic.click_PageRandomization()
        ex = mySurvey.myLogic.pageRandom_randomizePages_verifySelected([2, 4], 4)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that page randomization selected pages after deleting selected page",
                                 "checks to make sure that post deleting selected page, "
                                 "selected page randomization list is proper.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify correct page list shown for page randomization option post deleting selected page."

        ex = mySurvey.myLogic.checkPagesRandomizedIconSelected(2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page randomization icon appears",
                                 "checks to make sure that the selected page randomization icon appears.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of page randomization icon"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
