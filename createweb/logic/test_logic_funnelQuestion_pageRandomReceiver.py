from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicFunnelQuestionPageRandomReceiver/",  # report_relative_location
                               "test_logic_funnelQuestion_pageRandomReceiver",  # report_file_name_prefix
                               "Randomize receiver question page with all other pages that are after the page with the sender question",  # test_suite_title
                               ("This test adds a sender and receiver question and funnels accordingly."
                                " Test then attempts attempts to randomize receiver page with other pages."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_logic_funnelQuestion_pageRandomReceiver(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Randomize receiver question page with all other pages that are after the page with the sender question.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best German Kanmusu?", 1,
                                                          ["Graf Zeppelin", "Bismarck", "Prinz Eugen", "U-511"])
        mySurvey.myBuilder.click_NewPageAddButton()
        for x in xrange(3):
            mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(5)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1,
                                                          ["Miku", "Luka", "Rin", "Gumi"])
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myLogic.toggleQuestionFunneling()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageRandomization()
        ex = mySurvey.myLogic.verify_pageRandom_randomizePages_conflictError()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify page randomization conflict error",
                                 "checks to make sure that the conflict error appears in page randomization",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify conflict error on page randomization page."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
