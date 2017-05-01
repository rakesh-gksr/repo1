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
                               "TestLogicQuestionRandomSelected/",  # report_relative_location
                               "test_logic_questionRandomSelected",  # report_file_name_prefix
                               "verify question skip logic destination question can't be randomized",  # test_suite_title
                               ("This test verifies question skip logic "
                                "destination question can't be randomized"),  # test_suite_description
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

@pytest.mark.questionRandomization
@pytest.mark.C83922
@pytest.mark.IB
def test_logic_questionRandomSelected(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify question skip logic destination question"
                                                           " can't be randomized")
    try:
        answer_rows = ["silent", "noisy"]
        # Question 1
        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "How noisy is this neighborhood?", answer_rows)
        mySurvey.myLogic.pushQuestionToStack("How noisy is this neighborhood?")

        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_NewPageAddButton()
        # Question 2
        mySurvey.myBank.searchForQuestion(mySurvey.survey_id,
                                          "In a typical month, about how much money, in U.S. dollars, do you spend on your cable service?", answer_rows)
        mySurvey.myLogic.pushQuestionToStack(
            "In a typical month, about how much money, in U.S. dollars, do you spend on your cable service?")
        # Question 3
        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "In what county (or counties) does your target customer live?", answer_rows)
        mySurvey.myLogic.pushQuestionToStack("In what county (or counties) does your target customer live?")

        driver.refresh()
        # change question 1 type to dropdown
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.changeQType("Dropdown")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        # apply skip logic by clicking on Logic tab through hovering on question 1
        mySurvey.myQuestion.hover_on_question(1)
        mySurvey.myLogic.click_on_logic_tab_on_hovering_question()
        mySurvey.myLogic.setQuestionSkipLogic(1, 2, False, 2, True)
        mySurvey.myLogic.setQuestionSkipLogic(2, 2, False, 3)

        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_QuestionRandomization()
        result, ex = mySurvey.myLogic.questionRandom_verifyDestinationQuestionDisabled([2, 3], 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "verify question skip logic destination question " + result + " can't be randomized",
                                 "verifies that question skip logic destination question can't be select",
                                 ex,
                                 True,
                                 not ex,
                                 driver)

        assert ex, "Failed to verify question state to Dropdown"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
