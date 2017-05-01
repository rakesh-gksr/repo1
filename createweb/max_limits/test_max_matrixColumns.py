from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestMaxMatrixColumns/",  # report_relative_location
                               "test_max_matrixColumns",  # report_file_name_prefix
                               "verify adding max columns on matrix and menu matrix question types",  # test_suite_title
                               ("This test adds a matrix with max columns choices "
                                " and then checks to make sure that an error notification appears when adding another one. Repeat for menu matrix"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver

    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_max_matrixColumns(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify adding max columns on matrix question types.")
    try:
        # add 13 matrix single choice question rows(options) via API
        mySurvey.myQuestion.create_question_massNewRow_insert(mySurvey.survey_id, "matrix", "single", 13, "column")
        driver.refresh()
        mySurvey.myQuestion.click_on_question_to_edit()
        # add 3 more rows (column options) via GUI
        # mySurvey.myQuestion.add_matrix_columnRow(13)
        for i in range(14, 17):
            row = mySurvey.myLogic.RNG(20)
            mySurvey.myQuestion.add_matrix_columnRow(i-1)
            mySurvey.myQuestion.enter_matrix_answerText(i, row)

        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question saved",
                                 "checks to make sure that save button not visible.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question saved."

        mySurvey.myQuestion.click_on_question_to_edit()
        # try to add 1 more row to check maximum allowed columns are not more than 16
        mySurvey.myQuestion.add_matrix_columnRow(1)
        ex = mySurvey.myQuestion.verify_maxMatrix_columnRow(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify maximum column error for "
                                                               "matrix type, only 16 rows allowed",
                                 "checks to make sure that the warning pops up with "
                                 "maximum column for matrix type reached",
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


def test_max_menuMatrixColumns(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify adding max columns on menu matrix question types.")
    try:
        mySurvey.myQuestion.create_question_massNewRow_insert(mySurvey.survey_id, "matrix", "menu", 6, "menu_columns")
        driver.refresh()

        mySurvey.myQuestion.click_on_question_to_edit()
        # add 3 more rows (column options) via GUI
        for i in range(7, 10):
            row = mySurvey.myLogic.RNG(20)
            mySurvey.myQuestion.add_matrix_columnRow(i - 1)
            mySurvey.myQuestion.enter_matrix_answerText(i, row)
            mySurvey.myQuestion.add_menuMatrix_dropdownRowText(i)

        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question saved",
                                 "checks to make sure that save button not visible.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question saved."
        mySurvey.myQuestion.click_on_question_to_edit()
        # try to add 1 more row to check maximum allowed columns are not more than 9
        mySurvey.myQuestion.add_matrix_columnRow(1)
        ex = mySurvey.myQuestion.verify_maxMenuMatrix_columnRow(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify maximum column error for menu matrix type",
                                 "checks to make sure that the warning pops up with maximum column for menu matrix type reached",
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
