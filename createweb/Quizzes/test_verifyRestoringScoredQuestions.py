from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestVerifyRestoringScoredQuestions/",  # report_relative_location
                               "test_verifyRestoringScoredQuestions",  # report_file_name_prefix
                               # test_suite_title
                               ("Verify that the Restoring a scored questions restores the scores of the answer "
                                "choices along with the Scoring selection"),
                               ("Test to verify that the Restoring a scored questions restores the scores of the "
                                "answer choices along with the Scoring selection"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().\
        strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.quiz
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C16435221
def test_verify_restoring_scored_questions(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify that the Restoring a scored questions restores the scores of the answer choices along with "
        "the Scoring selection")
    try:
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.question_quiz_toggle_on()
        ex = mySurvey.myQuestion.verify_question_quiz_toggle(True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Scoring Checkbox",
                                 "Verifies that that scoring checkbox is present and checked in multiple "
                                 "choice question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scoring checkbox is present and checked in multiple choice question type."
        mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Red")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Blue")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Green")
        score_input = (10, 20, 30)
        for i in range(1, 4):
            mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(i, score_input[i-1])
            ex = mySurvey.myQuestion.verify_quiz_score(i, score_input[i-1])
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Dropdown Score Value",
                                     "Verifies that dropdown value of answer field " + str(i) + " is " +
                                     str(score_input[i-1]),
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify that dropdown value of answer field " + str(i) + " is " + str(score_input[i-1])
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Multiple Choice Question Type",
                                 "Verifies that Multiple Choice question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Multiple Choice question added to live preview."
        mySurvey.myOptions.wait_until_accordion_quiz_update()
        ex = mySurvey.myQuestion.hover_on_question_to_delete_it(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Delete Multiple Choice question",
                                 "Verifies that Multiple Choice is deleted.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Multiple Choice question deleted."
        mySurvey.myCreate.restoreDeletedQuestion(1)
        mySurvey.myQuestion.click_on_question_to_edit(1)
        for i in range(1, 4):
            ex = mySurvey.myQuestion.verify_quiz_score(i, score_input[i - 1])
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Dropdown Score Value",
                                     "Verifies that dropdown value of answer field " + str(i) + " is " + str(
                                         score_input[i - 1]),
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify that dropdown value of answer field " + str(i) + " is " + str(
                score_input[i - 1])
        mySurvey.myQuestion.click_question_save_from_edit_tab()

        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.turn_on_multiple_answers()
        ex = mySurvey.myQuestion.verify_question_quiz_toggle(True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Scoring Checkbox",
                                 "Verifies that that scoring checkbox is present and checked in multiple "
                                 "choice multi select question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scoring checkbox is present and checked in multiple choice multi select " \
                   "question type."
        mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Red")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Blue")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Green")
        score_input = (10, 20, 30)
        for i in range(1, 4):
            mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(i, score_input[i - 1])
            ex = mySurvey.myQuestion.verify_quiz_score(i, score_input[i - 1])
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Dropdown Score Value",
                                     "Verifies that dropdown value of answer field " + str(i) + " is " + str(
                                         score_input[i - 1]),
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify that dropdown value of answer field " + str(i) + " is " + \
                       str(score_input[i - 1])
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Multiple Choice Multi Select Question Type",
                                 "Verifies that Multiple Choice Multi Select question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Multiple Choice Multi Select question added to live preview."
        ex = mySurvey.myQuestion.hover_on_question_to_delete_it(2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Delete Multiple Choice Multi Select question",
                                 "Verifies that Multiple Choice Multi Select is deleted.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Multiple Choice Multi Select question deleted."
        mySurvey.myCreate.restoreDeletedQuestion(1)
        mySurvey.myQuestion.click_on_question_to_edit(2)
        for i in range(1, 4):
            ex = mySurvey.myQuestion.verify_quiz_score(i, score_input[i - 1])
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Dropdown Score Value",
                                     "Verifies that dropdown value of answer field " + str(i) + " is " + str(
                                         score_input[i - 1]),
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify that dropdown value of answer field " + str(i) + " is " + str(
                score_input[i - 1])
        mySurvey.myQuestion.click_question_save_from_edit_tab()

        mySurvey.myBuilder.click_DropdownAddButton()
        mySurvey.myQuestion.question_quiz_toggle_on()
        ex = mySurvey.myQuestion.verify_question_quiz_toggle(True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Scoring Checkbox",
                                 "Verifies that that scoring checkbox is present and checked in Dropdown question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scoring checkbox is present and checked in Dropdown question type."
        mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Red")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Blue")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Green")
        score_input = (10, 20, 30)
        for i in range(1, 4):
            mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(i, score_input[i - 1])
            ex = mySurvey.myQuestion.verify_quiz_score(i, score_input[i - 1])
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Dropdown Score Value",
                                     "Verifies that dropdown value of answer field " + str(i) + " is " + str(
                                         score_input[i - 1]),
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify that dropdown value of answer field " + str(i) + " is " + \
                       str(score_input[i - 1])
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Dropdown Question Type",
                                 "Verifies that Dropdown question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Dropdown question added to live preview."
        ex = mySurvey.myQuestion.hover_on_question_to_delete_it(3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Delete Dropdown question",
                                 "Verifies that Dropdown question is deleted.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Dropdown question deleted."
        mySurvey.myCreate.restoreDeletedQuestion(1)
        mySurvey.myQuestion.click_on_question_to_edit(3)
        for i in range(1, 4):
            ex = mySurvey.myQuestion.verify_quiz_score(i, score_input[i - 1])
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Dropdown Score Value",
                                     "Verifies that dropdown value of answer field " + str(i) + " is " + str(
                                         score_input[i - 1]),
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify that dropdown value of answer field " + str(i) + " is " + str(
                score_input[i - 1])
        mySurvey.myQuestion.click_question_save_from_edit_tab()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
