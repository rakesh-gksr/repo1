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
# test railid - C212980
@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicRemovingPageRotationLogicOnAllPages/",  # report_relative_location
                               "test_logic_removingPageRotationLogicOnAllPages",  # report_file_name_prefix
                               "verify removing page rotation logic on all pages",  # test_suite_title
                               ("This test applies "
                                "  removing page rotation logic  "
                                " on all pages"),  # test_suite_description
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


    report.add_report_record(ReportMessageTypes.TEST_CASE,
                             "verify removing page rotation logic on all pages")
    try:
        # add few pages
        pagewise_questions = [
            "How noisy is this neighborhood?",
            "In a typical month, about how much money, in U.S. dollars, do you spend on your cable service?",
            "What number would you use to rate all your health care in the last 12 months?",
            "In what state or U.S. territory are you currently registered to vote?",
            "Do you feel your children is getting proper education facilities?",
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
        mySurvey.myLogic.pageRandom_rotatePages()
        mySurvey.myLogic.click_PageRandomization()
        mySurvey.myLogic.delete_pageRandomization()

        ex = mySurvey.myLogic.verifyPageRandomizationStatus("OFF")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "verify removing page rotation logic on all pages.",
                                 "checks to verify page rotation.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)

        assert ex, "Failed to check page rotation deletion"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
