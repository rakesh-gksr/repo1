from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAdvBranchMoveUpDownLogic/",  # report_relative_location
                               "test_advBranch_moveUpDownLogic",  # report_file_name_prefix
                               "Test moving up/down advanced branching logic",  # test_suite_title
                               ("Tests CREATE-5840."),  # test_suite_description
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


def test_advBranch_moveUpLogic(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test dragging logic row up in advanded branching.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myDesign.click_addPageTitle("Page 1", "This is test page 1")
        mySurvey.myQuestion.generate_ranking_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1, 4, False)
        mySurvey.myCreate.newPage_viaSvysvc(mySurvey.survey_id, 2, "Page 2")
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("matrix", [1, 1, 1], "equals", [2], "finish", "default", None, "and"),
            ("matrix", [1, 1, 2], "notequals", [3], "finish", "default", None)])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Advanced Logic",
                                 "Verifies advanced logic window closed and logic saved.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to save advanced logic"
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.open_existing_page_logic()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("matrix", [1, 1, 3], "notequals", [4], "finish", "default", None)])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Advanced Logic",
                                 "Verifies advanced logic window closed and logic saved.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to save advanced logic"
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.open_existing_page_logic()
        mySurvey.myLogic.move_advBranch_rule(2, "up")
        ex = mySurvey.myLogic.verify_advBranch_logicRow(1, "Q1.R3 != C4 => END SURVEY")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 2 moved to row 1",
                                 "Verifies that advanced logic row moved up successfully.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify moving logic row up"
        ex = mySurvey.myLogic.verify_advBranch_logicRow(2, "Q1.R1 = C2 AND Q1.R2 != C3 => END SURVEY")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 1 moved to row 2",
                                 "Verifies that advanced logic row moved down successfully.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify moving logic row down"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_advBranch_moveDownLogic(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test dragging logic row Down in advanded branching.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myDesign.click_addPageTitle("Page 1", "This is test page 1")
        mySurvey.myQuestion.generate_ranking_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1, 4, False)
        mySurvey.myCreate.newPage_viaSvysvc(mySurvey.survey_id, 2, "Page 2")
        driver.refresh()
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("matrix", [1, 1, 1], "equals", [2], "finish", "default", None, "and"),
            ("matrix", [1, 1, 2], "notequals", [3], "finish", "default", None)])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Advanced Logic",
                                 "Verifies advanced logic window closed and logic saved.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to save advanced logic"
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.open_existing_page_logic()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("matrix", [1, 1, 3], "notequals", [4], "finish", "default", None)])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Advanced Logic",
                                 "Verifies advanced logic window closed and logic saved.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to save advanced logic"
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.open_existing_page_logic()
        mySurvey.myLogic.move_advBranch_rule(1, "down")
        ex = mySurvey.myLogic.verify_advBranch_logicRow(1, "Q1.R3 != C4 => END SURVEY")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 2 moved to row 1",
                                 "Verifies that advanced logic row moved up successfully.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify moving logic row up"
        ex = mySurvey.myLogic.verify_advBranch_logicRow(2, "Q1.R1 = C2 AND Q1.R2 != C3 => END SURVEY")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 1 moved to row 2",
                                 "Verifies that advanced logic row moved down successfully.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify moving logic row down"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
