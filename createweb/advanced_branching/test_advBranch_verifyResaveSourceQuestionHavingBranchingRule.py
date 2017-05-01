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
                               "TestadvBranchVerifyResaveSourceQuestionHavingBranchingRule/",  # report_relative_location
                               "test_advBranch_verifyResaveSourceQuestionHavingBranchingRule",  # report_file_name_prefix
                               "can't re-save source question + all other questions on a survey "
                               "having branching rule",  # test_suite_title
                               ("This test verifies that re-save source question and all other question having"
                                " branching rule save successfully "),  # test_suite_description
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

@pytest.mark.advBranch
@pytest.mark.IB
@pytest.mark.C195143
def test_advBranch_verifyResaveSourceQuestionHavingBranchingRule(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "can't re-save source question + all other questions on"
                                                           " a survey having branching rule")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myDesign.click_addPageTitle("Page 1", "This is test page 1")
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1,
                                                          ["Miku", "Luka", "Rin", "Gumi"])
        # code to added new page into survey
        mySurvey.myCreate.newPage_viaSvysvc(mySurvey.survey_id, 2, "Page 2" )
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
        # edit question no 1 on page 1
        mySurvey.myQuestion.click_on_question_to_edit(1)
        # re save question question after editing question
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the save button after editing Q1",
                                 "Verifies that Q1 question saved successfully.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click save button"
        # add more questions
        mySurvey.myQuestion.generate_ranking_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 2)
        mySurvey.myQuestion.generate_menu_matrix_question(
            mySurvey.survey_id, page_num,
            "Best Vocaloid?", 3)
        # edit question no 2 on page 1
        mySurvey.myQuestion.click_on_question_to_edit(2)
        # re save question question after editing question
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the save button after editing Q2",
                                 "Verifies that Q2 question saved successfully.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click save button"
        # edit question no 3 on page 1
        mySurvey.myQuestion.click_on_question_to_edit(3)
        # re save question question after editing question
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the save button after editing Q3",
                                 "Verifies that Q3 question saved successfully.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click save button"



    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
