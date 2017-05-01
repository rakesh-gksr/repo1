from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicFunnelQuestionReceiverSkip/",  # report_relative_location
                               "test_logic_funnelQuestion_receiverSkip",  # report_file_name_prefix
                               "Tests that all funnneled answers can have logic applied",  # test_suite_title
                               ("This test verifies CREATE-5071."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_logic_funnelQuestion_receiverSkip(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Tests that all funnneled answers can have logic applied.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myDesign.click_addPageTitle("Page 1", "This is test page 1")
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1,
                                                          ["Miku", "Luka", "Rin"])
        mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myDesign.click_addPageTitle("Page 2", "This is test page 2")
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1, ["Gumi"])
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myLogic.toggleQuestionFunneling()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myQuestion.click_question_logic_tab()
        ex = mySurvey.myLogic.verify_logic_rows(4)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify number of logic Rows",
                                 "checks to make sure that funneled rows can have skip logic applied",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify logic rows for funneled answers."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
