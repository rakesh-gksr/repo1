from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest

__author__ = 'rakesh'


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestadvBranchVerifyAdvanceBranchingAfterResavingQuestion/",  # report_relative_location
                               "test_advBranch_verifyAdvanceBranchingAfterResavingQuestion",  # report_file_name_prefix
                               "Resaving any question removes branching rule applied on any question",
                               # test_suite_title
                               ("This test adds a multiple choice question on page 1 and apply the advanced branching"
                                " type and then open Q1 question in edit mode "
                                " and then verifies that branching rule still apply if user re saves the question."),
                               # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    env_init("platinum_advanced_branching")
    import datetime
    import os
    testcasename = os.path.basename(__file__).split(".")[0] + "--" + datetime.datetime.now().strftime("%I:%M%p %b %d,"
                                                                                                      " %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.advBranch
@pytest.mark.IB
@pytest.mark.C195135
def test_advBranch_verifyAdvanceBranchingAfterResavingQuestion(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Resaving any question removes branching rule applied on " +
                                                           "any question Jira Id: CREATE-6111")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myDesign.click_addPageTitle("Page 1", "This is test page 1")
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1,
                                                          ["Miku", "Luka", "Rin", "Gumi"])
        # code to added new page into survey
        mySurvey.myCreate.newPage_viaSvysvc(mySurvey.survey_id, 2, "Page 2" )
        driver.refresh()
        # code to add advance logic on page no 1
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
        # edit question no 1 on page 1
        mySurvey.myQuestion.click_on_question_to_edit(1)
        # re save question question after editing question
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the save button after editing Q1",
                                 "Verifies that Q1 question saved successfully.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click save button"
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
        ex = mySurvey.myLogic.verify_advanced_branching("multiChoice", 1, [1], "end_survey",
                                                        "That's the end of the preview!")

        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify branching rule still apply if user resaves "
                                                               "the question",
                                 "verifies that branching rule still apply if user resaves the question.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching after editing the Q1 question"
        mySurvey.myDesign.return_from_preview_window()

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
