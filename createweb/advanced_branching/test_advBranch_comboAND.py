from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAdvBranchComboAND/",  # report_relative_location
                               "test_advBranch_comboAnd",  # report_file_name_prefix
                               "Test branching based on combination of different questions (AND)",  # test_suite_title
                               ("This test adds certain advanced branching types "
                                " and then verifies proper result in preview."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    env_init('platinum_advanced_branching')
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_advBranch_comboAND(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test branching based on combination of different questions (AND).")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myDesign.click_addPageTitle("Page 1", "This is test page 1")
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1,
                                                          ["Miku", "Luka", "Rin"])
        driver.refresh()
        mySurvey.myQuestion.generate_menu_matrix_question(
            mySurvey.survey_id, page_num,
            "Best Vocaloid?", 2)
        mySurvey.myQuestion. generate_ranking_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 3)
        mySurvey.myQuestion.generate_multi_textbox_question(
            mySurvey.survey_id, page_num,
            "Best Vocaloid?", 4)
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.turn_on_multiple_answers()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        for x in xrange(4):
            mySurvey.myCreate.newPage_viaSvysvc(mySurvey.survey_id, x + 2, "Page " + str(x + 2))
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("MultipleChoice", [1, 1], "notcontains", [None], "skip", "default", 3, "and"),
            ("matrix", [1, 3, 1], "equals", [None], "skip", "default", 3, "and"),
            ("menuMatrix", [1, 2, 1, 1], "response", [None], "skip", "default", 3, "and"),
            ("multibox", [1, 4, 1], "notcontains", ["like"], ["skip", "hidep"], ["default", "default"], [3, 4])])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Advanced Logic",
                                 "Verifies advanced logic window closed and logic saved.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to save advanced logic"
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks preview button, in order to verify theme in preview window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        mySurvey.myDesign.click_off_preview_warning()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.switch_to_preview_iframe()
        ex = mySurvey.myLogic.verify_advanced_branching(
            [
                "multiChoice", "menuMatrix", "ranking", "text"], [
                1, 2, 3, 4], [
                2, (1, 1, 1), (1, 1), "Miku"], [
                    "page_skip", "future_skip"], [
                        "Page 3", 4])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - All Conditions True",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - All Conditions True"
        mySurvey.myDesign.return_from_preview_window()
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks preview button, in order to verify theme in preview window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        mySurvey.myDesign.click_off_preview_warning()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.switch_to_preview_iframe()
        ex = mySurvey.myLogic.verify_advanced_branching(
            [
                "multiChoice", "menuMatrix", "ranking", "text"], [
                1, 2, 3, 4], [
                1, None, (1, 2), "like"], [
                    "page_skip", "future_skip"], [
                        "Page 3", 4])
        ex = not ex
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - All Conditions False",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - All Conditions False"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
