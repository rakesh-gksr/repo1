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
                               "TestadvBranchVerifyAccordionToggelOnOffOptions/",  # report_relative_location
                               "test_advBranch_verifyAccordionToggleOnOffOptions",  # report_file_name_prefix
                               "Advanced branching deleting doesn't toggle off on accordion when source page for"
                               " branching is deleted",
                               # test_suite_title
                               ("This test verifies that toggled ON on accordion when advance branching logic "
                                "applied, and toggled OFF on accordion when advance branching logic removed."),
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
@pytest.mark.C195183
def test_advBranch_verifyAccordionToggleOnOffOptions(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Advanced branching deleting doesn't toggle off on " +
                                                           "accordion when source page for branching is deleted. " +
                                                           "Jira Id: CREATE-5945")
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
        # code to call method to verify page skip logic is on
        mySurvey.myLogic.verify_pageSkipOn()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Page Skip Logic On",
                                 "Verifies that the accordion page skip logic button shows ON.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Page Skip Logic ON"
        # code to call method to delete the page no 1
        ex = mySurvey.myCreate.nuke_page(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify page is deleted",
                                 "verifies that page is deleted.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify page is deleted"
        # code to call method to verify page skip logic is off
        ex = mySurvey.myLogic.verify_pageSkipOff()
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
