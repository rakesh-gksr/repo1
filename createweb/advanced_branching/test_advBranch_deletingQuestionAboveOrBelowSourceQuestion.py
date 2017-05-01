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
                               "TestadvBranchDeletingQuestionAboveOrBelowSourceQuestion/",  # report_relative_location
                               "test_advBranch_deletingQuestionAboveOrBelowSourceQuestion",  # report_file_name_prefix
                               "can't delete question above or below source question for advanced branching",
                               # test_suite_title
                               ("This test verifies that deleting question on source page from above or below source"
                                " question works fine with out any error"),
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
@pytest.mark.C195148
def test_advBranch_deletingQuestionAboveOrBelowSourceQuestion(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "can't delete question above or below source question for "
                                                           "advanced branching. "
                                                           "Test Rail Id: C195148 "
                                                           "Jira Id: CREATE-6101")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myDesign.click_addPageTitle("Page 1", "This is test page 1")
        mySurvey.myQuestion.generate_ranking_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 2,
                                                          ["Miku", "Luka", "Rin", "Gumi"])

        mySurvey.myQuestion.generate_menu_matrix_question(
            mySurvey.survey_id, page_num,
            "Best Vocaloid?", 3)
        # code to added new page into survey
        mySurvey.myCreate.newPage_viaSvysvc(mySurvey.survey_id, 2, "Page 2")

        # code to add advance logic on page no 1
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("MultipleChoice", [1, 5], "equals", [None], "finish", "default", None)])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Advanced Logic",
                                 "Verifies advanced logic window closed and logic saved.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to save advanced logic"

        ex = mySurvey.myQuestion.hover_on_question_to_delete_it(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Delete Q1 Question",
                                 "Verifies Q1 deleted successfully.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to delete Q1 question"
        # after deleting Q1 question on page number 1, the third question become second question
        # Below is code to delete that third question which now become question second
        ex = mySurvey.myQuestion.hover_on_question_to_delete_it(2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Delete Q3 Question",
                                 "Verifies Q3 deleted successfully.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to delete Q3 question"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
