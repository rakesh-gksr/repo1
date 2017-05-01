from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAdvBranchQuestionMoveFromSourcePage/",  # report_relative_location
                               "test_advBranch_questionMoveFromSourcePage",  # report_file_name_prefix
                               "can't move question across pages with advanced branching rule",  # test_suite_title
                               "This test verifies that moving question across pages with advanced branching rule "
                               "works fine without error.",  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    env_init("platinum_advanced_branching")
    import datetime
    import os
    testcasename = os.path.basename(__file__).split(".")[0] + "--" + datetime.datetime.now().strftime("%I:%M%p %b %d, "
                                                                                                      "%Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.advBranch
@pytest.mark.IB
@pytest.mark.C195152
def test_advBranch_questionMoveFromSourcePage(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "can't move question across pages with advanced " +
                                                           "branching rule. Jira Id: CREATE-6097")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myDesign.click_addPageTitle("Page 1", "This is test page 1")
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1,
                                                          ["Miku", "Luka", "Rin"])
        # code to added new page into survey
        mySurvey.myCreate.newPage_viaSvysvc(mySurvey.survey_id, 2, "Page 2")
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
        mySurvey.myQuestion.click_on_question_to_edit()
        mySurvey.myQuestion.click_question_move_tab()
        ex = mySurvey.myLogic.moveQuestion(2, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Q1 Question moved from Page 1 to Page 2",
                                 "verifies that Q1 question moved from Page 1 to Page 2 successfully without "
                                 "any error.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to move the Q1 question moved from Page 1 to Page 2"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
