from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestMaxRowsColumnsInput/",  # report_relative_location
                               "test_max_rowsColumns_input",  # report_file_name_prefix
                               "verify text length for column and rows",  # test_suite_title
                               ("This test adds a matrix and menu matrix with max rows and columns "
                                " and then checks to make sure that we are unable to add characters past the max length"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver

    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_max_matrixRows(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify adding max columns on matrix question types.")
    try:
        mySurvey.myBuilder.click_MatrixRatingScaleAddButton()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(20))
        row = mySurvey.myLogic.RNG(251)
        column = mySurvey.myLogic.RNG(101)
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, row)
        mySurvey.myQuestion.enter_matrix_answerText(1, column)
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = True if mySurvey.myQuestion.verifyMatrixQuestionAnswer(1, 1) == row[:-1] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify maximum matrix rows",
                                 "checks to make sure that the warning pops up with maximum rows for matrix type reached",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify maximum rows for matrix."
        ex = True if mySurvey.myQuestion.verifyMatrixColumnAnswer(1, 1) == column[:-1] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify maximum matrix rows",
                                 "checks to make sure that the warning pops up with maximum columns for matrix type reached",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify maximum columns for matrix."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_max_menuMatrixRows(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify adding max columns on menu matrix question types.")
    try:
        mySurvey.myBuilder.click_MatrixOfDropdownMenusAddButton()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(20))
        row = mySurvey.myLogic.RNG(251)
        column = mySurvey.myLogic.RNG(101)
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, row)
        mySurvey.myQuestion.enter_matrix_answerText(1, column)
        mySurvey.myQuestion.enter_answer_choices_matrix_menu(1, mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = True if mySurvey.myQuestion.verifyMatrixQuestionAnswer(1, 1) == row[:-1] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify maximum menu matrix rows",
                                 "checks to make sure that the warning pops up with maximum rows for menu matrix type reached",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify maximum rows for menu matrix."
        ex = True if mySurvey.myQuestion.verifyMatrixColumnAnswer(1, 1) == column[:-1] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify maximum menu matrix columns",
                                 "checks to make sure that the warning pops up with maximum columns for menu matrix type reached",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify maximum columns for menu matrix."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
