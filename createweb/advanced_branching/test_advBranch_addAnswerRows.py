from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAdvBranchAddAnswerRows/",  # report_relative_location
                               "test_advBranch_addAnswerRows",  # report_file_name_prefix
                               "Test adding answer options after the rules apply",  # test_suite_title
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


def test_advBranch_addAnswerRows(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test adding answer options after the rules apply.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myDesign.click_addPageTitle("Page 1", "This is test page 1")
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1,
                                                          ["Miku", "Luka", "Rin", "Gumi"])
        for x in xrange(4):
            mySurvey.myCreate.newPage_viaSvysvc(mySurvey.survey_id, x + 2, "Page " + str(x + 2))
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("MultipleChoice", [1, 1], "equals", ["Luka"], "skip", "default", 4, "and"),
            ("MultipleChoice", [1, 1], "equals", ["Gumi"], "skip", "default", 4)])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Advanced Logic",
                                 "Verifies advanced logic window closed and logic saved.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to save advanced logic"
        # Answer 2 becomes Answer 3 and Answer 4 becomes answer 7
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.add_multipleChoice_answerRow(1)
        mySurvey.myQuestion.add_multipleChoice_answerRow(3)
        mySurvey.myQuestion.add_multipleChoice_answerRow(5)
        mySurvey.myQuestion.add_multipleChoice_answerRow(7)
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Len")
        mySurvey.myQuestion.enter_multipleChoice_answerText(4, "IA")
        mySurvey.myQuestion.enter_multipleChoice_answerText(6, "Ritsu")
        mySurvey.myQuestion.enter_multipleChoice_answerText(8, "Teto")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myLogic.verify_AnswerRows_advancedBranching("Q1", 1, ["C3", "C7"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching updated",
                                 "verifies that Page Skip Logic is on and that the Advanced Branching rule is updated.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Page Skip Logic On/Advanced Branching updated"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
