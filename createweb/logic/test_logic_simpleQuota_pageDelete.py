from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest



@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicSimpleQuotaPageDelete/",  # report_relative_location
                               "test_logic_simpleQuota_pageDelete",  # report_file_name_prefix
                               "Test delete a page with quota",  # test_suite_title
                               ("This Test performs two tests for CREATE-4484. Firstly deleting a page with a quota and checking for the warning."
                                " Secondly, checking warning on pages that are the destinations of page skip logic"
                                " or question skip logic."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_logic_simpleQuota_pageDelete(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test delete a page with simple quota.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myCreate.scroll_to_page_num(1)
        ex = mySurvey.myBuilder.click_MultipleChoiceAddButton()
        # time.sleep(3)
        ex = mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Kongou")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Hiei")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Kirishima")
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        # time.sleep(1)
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_Quota()
        mySurvey.myLogic.quotaSetupWizard("simple", 1, 1, [1, 2, 3])
        mySurvey.myLogic.click_QuotaDone()
        ex = mySurvey.myLogic.checkQuotaIcon(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify icon removed from sender question",
                                 "checks to make sure that the icon next to the sender question is no longer present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify removal of icon."
        mySurvey.myCreate.nuke_page(1)
        ex = mySurvey.myLogic.verifyPageDeleteWarningQuota()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify page deletion warning appears",
                                 "checks to make sure that a warning appears when trying to delete the page with quota.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify page deletion warning."
        # time.sleep(3)
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_logic_test_logic_simpleQuota_pageOrQuestionLogic_pageDelete(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test delete a page which is destination of page skip logic or question skip logic.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myCreate.scroll_to_page_num(1)
        ex = mySurvey.myBuilder.click_MultipleChoiceAddButton()
        # time.sleep(3)
        ex = mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Kongou")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Hiei")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Kirishima")
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
            # time.sleep(1)
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        mySurvey.myLogic.select_PageSkipTypeDropdown("P2")
        mySurvey.myLogic.click_PageSkipLogicTargetApplyButton()
        mySurvey.myCreate.scroll_to_page_num(2)
        # time.sleep(3)
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myDesign.scroll_to_top()
        mySurvey.myQuestion.click_on_question_to_edit()
        mySurvey.myQuestion.click_question_logic_tab()
        mySurvey.myLogic.setQuestionSkipLogic(1, 3)
        mySurvey.myCreate.nuke_page_warning(3)
        ex = mySurvey.myLogic.verifyPageDeleteWarningLogic()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify page deletion warning appears",
                                 "checks to make sure that a warning appears when trying to delete the page with quota.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify page deletion warning."
        mySurvey.myCreate.nuke_page_warning(2)
        ex = mySurvey.myLogic.verifyPageDeleteWarningLogic()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify page deletion warning appears",
                                 "checks to make sure that a warning appears when trying to delete the page with quota.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify page deletion warning."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
