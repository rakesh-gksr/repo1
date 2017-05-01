from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAdvBranchMultiSelect/",  # report_relative_location
                               "test_advBranch_multiSelect",  # report_file_name_prefix
                               # test_suite_title
                               "Test adding a branching rule that skips to a later page based on the answer to a multi-select question",
                               ("This test adds certain advanced branching types "
                                " and then verifies proper result in preview."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    env_init("platinum_advanced_branching")
    import datetime
    import os
    testcasename = os.path.basename(__file__).split(".")[0] + "--" + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_advBranch_multiSelect_multiChoice(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based on the answer to a multi-select question - For Multiple Choice Questions.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myDesign.click_addPageTitle("Page 1", "This is test page 1")
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1,
                                                          ["Miku", "Luka", "Rin"])
        for x in xrange(4):
            mySurvey.myCreate.newPage_viaSvysvc(mySurvey.survey_id, x + 2, "Page " + str(x + 2))
        driver.refresh()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_matrix_scale_question(mySurvey.survey_id, page_num,
                                                           "Please classify the following Ships", 2,
                                                           ["Haruna", "Yuudachi", "Naka"],
                                                           ["Destroyer(DD)", "Light Cruiser(CL)", "Battleship(BB)",
                                                            "Aircraft Carrier(CV)", "Submarine(SS)"])
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.turn_on_multiple_answers()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myQuestion.turn_on_multiple_answers("Matrix")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("MultipleChoice", [1, 1], "response", [None], "skip", "default", 3)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("multiChoice", 1, [1], "page_skip", "Page 3")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Has Response",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Has Response"
        mySurvey.myDesign.return_from_preview_window()
        mySurvey.myLogic.remove_advanced_branching()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("MultipleChoice", [1, 1], "noresponse", [None], "finish", "default", None)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("multiChoice", 1, None, "end_survey", "That's the end of the preview!")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Has No Response",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Has No Response"
        mySurvey.myDesign.return_from_preview_window()
        mySurvey.myLogic.remove_advanced_branching()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("MultipleChoice", [1, 1], "notcontains", [None], "disqualify", "default", None)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("multiChoice", 1, [3], "end_survey", "That's the end of the preview!")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Does Not Contain",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Does Not Contain"
        mySurvey.myDesign.return_from_preview_window()
        mySurvey.myLogic.remove_advanced_branching()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("MultipleChoice", [1, 1], "containsanyof", ["Luka"], "hideq", "question", 2)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("multiChoice", 1, [1], "page_skip", "Page 3")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Contains One Of",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Contains One Of"
        mySurvey.myDesign.return_from_preview_window()
        mySurvey.myLogic.remove_advanced_branching()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("MultipleChoice", [1, 1], "notcontainsanyof", ["Luka"], "showq", "question", 2)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("multiChoice", 1, [3], "page_skip", "Page 2")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Does Not Contain Any Of",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Does Not Contain Any Of"
        mySurvey.myDesign.return_from_preview_window()
        mySurvey.myLogic.remove_advanced_branching()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("MultipleChoice", [1, 1], "containsallof", ["Luka", "Rin"], "hidep", "default", 5)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("multiChoice", 1, [1, 2, 3], "future_skip_end", [5, "That's the end of the preview!"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Contains All Of",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Contains All Of"
        mySurvey.myDesign.return_from_preview_window()
        mySurvey.myLogic.remove_advanced_branching(1)
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("MultipleChoice", [1, 1], "notcontainsallof", ["Luka"], "showp", "default", 4)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("multiChoice", 1, [3], "future_show", [4, "Page 4"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Does Not Contain All Of",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Does Not Contain All Of"
        mySurvey.myDesign.return_from_preview_window()
        mySurvey.myLogic.remove_advanced_branching()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("MultipleChoice", [1, 1], "equals", [None], "invalidate", "question_error", [2, "INVALIDATED"])])
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
        ex = mySurvey.myLogic.verify_advanced_branching("multiChoice", 1, [1], "invalidation", ["Page 2", "INVALIDATED"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Is Exactly",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Is Exactly"
        mySurvey.myDesign.return_from_preview_window()
        mySurvey.myLogic.remove_advanced_branching()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("MultipleChoice", [1, 1], "notequals", [None], "disqualify", "default", None)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("multiChoice", 1, [2], "end_survey", "That's the end of the preview!")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Is Not Exactly",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Is Not Exactly"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advBranch_multiSelect_matrix(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based on the answer to a multi-select question - For Matrix Type Questions")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myDesign.click_addPageTitle("Page 1", "This is test page 1")
        mySurvey.myQuestion.generate_matrix_scale_question(mySurvey.survey_id, page_num,
                                                           "Please classify the following Ships", 2,
                                                           ["Haruna", "Yuudachi", "Naka"],
                                                           ["Destroyer(DD)", "Light Cruiser(CL)", "Battleship(BB)",
                                                            "Aircraft Carrier(CV)", "Submarine(SS)"])
        for x in xrange(4):
            mySurvey.myCreate.newPage_viaSvysvc(mySurvey.survey_id, x + 2, "Page " + str(x + 2))
        driver.refresh()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1,
                                                          ["Miku", "Luka", "Rin"])
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myQuestion.turn_on_multiple_answers()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.turn_on_multiple_answers("Matrix")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("matrix", [1, 1, 1], "response", [None], "skip", "default", 3)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("matrix", 1, [(1, 1)], "page_skip", "Page 3")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Has Response",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Has Response"
        mySurvey.myDesign.return_from_preview_window()
        mySurvey.myLogic.remove_advanced_branching()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("matrix", [1, 1, 1], "noresponse", [None], "finish", "default", None)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("matrix", 1, None, "end_survey", "That's the end of the preview!")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Has No Response",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Has No Response"
        mySurvey.myDesign.return_from_preview_window()
        mySurvey.myLogic.remove_advanced_branching()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("matrix", [1, 1, 1], "notcontains", [None], "disqualify", "default", None)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("matrix", 1, [(1, 3)], "end_survey", "That's the end of the preview!")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Does Not Contain",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Does Not Contain"
        mySurvey.myDesign.return_from_preview_window()
        mySurvey.myLogic.remove_advanced_branching()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("matrix", [1, 1, 1], "containsanyof", ["Light Cruiser(CL)"], "hideq", "question", 2)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("matrix", 1, [(1, 1)], "page_skip", "Page 3")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Contains One Of",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Contains One Of"
        mySurvey.myDesign.return_from_preview_window()
        mySurvey.myLogic.remove_advanced_branching()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("matrix", [1, 1, 1], "notcontainsanyof", ["Light Cruiser(CL)"], "showq", "question", 2)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("matrix", 1, [(1, 3)], "page_skip", "Page 2")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Does Not Contain Any Of",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Does Not Contain Any Of"
        mySurvey.myDesign.return_from_preview_window()
        mySurvey.myLogic.remove_advanced_branching()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("matrix", [1, 1, 1], "containsallof", ["Light Cruiser(CL)", "Battleship(BB)"], "hidep", "default", 5)])
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
            "matrix", 1, [
                (1, 1), (1, 2), (1, 3)], "future_skip_end", [
                5, "That's the end of the preview!"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Contains All Of",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Contains All Of"
        mySurvey.myDesign.return_from_preview_window()
        mySurvey.myLogic.remove_advanced_branching(1)
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("matrix", [1, 1, 1], "notcontainsallof", ["Light Cruiser(CL)", "Battleship(BB)"], "showp", "default", 4)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("matrix", 1, [(1, 4)], "future_show", [4, "Page 4"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Does Not Contain All Of",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Does Not Contain All Of"
        mySurvey.myDesign.return_from_preview_window()
        mySurvey.myLogic.remove_advanced_branching()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("matrix", [1, 1, 1], "equals", [None], "invalidate", "question_error", [2, "INVALIDATED"])])
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
        ex = mySurvey.myLogic.verify_advanced_branching("matrix", 1, [(1, 1)], "invalidation", ["Page 2", "INVALIDATED"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Is Exactly",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Is Exactly"
        mySurvey.myDesign.return_from_preview_window()
        mySurvey.myLogic.remove_advanced_branching()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("matrix", [1, 1, 1], "notequals", [None], "disqualify", "default", None)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("matrix", 1, [(1, 2)], "end_survey", "That's the end of the preview!")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Is Not Exactly",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Is Not Exactly"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
