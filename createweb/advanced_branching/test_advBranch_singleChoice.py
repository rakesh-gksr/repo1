from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest

survey_id_dict= {
    'multi_choice': '130248739',
    'dropdown': '130249837',
    'multi_textbox': '130249853',
    'NPS': '130249962',
    'ranking': '130250001'
}


def pre_setup_survey(mySurvey, driver, report, survey_type):
    survey_title = mySurvey.myCreate.get_survey_title()
    new_survey_id = mySurvey.myCreate.copy_exiting_survey_via_svysvc(survey_id_dict[survey_type], "58237384", survey_title + " Copied via svysvc")
    url = mySurvey.myCreate.open_copied_survey(new_survey_id["survey_id"])
    driver.get(url)
    report.add_report_record(ReportMessageTypes.TEST_STEP, "Survey Loaded or recreated",
                             "The survey has either been copied or recreated and is ready for the test",
                             True,
                             True,
                             False,
                             driver)


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAdvBranchSingleChoice/",  # report_relative_location
                               "test_advBranch_singleChoice",  # report_file_name_prefix
                               # test_suite_title
                               "Test adding a branching rule that skips to a later page based on the answer to a single choice question selecting each predicates",
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


def test_advBranch_singleChoice_multiChoice_response(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based on the answer to a single choice question selecting each predicates - For Multiple Choice Questions - Response.")
    try:
        pre_setup_survey(mySurvey, driver, report, "multi_choice")
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
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advBranch_singleChoice_multiChoice_noResponse(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based on the answer to a single choice question selecting each predicates - For Multiple Choice Questions - No Response.")
    try:
        pre_setup_survey(mySurvey, driver, report, "multi_choice")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("MultipleChoice", [1, 1], "noresponse", [None], "skip", "default", 4)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("multiChoice", 1, None, "page_skip", "Page 4")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Has No Response",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Has No Response"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advBranch_singleChoice_multiChoice_equals(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based on the"
        " answer to a single choice question selecting each predicates - For Multiple Choice Questions - Equals.")
    try:
        pre_setup_survey(mySurvey, driver, report, "multi_choice")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("MultipleChoice", [1, 1], "equals", [None], "finish", "default", None)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("multiChoice", 1, [1], "end_survey", "That's the end of the preview!")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Is Exactly",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Is Exactly"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advBranch_singleChoice_multiChoice_notEquals(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based on the"
        " answer to a single choice question selecting each predicates - For Multiple Choice Questions - Not Equals.")
    try:
        pre_setup_survey(mySurvey, driver, report, "multi_choice")
        mySurvey.myLogic.unfold_LogicRegion()
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


def test_advBranch_singleChoice_multiChoice_isOneOf(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based on the"
        " answer to a single choice question selecting each predicates - For Multiple Choice Questions - Is One Of.")
    try:
        pre_setup_survey(mySurvey, driver, report, "multi_choice")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("MultipleChoice", [1, 1], "isoneof", ["Luka", "Rin"], "skip", "default", 2)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("multiChoice", 1, [1], "page_skip", "Page 2")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Contains One Of",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Contains One Of"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advBranch_singleChoice_multiChoice_notOneOf(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based on the"
        " answer to a single choice question selecting each predicates - For Multiple Choice Questions - Not One Of.")
    try:
        pre_setup_survey(mySurvey, driver, report, "multi_choice")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("MultipleChoice", [1, 1], "notisoneof", ["Luka", "Rin"], "disqualify", "default", None)])
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
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Does Not Contain All Of",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Does Not Contain All Of"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advBranch_singleChoice_dropdown_response(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based "
        "on the answer to a single choice question selecting each predicates - For Dropdown Questions - Response.")
    try:
        pre_setup_survey(mySurvey, driver, report, "dropdown")
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
        ex = mySurvey.myLogic.verify_advanced_branching("dropdown", 1, ["Miku"], "page_skip", "Page 3")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Has Response",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Has Response"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advBranch_singleChoice_dropdown_noResponse(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based "
        "on the answer to a single choice question selecting each predicates - For Dropdown Questions - No Response.")
    try:
        pre_setup_survey(mySurvey, driver, report, "dropdown")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("MultipleChoice", [1, 1], "noresponse", [None], "skip", "default", 4)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("dropdown", 1, None, "page_skip", "Page 4")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Has No Response",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Has No Response"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advBranch_singleChoice_dropdown_equals(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based "
        "on the answer to a single choice question selecting each predicates - For Dropdown Questions - Equals.")
    try:
        pre_setup_survey(mySurvey, driver, report, "dropdown")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("MultipleChoice", [1, 1], "equals", [None], "finish", "default", None)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("dropdown", 1, ["Miku"], "end_survey", "That's the end of the preview!")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Is Exactly",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Is Exactly"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advBranch_singleChoice_dropdown_notEquals(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based "
        "on the answer to a single choice question selecting each predicates - For Dropdown Questions - Not Equals.")
    try:
        pre_setup_survey(mySurvey, driver, report, "dropdown")
        mySurvey.myLogic.unfold_LogicRegion()
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
        ex = mySurvey.myLogic.verify_advanced_branching("dropdown", 1, ["Luka"], "end_survey", "That's the end of the preview!")
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


def test_advBranch_singleChoice_dropdown_oneOf(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based "
        "on the answer to a single choice question selecting each predicates - For Dropdown Questions - Is One Of.")
    try:
        pre_setup_survey(mySurvey, driver, report, "dropdown")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("MultipleChoice", [1, 1], "isoneof", ["Luka", "Rin"], "skip", "default", 2)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("dropdown", 1, ["Miku"], "page_skip", "Page 2")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Contains One Of",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Contains One Of"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advBranch_singleChoice_dropdown_notOneOf(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based "
        "on the answer to a single choice question selecting each predicates - For Dropdown Questions - Is Not One Of.")
    try:
        pre_setup_survey(mySurvey, driver, report, "dropdown")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("MultipleChoice", [1, 1], "notisoneof", ["Luka", "Rin"], "disqualify", "default", None)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("dropdown", 1, None, "end_survey", "That's the end of the preview!")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Does Not Contain All Of",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Does Not Contain All Of"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advBranch_singleChoice_multiBoxes_response(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based on the "
        "answer to a single choice question selecting each predicates - For Multi Textbox Questions - Response.")
    try:
        pre_setup_survey(mySurvey, driver, report, "multi_textbox")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("multibox", [1, 1, 1], "response", [None], "skip", "default", 3)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("text", 1, ["Miku"], "page_skip", "Page 3")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Has Response",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Has Response"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advBranch_singleChoice_multiBoxes_noResponse(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based on the "
        "answer to a single choice question selecting each predicates - For Multi Textbox Questions - No Response.")
    try:
        pre_setup_survey(mySurvey, driver, report, "multi_textbox")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("multibox", [1, 1, 1], "noresponse", [None], "skip", "default", 4)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("text", 1, None, "page_skip", "Page 4")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Has No Response",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Has No Response"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advBranch_singleChoice_multiBoxes_equals(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based on the "
        "answer to a single choice question selecting each predicates - For Multi Textbox Questions - Equals.")
    try:
        pre_setup_survey(mySurvey, driver, report, "multi_textbox")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("multibox", [1, 1, 1], "equals", ["Miku"], "finish", "default", None)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("text", 1, ["Miku"], "end_survey", "That's the end of the preview!")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Is Exactly",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Is Exactly"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advBranch_singleChoice_multiBoxes_notEquals(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based on the "
        "answer to a single choice question selecting each predicates - For Multi Textbox Questions - Not Equals.")
    try:
        pre_setup_survey(mySurvey, driver, report, "multi_textbox")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("multibox", [1, 1, 1], "notequals", ["Miku"], "disqualify", "default", None)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("text", 1, ["Luka"], "end_survey", "That's the end of the preview!")
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


def test_advBranch_singleChoice_multiBoxes_contains(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based on the "
        "answer to a single choice question selecting each predicates - For Multi Textbox Questions - Contains.")
    try:
        pre_setup_survey(mySurvey, driver, report, "multi_textbox")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("multibox", [1, 1, 1], "contains", ["Miku"], "skip", "default", 2)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("text", 1, ["Hatsune Miku"], "page_skip", "Page 2")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Contains One Of",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Contains One Of"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advBranch_singleChoice_multiBoxes_notContains(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based on the "
        "answer to a single choice question selecting each predicates - For Multi Textbox Questions - Not Contains.")
    try:
        pre_setup_survey(mySurvey, driver, report, "multi_textbox")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("multibox", [1, 1, 1], "notcontains", ["Miku"], "disqualify", "default", None)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("text", 1, ["Luka"], "end_survey", "That's the end of the preview!")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Does Not Contain All Of",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Does Not Contain All Of"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advBranch_singleChoice_NPS_response(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based on the "
        "answer to a single choice question selecting each predicates - For NPS Questions - Response.")
    try:
        pre_setup_survey(mySurvey, driver, report, "NPS")
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
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advBranch_singleChoice_NPS_noResponse(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based on the "
        "answer to a single choice question selecting each predicates - For NPS Questions - No Response.")
    try:
        pre_setup_survey(mySurvey, driver, report, "NPS")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("matrix", [1, 1, 1], "noresponse", [None], "skip", "default", 4)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("matrix", 1, None, "page_skip", "Page 4")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Has No Response",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Has No Response"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advBranch_singleChoice_NPS_equals(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based on the "
        "answer to a single choice question selecting each predicates - For NPS Questions - Equals.")
    try:
        pre_setup_survey(mySurvey, driver, report, "NPS")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("matrix", [1, 1, 1], "equals", [1], "finish", "default", None)])
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
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Is Exactly",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Is Exactly"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advBranch_singleChoice_NPS_notEquals(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based on the "
        "answer to a single choice question selecting each predicates - For NPS Questions - Not Equals.")
    try:
        pre_setup_survey(mySurvey, driver, report, "NPS")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("matrix", [1, 1, 1], "notequals", [1], "disqualify", "default", None)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("matrix", 1, [(1, 1)], "end_survey", "That's the end of the preview!")
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


def test_advBranch_singleChoice_NPS_oneOf(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based on the "
        "answer to a single choice question selecting each predicates - For NPS Questions - Is One Of.")
    try:
        pre_setup_survey(mySurvey, driver, report, "NPS")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("matrix", [1, 1, 1], "isoneof", [1, 2, 3], "skip", "default", 2)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("matrix", 1, [(1, 1)], "page_skip", "Page 2")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Contains One Of",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Contains One Of"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advBranch_singleChoice_NPS_notOneOf(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based on the "
        "answer to a single choice question selecting each predicates - For NPS Questions - Is Not One Of.")
    try:
        pre_setup_survey(mySurvey, driver, report, "NPS")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("matrix", [1, 1, 1], "notisoneof", [1, 2, 3], "disqualify", "default", None)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("matrix", 1, [(1, 5)], "end_survey", "That's the end of the preview!")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Does Not Contain All Of",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Does Not Contain All Of"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advBranch_singleChoice_ranking_response(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based on the "
        "answer to a single choice question selecting each predicates - For Ranking Questions - Response.")
    try:
        pre_setup_survey(mySurvey, driver, report, "ranking")
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
        ex = mySurvey.myLogic.verify_advanced_branching("ranking", 1, [(1, 1)], "page_skip", "Page 3")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Has Response",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Has Response"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advBranch_singleChoice_ranking_noResponse(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based on the "
        "answer to a single choice question selecting each predicates - For Ranking Questions - No Response.")
    try:
        pre_setup_survey(mySurvey, driver, report, "ranking")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("matrix", [1, 1, 1], "noresponse", [None], "skip", "default", 4)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("ranking", 1, None, "page_skip", "Page 4")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Has No Response",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Has No Response"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advBranch_singleChoice_ranking_equals(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based on the "
        "answer to a single choice question selecting each predicates - For Ranking Questions - Equals.")
    try:
        pre_setup_survey(mySurvey, driver, report, "ranking")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("matrix", [1, 1, 1], "equals", [1], "finish", "default", None)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("ranking", 1, [(1, 1)], "end_survey", "That's the end of the preview!")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Is Exactly",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Is Exactly"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advBranch_singleChoice_ranking_notEquals(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based on the "
        "answer to a single choice question selecting each predicates - For Ranking Questions - Not Equals.")
    try:
        pre_setup_survey(mySurvey, driver, report, "ranking")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("matrix", [1, 1, 1], "notequals", [1], "disqualify", "default", None)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("ranking", 1, [(1, 2)], "end_survey", "That's the end of the preview!")
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


def test_advBranch_singleChoice_ranking_oneOf(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based on the "
        "answer to a single choice question selecting each predicates - For Ranking Questions - Is One Of.")
    try:
        pre_setup_survey(mySurvey, driver, report, "ranking")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("matrix", [1, 1, 1], "isoneof", [2, 3], "skip", "default", 2)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("ranking", 1, [(1, 1)], "page_skip", "Page 2")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Contains One Of",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Contains One Of"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advBranch_singleChoice_ranking_notOneOf(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test adding a branching rule that skips to a later page based on the "
        "answer to a single choice question selecting each predicates - For Ranking Questions - Is Not One Of.")
    try:
        pre_setup_survey(mySurvey, driver, report, "ranking")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("matrix", [1, 1, 1], "notisoneof", [2, 3], "disqualify", "default", None)])
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
        ex = mySurvey.myLogic.verify_advanced_branching("ranking", 1, [(1, 4)], "end_survey", "That's the end of the preview!")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - Does Not Contain All Of",
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - Does Not Contain All Of"
        mySurvey.myDesign.return_from_preview_window()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
