from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicFunnelQuestionReceiverMove/",  # report_relative_location
                               "test_logic_funnelQuestion_receiverMove",  # report_file_name_prefix
                               "Test moving a question that is funneling answer choices from a previous question on same page or page after",  # test_suite_title
                               ("This test adds 2 questions "
                                " and then funnels questions into the rows of the second matrix"
                                " question and then moves the receiver. Test verifies funneling logic copied"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_logic_funnelQuestion_receiverMove(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test moving a question that is funneling answer choices from a previous question on same page or page after.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1,
                                                          ["Miku", "Luka", "Rin", "Gumi"])
        mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best German Kanmusu?", 1,
                                                          ["Graf Zeppelin", "Bismarck", "Prinz Eugen", "U-511"])
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 2,
                                                          ["Miku", "Luka", "Rin", "Gumi"])
        mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myLogic.toggleQuestionFunneling()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myLogic.verifyNumFunneledRows(4)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Funneled Rows",
                                 "checks to make sure that there are the same number of funneled rows present"
                                 " as rows in the previous question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify funneled rows."
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myQuestion.click_question_move_tab()
        mySurvey.myLogic.moveQuestion(3, 3)
        ex = mySurvey.myLogic.verifyNumFunneledRows(4, 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Funneled Rows",
                                 "checks to make sure that there are the same number of funneled rows present"
                                 " as rows in the previous question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify funneled rows."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_logic_funnelQuestion_dragReceiver(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test Dragging receiver question before the sender question.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1,
                                                          ["Miku", "Luka", "Rin", "Gumi"])
        mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best German Kanmusu?", 1,
                                                          ["Graf Zeppelin", "Bismarck", "Prinz Eugen", "U-511"])
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myLogic.toggleQuestionFunneling()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myLogic.verifyNumFunneledRows(4)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Funneled Rows",
                                 "checks to make sure that there are the same number of funneled rows present"
                                 " as rows in the previous question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify funneled rows."
        mySurvey.myCreate.move_question_via_drag_and_drop(2, 1)
        mySurvey.myDesign.scroll_to_top()
        # call this to release the dragged question
        mySurvey.myLogic.clickOnPageNumberBody()
        ex = mySurvey.myLogic.verifyNumFunneledRows(4, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Funneled Rows",
                                 "checks to make sure that there are the same number of funneled rows present"
                                 " as rows in the previous question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify funneled rows."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
