from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAdvBranchVerifyBranchingActionExitBlock/",  # report_relative_location
                               "test_advBranch_verifyBranchingActionExitBlock",  # report_file_name_prefix
                               "Branching action 'Exit block' should be exclusive",
                               # test_suite_title
                               ("This test verifies that when branching action 'exit block' is selected" +
                                " on first 'add action' menu then all the branching action got hidden" +
                                " in second 'add action' menu."),  # test_suite_description
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
@pytest.mark.C195187
def test_advBranch_verifyBranchingActionExitBlock(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Branching action 'Exit block' should be exclusive")
    try:

        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myDesign.click_addPageTitle("Page 1", "This is test page 1")
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1,
                                                          ["Miku", "Luka", "Rin"])
        for x in xrange(3):
            mySurvey.myCreate.newPage_viaSvysvc(mySurvey.survey_id, x + 2, "Page " + str(x + 2))
        driver.refresh()
        # code to create new block with page 1 and page 2
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_blockRandomizationButton()
        mySurvey.myLogic.click_blockRandom_newBlock()
        mySurvey.myLogic.addSequentialBlocks(["1: Page 1", "2: Page 2"])
        mySurvey.myLogic.blockRandomDone()
        # code to create new block with page 3 and page 4
        mySurvey.myLogic.click_blockRandomizationButton()
        mySurvey.myLogic.click_blockRandom_newBlock()
        mySurvey.myLogic.addSequentialBlocks(["3: Page 3", "4: Page 4"])
        mySurvey.myLogic.blockRandomDone()
        # code to verify block randomization logic is applied or not
        ex = mySurvey.myLogic.verifyBlockRandomizationLogicApplied(4)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify block logic applied",
                                 "checks to make sure that block logic applied.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify block logic applied."
        # code to add branching logic on page 1
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        # code to add branching logic condition
        ex = mySurvey.myLogic.addNewBranchingCondition(1, 1, "equals", "Miku")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Add Advanced Logic Condition",
                                 "Verifies advanced logic condition added.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add advanced logic condition"
        # code to add branching logic action
        ex = mySurvey.myLogic.addBranchingAction(1, 'exitb')
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Add Advanced Logic Action",
                                 "Verifies advanced logic action added.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add advanced logic action"
        # code verify advanced branching actions are not available
        ex = mySurvey.myLogic.verifyBranchingActionsHidden(2, ["exitb','skip','finish','disqualify"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching Actions",
                                 "Verifies that advanced branching actions are not available ",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that advanced branching actions are not available"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
