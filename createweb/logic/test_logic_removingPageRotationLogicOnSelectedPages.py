from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest
import time

'''
__author__ = 'rajat'
'''
#Test railId - C212981
@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicRemovingPageRotationLogicOnSelectedPages/",  # report_relative_location
                               "test_logic_removingPageRotationLogicOnSelectedPages",  # report_file_name_prefix
                               "verify removing page rotation logic on selected pages",  # test_suite_title
                               ("This test applies "
                                "  removing page rotation logic  "
                                " on selected pages"),  # test_suite_description
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
def test_logic_removingPageRotationLogicOnAllPages(create_survey):
    driver, mySurvey, report = create_survey


    Question1 = "Hows overall progress for Infobeans?"
    Question2 = "How was examination?"
    Question3 = "How is your health?"
    Question4 = "Are you fine?"
    Question5 = "Who are you?"

    Page1 = [
        Question1
    ]
    Page2 = [
        Question2
    ]
    Page3 = [
        Question3
    ]
    Page4 = [
        Question4
    ]
    Page5 = [
        Question5
    ]


    answer_rows = ["Good", "Very Good", "Normal"]

    report.add_report_record(ReportMessageTypes.TEST_CASE,
                             "verify removing page rotation logic on selected pages")
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

        mySurvey.myBuilder.click_NewPageAddButton()

        # page4
        for Question in Page4:
            mySurvey.myBank.searchForQuestion(mySurvey.survey_id, Question, answer_rows)
            mySurvey.myLogic.pushQuestionToStack(Question)

        mySurvey.myBuilder.click_NewPageAddButton()

        # page5
        for Question in Page5:
            mySurvey.myBank.searchForQuestion(mySurvey.survey_id, Question, answer_rows)
            mySurvey.myLogic.pushQuestionToStack(Question)

        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageRandomization()
        mySurvey.myLogic.pageRandom_rotatePages_selected([1,3,5])
        mySurvey.myLogic.click_PageRandomization()
        mySurvey.myLogic.delete_pageRandomization()

        ex = mySurvey.myLogic.verifyPageRandomizationStatus('OFF')
        print ex
        report.add_report_record(ReportMessageTypes.TEST_STEP, "verify removing page rotation logic on selected pages.",
                                 "checks to verify page rotation.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)

        assert ex, "True"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
