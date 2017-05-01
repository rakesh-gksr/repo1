from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAdvBranchExitblock/",  # report_relative_location
                               "test_advBranch_exitblock",  # report_file_name_prefix
                               "Test adding branching action Exit Block",
                               # test_suite_title
                               ("This test verifies advanced branching rule is applied for Exit Block action"
                                " and then verifies proper result in preview."),  # test_suite_description
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
@pytest.mark.C246571
def test_advBranch_exitblock(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test adding branching action Exit Block")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myDesign.click_addPageTitle("Page 1", "This is test page 1")
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1,
                                                          ["Miku", "Luka", "Rin"])
        for x in xrange(1):
            mySurvey.myCreate.newPage_viaSvysvc(mySurvey.survey_id, x + 2, "Page " + str(x + 2))
        driver.refresh()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_matrix_scale_question(mySurvey.survey_id, page_num,
                                                           "Please classify the following Ships", 2,
                                                           ["Haruna", "Yuudachi", "Naka"],
                                                           ["Destroyer(DD)", "Light Cruiser(CL)", "Battleship(BB)",
                                                            "Aircraft Carrier(CV)", "Submarine(SS)"])
        # code to create new block with page 1 and page 2
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_blockRandomizationButton()
        mySurvey.myLogic.click_blockRandom_newBlock()
        mySurvey.myLogic.addSequentialBlocks(["1: Page 1", "2: Page 2"])
        mySurvey.myLogic.blockRandomDone()
        # code to verify block randomization logic is applied or not
        ex = mySurvey.myLogic.verifyBlockRandomizationLogicApplied(2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify block logic applied",
                                 "checks to make sure that block logic applied.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify block logic applied."
        driver.refresh()
        # code to add branching logic on page 1
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("MultipleChoice", [1, 1], "equals", ["Miku"], "exitb", "default", None)])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Advanced Logic",
                                 "Verifies advanced logic window closed and logic saved.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to save advanced logic"
        # code test page logic on preview and test window
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

        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify branching rule with block randomization",
                                 "verifies advanced that branching rule is applied for Exit Block action",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching with block randomization"
        mySurvey.myDesign.return_from_preview_window()

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
