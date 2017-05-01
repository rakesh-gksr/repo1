

from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from dynamic_tests.dynamic_tests_config import page_move_test_info
import traceback
import pytest

__author__ = 'rakesh'


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestadvBranchPageMove/",  # report_relative_location
                               "test_advBranch_pageMove",  # report_file_name_prefix
                               "moving page with adv branching logic applied",
                               # test_suite_title
                               "This test verifies that page moving works fine with adv branching logic without"
                               " any error",
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
@pytest.mark.C195151
@pytest.mark.C195178
@pytest.mark.C195182
@pytest.mark.parametrize("test_info", page_move_test_info,
                         ids=[dict["test_case_title"] for dict in page_move_test_info])
def test_advBranch_pageMove(create_survey, test_info):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, test_info["test_case_title"] +
                             " Jira Id " + test_info["jira_id"])
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myDesign.click_addPageTitle("Page 1", "This is test page 1")
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 2,
                                                          ["Miku", "Luka", "Rin", "Gumi"])
        # code to added new page into survey
        mySurvey.myCreate.newPage_viaSvysvc(mySurvey.survey_id, 2, "Page 2")
        driver.refresh()
        # code to add advance logic on page no 1
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule(test_info["branching_rule"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Advanced Logic",
                                 "Verifies advanced logic window closed and logic saved.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to save advanced logic"

        # code to page moving from source to destination
        ex = mySurvey.myLogic.movePage(test_info["params"]["pFrom"],
                                       test_info["params"]["pTo"],
                                       test_info["params"]["position"])

        report.add_report_record(ReportMessageTypes.TEST_STEP, test_info["page_move_step_title"],
                                 test_info["page_move_step_desc"],
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to move Page"

        if test_info["advance_branching_off"]:
            ex = mySurvey.myLogic.verify_num_advanced_branching(1, ["SKIP TO", "P2"])
            ex = not ex
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching deleted",
                                     "verifies that Page Skip Logic is off and that the Advanced Branching rule"
                                     " is deleted.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify Page Skip Logic Off/Advanced Branching deleted"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
