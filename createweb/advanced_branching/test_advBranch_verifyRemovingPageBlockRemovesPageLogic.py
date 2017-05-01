from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAdvBranchVerifyRemovingPageBlockRemovesPageLogic/",  # report_relative_location
                               "test_advBranch_verifyRemovingPageBlockRemovesPageLogic",  # report_file_name_prefix
                               ("Advanced Branching is shown enabled, but the 'Exit Block' rule is not displayed if" +
                                " the page is removed from the block"),
                               # test_suite_title
                               ("This test verifies advanced branching rule get removed if the page is removed from "
                                "the block."),  # test_suite_description
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
@pytest.mark.C195172
def test_advBranch_verifyRemovingPageBlockRemovesPageLogic(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, ("Advanced Branching is shown enabled, " +
                                                            "but the 'Exit Block' rule is not displayed if the page " +
                                                            "is removed from the block"))
    try:

        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myDesign.click_addPageTitle("Page 1", "This is test page 1")
        mySurvey.myQuestion.generate_matrix_scale_question(mySurvey.survey_id, page_num,
                                                           "Please classify the following Ships", 1,
                                                           ["Haruna", "Yuudachi", "Naka"],
                                                           ["Destroyer(DD)", "Light Cruiser(CL)", "Battleship(BB)",
                                                            "Aircraft Carrier(CV)", "Submarine(SS)"])
        for x in xrange(3):
            mySurvey.myCreate.newPage_viaSvysvc(mySurvey.survey_id, x + 2, "Page " + str(x + 2))
        driver.refresh()
        page_num = mySurvey.myDesign.getPageID(2)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 2,
                                                          ["Miku", "Luka", "Rin"])

        # Add new page block with page 2 and page 3
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_blockRandomizationButton()
        mySurvey.myLogic.click_blockRandom_newBlock()
        mySurvey.myLogic.addSequentialBlocks(["2: Page 2", "3: Page 3"])
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
        # code to add new branching rule
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P2: Page 2")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("MultipleChoice", [2, 1], "equals", ["Miku"], "exitb", "default", None)])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Advanced Logic",
                                 "Verifies advanced logic window closed and logic saved.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to save advanced logic"
        # code to call method to verify page skip logic is on
        mySurvey.myLogic.verify_pageSkipOn()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Page Skip Logic On",
                                 "Verifies that the accordion page skip logic button shows ON.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Page Skip Logic ON"
        # code to remove page block with page 2 and page 3
        mySurvey.myLogic.click_blockRandomizationButton()
        mySurvey.myLogic.click_blockRandomization_editBlock()
        ex = mySurvey.myLogic.click_blockRandomization_killBlock(["2: Page 2", "3: Page 3"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify block deletion",
                                 "checks to make sure that block deleted.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify block deletion."
        # code to call method to verify page skip logic is off
        mySurvey.myLogic.verify_pageSkipOff()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Page Skip Logic Off",
                                 "Verifies that the accordion page skip logic button shows OFF.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Page Skip Logic OFF"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
