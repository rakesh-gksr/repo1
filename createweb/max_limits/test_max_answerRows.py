from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestMaxAnswerRows/",  # report_relative_location
                               "test_max_answerRows",  # report_file_name_prefix
                               "verify adding max answer choices for all question types",  # test_suite_title
                               ("This test adds certain question types "
                                " and then checks to make sure there is a max number of answer rows."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename

def test_max_answerRows_multipleChoice(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Max number of Answer Rows for multiple choice type questions.")
    try:
        # add multiple choice question with 195 rows(options) via API
        mySurvey.myQuestion.create_question_massNewRow_insert(mySurvey.survey_id, "single_choice", "vertical", 195)
        driver.refresh()
        mySurvey.myQuestion.click_on_question_to_edit()
        # add 5 more rows (options) via GUI
        mySurvey.myQuestion.add_multipleChoice_answerRow(195)
        for i in range(196, 201):
            row = mySurvey.myLogic.RNG(20)
            mySurvey.myQuestion.enter_multipleChoice_answerText(i, row)

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
        mySurvey.myQuestion.add_multipleChoice_answerRow(1)
        ex = mySurvey.myQuestion.verify_max_num_answer_rows()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify maximum answer rows warning",
                                 "checks to make sure that the warning pops up with maximum answer rows reached",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify maximum answer rows for multiple choice."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_max_answerRows_dropdown(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Max number of Answer Rows for Dropdown type questions.")
    try:
        # add dropdown question with 495 rows(options) via API
        mySurvey.myQuestion.create_question_massNewRow_insert(mySurvey.survey_id, "single_choice", "menu", 495)
        driver.refresh()

        mySurvey.myQuestion.click_on_question_to_edit()
        # add 5 more rows (options) via GUI
        mySurvey.myQuestion.add_multipleChoice_answerRow(495)
        for i in range(496, 501):
            row = mySurvey.myLogic.RNG(20)
            mySurvey.myQuestion.enter_multipleChoice_answerText(i, row)

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
        mySurvey.myQuestion.add_multipleChoice_answerRow(1)
        ex = mySurvey.myQuestion.verify_max_num_answer_rows(True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify maximum answer rows warning",
                                 "checks to make sure that the warning pops up with maximum answer rows reached",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify maximum answer rows for Dropdown."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_max_answerRows_multiTextbox(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Max number of Answer Rows for multiple textbox type questions.")
    try:
        # add multiple textbox question with 195 rows(options) via API
        mySurvey.myQuestion.create_question_massNewRow_insert(mySurvey.survey_id, "open_ended", "multi", 195)
        driver.refresh()

        mySurvey.myQuestion.click_on_question_to_edit()
        # add 5 more rows (textbox options) via GUI
        mySurvey.myQuestion.add_multipleChoice_answerRow(195)
        for i in range(196, 201):
            row = mySurvey.myLogic.RNG(20)
            mySurvey.myQuestion.enter_multipleChoice_answerText(i, row)

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
        mySurvey.myQuestion.add_multipleChoice_answerRow(1)  # error message not implemented
        ex = mySurvey.myQuestion.verify_max_num_answer_rows()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify maximum answer rows warning",
                                 "checks to make sure that the warning pops up with maximum answer rows reached",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify maximum answer rows for multiple textbox."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_max_answerRows_ranking(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Max number of Answer Rows for ranking type questions.")
    try:
        # add matrix ranking question with 195 rows(options) via API
        mySurvey.myQuestion.create_question_massNewRow_insert(mySurvey.survey_id, "matrix", "ranking", 195)
        driver.refresh()

        mySurvey.myQuestion.click_on_question_to_edit()
        # add 5 more rows (ranking options) via GUI
        mySurvey.myQuestion.add_multipleChoice_answerRow(195)
        for i in range(196, 201):
            row = mySurvey.myLogic.RNG(20)
            mySurvey.myQuestion.enter_multipleChoice_answerText(i, row)

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
        mySurvey.myQuestion.add_multipleChoice_answerRow(1)  # error message not implemented
        ex = mySurvey.myQuestion.verify_max_num_answer_rows()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify maximum answer rows warning",
                                 "checks to make sure that the warning pops up with maximum answer rows reached",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify maximum answer rows for ranking."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_max_answerRows_datetime(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Max number of Answer Rows for datetime type questions.")
    try:
        # add multiple datetime question with 195 rows(options) via API
        mySurvey.myQuestion.create_question_massNewRow_insert(mySurvey.survey_id, "datetime", "date_us", 195)
        driver.refresh()

        mySurvey.myQuestion.click_on_question_to_edit()
        # add 5 more rows (datetime options) via GUI
        mySurvey.myQuestion.add_multipleChoice_answerRow(195)
        for i in range(196, 201):
            row = mySurvey.myLogic.RNG(20)
            mySurvey.myQuestion.enter_multipleChoice_answerText(i, row)

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
        mySurvey.myQuestion.add_multipleChoice_answerRow(1)  # error message not implemented
        ex = mySurvey.myQuestion.verify_max_num_answer_rows()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify maximum answer rows warning",
                                 "checks to make sure that the warning pops up with maximum answer rows reached",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify maximum answer rows for datetime."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
