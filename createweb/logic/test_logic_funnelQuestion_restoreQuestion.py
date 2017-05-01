from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicFunnelQuestion_restoreQuestion/",  # report_relative_location
                               "test_logic_funnelQuestion_restoreQuestion",  # report_file_name_prefix
                               "Test restoring sender/receiver question",  # test_suite_title
                               ("This test adds a sender and receiver question and funnels accordingly."
                                " Test then attempts attempts to restore questions independently after deleting sender/receiver question/all."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_logic_funnelQuestion_restoreQuestion_sender(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test restoring sender question.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best German Kanmusu?", 1,
                                                          ["Graf Zeppelin", "Bismarck", "Prinz Eugen", "U-511"])
        mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1,
                                                          ["Miku", "Luka", "Rin", "Gumi"])
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myLogic.toggleQuestionFunneling()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 2,
                                                          ["Miku", "Luka", "Rin", "Gumi"])
        mySurvey.myQuestion.click_on_question_to_edit(3)
        mySurvey.myLogic.toggleQuestionFunneling()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 3,
                                                          ["Miku", "Luka", "Rin", "Gumi"])
        mySurvey.myQuestion.click_on_question_to_edit(4)
        mySurvey.myLogic.toggleQuestionFunneling()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myQuestion.hover_on_question_to_delete_it()
        mySurvey.myLogic.confirmMultiQuestionDelete()
        mySurvey.myCreate.restoreDeletedQuestion(1)
        ex = True if mySurvey.myCreate.num_questions_in_survey() == 1 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify independent question restore",
                                 "Verifies that questions restore independently, question 1.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify funneling question restore for question 1"
        mySurvey.myCreate.restoreDeletedQuestion(1)
        ex = True if mySurvey.myCreate.num_questions_in_survey() == 2 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify independent question restore",
                                 "Verifies that questions restore independently, question 2.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify funneling question restore for question 2"
        mySurvey.myCreate.restoreDeletedQuestion(1)
        ex = True if mySurvey.myCreate.num_questions_in_survey() == 3 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify independent question restore",
                                 "Verifies that questions restore independently, question 3.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify funneling question restore for question 3"
        mySurvey.myCreate.restoreDeletedQuestion(1)
        ex = True if mySurvey.myCreate.num_questions_in_survey() == 4 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify independent question restore",
                                 "Verifies that questions restore independently, question 4.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify funneling question restore for question 4"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_logic_funnelQuestion_restoreQuestion_receiver(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test restoring sender question.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best German Kanmusu?", 1,
                                                          ["Graf Zeppelin", "Bismarck", "Prinz Eugen", "U-511"])
        mySurvey.myBuilder.click_NewPageAddButton()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1,
                                                          ["Miku", "Luka", "Rin", "Gumi"])
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myLogic.toggleQuestionFunneling()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myQuestion.hover_on_question_to_delete_it(2)
        ex = True if mySurvey.myCreate.num_questions_in_survey() == 1 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify sender didn't delete",
                                 "Verifies that sender question not deleted with receiver.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify sender not deleted"
        mySurvey.myCreate.restoreDeletedQuestion(1)
        ex = True if mySurvey.myCreate.num_questions_in_survey() == 2 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify independent question restore",
                                 "Verifies that questions restore independently, question 2.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify funneling question restore for question 2"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()