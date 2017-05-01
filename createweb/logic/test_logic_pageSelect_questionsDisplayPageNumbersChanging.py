from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest

'''
__author__ = 'rajat'
'''
# TESTRAIL ID - C83921


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicQuestionDisplayPageNumbersChanging/",  # report_relative_location
                               "test_logic_questionDisplayPageNumbersChanging",  # report_file_name_prefix
                               "verify questions display while changing page numbers on question randomization option",  # test_suite_title
                               ("This test verify questions display "
                                " while changing page numbers "
                                " on question randomization option."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.C83921
@pytest.mark.IB
def test_logic_questionDisplayPageRandomNumbersChanging(create_survey):
    driver, mySurvey, report = create_survey




    Question1 = "Hows overall progress for Infobeans?"
    Question2 = "How was examination?"
    Question3 = "How is your health?"

    Page1 = [
        Question1
    ]
    Page2 = [
        Question2
    ]
    Page3 = [
        Question3
    ]

    answer_rows = ["Good", "Very Good", "Normal"]
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify questions display while changing page numbers on question randomization option")
    try:
        # page1
        for Question in Page1:
          mySurvey.myBank.searchForQuestion(mySurvey.survey_id, Question, answer_rows)
          mySurvey.myLogic.pushQuestionToStack(Question)

        mySurvey.myBuilder.click_NewPageAddButton()

        # page2

        for Question in Page2:
          mySurvey.myBank.searchForQuestion(
            mySurvey.survey_id,
            Question, answer_rows)
          mySurvey.myLogic.pushQuestionToStack(Question)

        mySurvey.myBuilder.click_NewPageAddButton()
        # page3
        for Question in Page3:
          mySurvey.myBank.searchForQuestion(mySurvey.survey_id, Question, answer_rows)
          mySurvey.myLogic.pushQuestionToStack(Question)
        # Verifying Page text for page2
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_QuestionRandomization()
        ex = mySurvey.myLogic.verify_available_questions(2, Page2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "verify page number and its all questions display",
                                 "verifies that the page number 2 and its all questions is displayed.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that all the page number 2 and its all questions is displayed"

        # Verifying Page text for page3
        ex = mySurvey.myLogic.verify_available_questions(3, Page3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "verify page number and its all questions display",
                                 "verifies that the page number 3 and its all questions is displayed.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that all the page number 3 and its all questions is displayed"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
