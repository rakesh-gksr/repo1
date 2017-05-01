from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAdvBranchDestPageBeforeCond/",  # report_relative_location
                               "test_advBranch_destPage_beforeCond",  # report_file_name_prefix
                               # test_suite_title
                               "Test reordering pages after adding rules- reorder skip logic destination page above conditional page",
                               ("This test adds certain advanced branching types "
                                " and then verifies proper result in preview."),  # test_suite_description
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


def test_advBranch_destPage_beforeCond(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Test reordering pages after adding rules- reorder skip logic destination page above conditional page.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myDesign.click_addPageTitle("Page 1", "This is test page 1")
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1,
                                                          ["Miku", "Luka", "Rin"])
        for x in xrange(2):
            mySurvey.myCreate.newPage_viaSvysvc(mySurvey.survey_id, x + 2, "Page " + str(x + 2))
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        # pytest.set_trace()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("MultipleChoice", [1, 1], "response", [None], "skip", "default", 3)])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Advanced Logic",
                                 "Verifies advanced logic window closed and logic saved.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to save advanced logic"
        # if we pass 'before' in this case then dest page position will be above than cond page
        mySurvey.myLogic.movePage(3, 1, "before")
        ex = mySurvey.myLogic.verify_num_advanced_branching(0)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching deleted",
                                 "verifies that Page Skip Logic is off and that the Advanced Branching rule is deleted.",
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
