from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAdvBranchSaving/",  # report_relative_location
                               "test_advBranch_saving",  # report_file_name_prefix
                               # test_suite_title
                               "Test saving rules after selecting actions skip/hide/show page/questions which doesn't have any questions/page to select",
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


def test_advBranch_saving(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test saving rules after selecting actions skip/hide/show page/questions which doesn't have any questions/page to select.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myDesign.click_addPageTitle("Page 1", "This is test page 1")
        mySurvey.myQuestion.generate_ranking_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1)
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        try:
            ex = mySurvey.myLogic.addNewBranchingRule([
                ("matrix", [1, 1, 1], "equals", [2], "skip", "default", 2)])
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Advanced Logic",
                                 "Verifies advanced logic window closed and logic saved.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
            assert ex, "Failed to save advanced logic"
        except AttributeError:
            mySurvey.myLogic.closeDropdownActionItem()
            ex = True if mySurvey.myLogic.advBranching_add_action("finish", "default", None) else False
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify CREATE-4991",
                                     "Tries to page skip to non existant page and reselects end survey.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
        assert ex, "Failed to saving defect from CREATE-4991"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
