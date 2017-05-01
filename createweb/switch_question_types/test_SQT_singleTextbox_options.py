from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):

    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSQTSingleTextboxOptions/",  # report_relative_location
                               "test_SQT_singleTextbox_options",  # report_file_name_prefix
                               "verify switching from menu matrix to single textbox ",  # test_suite_title
                               ("This test suite adds a a menu matrix question and switches it to a single textbox question   "
                                " Test verifies question options and question saves."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_SQT_singleTextbox_options(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify switching from menu matrix to single textbox")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_MatrixOfDropdownMenusAddButton()
        answerRows = []
        matrixRows = []
        menuRows = []
        title = mySurvey.myLogic.RNG(30)
        mySurvey.myQuestion.enter_question_title(title)
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[0])
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[1])
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, answerRows[2])
        matrixRows.append(mySurvey.myLogic.RNG(10))
        matrixRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_matrix_answerText(1, matrixRows[0])
        mySurvey.myQuestion.enter_matrix_answerText(2, matrixRows[1])
        menuRows.append(mySurvey.myLogic.RNG(10))
        menuRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_answer_choices_matrix_menu(1, menuRows[0])
        mySurvey.myQuestion.enter_answer_choices_matrix_menu(2, menuRows[1])
        mySurvey.myQuestion.changeQType("SingleTextbox")
        mySurvey.myQuestion.click_question_options_tab()
        ex = mySurvey.myQuestion.verify_all_options(["required", "random_choice", "adjust_layout", "question_a_b"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question options present",
                                 "verifies that all options are present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question options"
        mySurvey.myQuestion.click_question_save_from_options_tab()
        mySurvey.myDesign.scroll_to_top()
        ex = True if mySurvey.myQuestion.verifyQuestionTitle(1) == title else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify title is correct",
                                 "verifies that the title of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify title"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
