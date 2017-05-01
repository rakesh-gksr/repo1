from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestVerifyScoringCheckboxForQuestions/",  # report_relative_location
                               "test_verifyScoringCheckboxForQuestions",  # report_file_name_prefix
                               # test_suite_title
                               "Verify the scoring is checked for all the scoring questions added once Quiz is Enabled",
                               ("Test to verify the scoring is checked for all the scoring questions added once "
                                "Quiz is Enabled"),  # test_suite_description
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
@pytest.mark.C12809381
def test_verify_quiz_option_in_accordion(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        " 	Verify the scoring is checked for all the scoring questions added once Quiz is Enabled")
    try:
        mySurvey.myOptions.unfold_OptionsRegion()
        mySurvey.myOptions.toggle_quiz_mode(display_quiz_result=False, show_collect_answers=False)
        ex = mySurvey.myOptions.verify_quiz_toggle(True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Quiz Mode is On",
                                 "Verifies that quiz mode is on",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify quiz mode is on."

        mySurvey.myBuilder.click_MultipleChoiceAddButton()
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
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Kongou")
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(1, 5)
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Hiei")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Kirishima")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Multiple Choice Question Type",
                                 "Verifies that Multiple Choice question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Multiple Choice question added to live preview."

        mySurvey.myBuilder.click_DropdownAddButton()
        ex = mySurvey.myQuestion.verify_question_quiz_toggle(True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Scoring Checkbox",
                                 "Verifies that scoring checkbox is present and checked in dropdown question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scoring checkbox is present and checked in dropdown question."
        mySurvey.myQuestion.enter_question_title("This wormhole leads to...")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "A room with a moose")
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(1, 5)
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Fluffy Pillows")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Pixels")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Dropdown Question Type",
                                 "Verifies that Dropdown question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Dropdown question added to live preview."

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.quiz
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C12809382
def test_verify_scoring_questions(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify the Multiple choice and Drop down questions are Scoring questions")
    try:
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Kongou")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Hiei")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Kirishima")
        mySurvey.myQuestion.question_quiz_toggle_on()

        ex = mySurvey.myQuestion.verify_row_quiz_points()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Select the checkbox Score this question for multiple choice",
                                 "Verifies value drop down appears in front of all the answer choices.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify drop down appears in front of all the answer choices."

        mySurvey.myQuestion.turn_on_multiple_answers()
        ex = mySurvey.myQuestion.verify_question_quiz_toggle()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Use checkboxes for the multiple choice question",
                                 "Verifies that the option Score this question is present selected.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that the option Score this question is present selected."

        mySurvey.myQuestion.click_question_cancel_from_edit_tab()
        mySurvey.myBuilder.click_DropdownAddButton()
        mySurvey.myQuestion.enter_question_title("This wormhole leads to...")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "A room with a moose")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Fluffy Pillows")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Pixels")
        mySurvey.myQuestion.question_quiz_toggle_on()

        ex = mySurvey.myQuestion.verify_question_quiz_toggle()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Select the checkbox Score this question for drop down",
                                 "Verifies that the option Score this question is present selected.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that the option Score this question is present selected."

        ex = mySurvey.myQuestion.verify_row_quiz_points()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Select the checkbox Score this question for drop down",
                                 "Verifies value drop down appears in front of all the answer choices.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify drop down appears in front of all the answer choices."

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.quiz
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C12809394
def test_multiple_choices_same_scores(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify multiple answer choices can have same scores")
    try:
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.question_quiz_toggle_on()
        ex = mySurvey.myQuestion.verify_question_quiz_toggle(is_toggle_on=True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Scoring Checkbox",
                                 "Verifies that that scoring checkbox is present and checked in multiple "
                                 "choice question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scoring checkbox is present and checked in multiple choice question type."

        mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Kongou")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Hiei")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Kirishima")
        for i in range(1, 4):
            mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(i, 2)
        ex = mySurvey.myQuestion.verify_max_quiz_score(2)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Enter scores for answer choices",
                                 "Verifies that the max score for multiple choices.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that the max score for multiple choices."

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

        mySurvey.myBuilder.click_DropdownAddButton()
        ex = mySurvey.myQuestion.verify_row_quiz_points()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Select the checkbox Score this question for drop down",
                                 "Verifies value drop down appears in front of all the answer choices.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify drop down appears in front of all the answer choices."
        mySurvey.myQuestion.enter_question_title("This wormhole leads to...")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "A room with a moose")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Fluffy Pillows")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Pixels")
        for i in range(1, 4):
            mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(i, 2)
        ex = mySurvey.myQuestion.verify_max_quiz_score(2)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Enter scores for answer choices",
                                 "Verifies that the max score for drop down.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that the max score for drop down."

        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Dropdown Question Type",
                                 "Verifies that Dropdown question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Dropdown question added to live preview."

        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        ex = mySurvey.myQuestion.verify_row_quiz_points()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Select the checkbox Score this question for multi choice multi select",
                                 "Verifies value drop down appears in front of all the answer choices.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify drop down appears in front of all the answer choices."

        mySurvey.myQuestion.enter_question_title("Multi choice multi select quesiton?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "A")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "B")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "C")
        for i in range(1, 4):
            mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(i, 2)
        mySurvey.myQuestion.turn_on_multiple_answers()
        ex = mySurvey.myQuestion.verify_max_quiz_score(6)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Enter scores for answer choices",
                                 "Verifies that the max score for multi choice multi select.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that the max score for multi choice multi select."

        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Multiple Choice Multi Select Question Type",
                                 "Verifies that Multiple Choice Multi Select question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Multiple Choice Multi Select question added to live preview."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.quiz
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C12809392
def test_max_score_updated(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify multiple answer choices can have same scores")
    try:
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Kongou")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Hiei")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Kirishima")
        mySurvey.myQuestion.question_quiz_toggle_on()

        ex = mySurvey.myQuestion.verify_row_quiz_points()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Select the checkbox Score this question for multiple choice",
                                 "Verifies value drop down appears in front of all the answer choices.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify drop down appears in front of all the answer choices."

        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(1, 5)
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(2, 10)
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(3, 15)
        ex = mySurvey.myQuestion.verify_max_quiz_score(15)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Enter scores for answer choices",
                                 "Verifies that the max score for multiple choices.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that the max score for multiple choices."
        mySurvey.myQuestion.delete_multipleChoice_answerRow(2)
        ex = mySurvey.myQuestion.verify_max_quiz_score(15)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Delete a row choice",
                                 "Verifies that the max score for multiple choices.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that the max score for multiple choices."

        mySurvey.myQuestion.add_multipleChoice_answerRow(3)
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Hiei")
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(3, 10)
        mySurvey.myQuestion.delete_multipleChoice_answerRow(2)
        ex = mySurvey.myQuestion.verify_max_quiz_score(10)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Delete max score points row",
                                 "Verifies that the max score gets updated.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that the max score gets updated."

        mySurvey.myQuestion.click_question_save_from_edit_tab()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.quiz
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C12809409
def test_quiz_mode_on_automatically(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify going from 0 to 1 scored question automatically turns on quiz mode")
    try:
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Kongou")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Hiei")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Kirishima")
        mySurvey.myQuestion.question_quiz_toggle_on()

        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(1, 1)
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(2, 1)
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(3, 1)

        ex = mySurvey.myQuestion.verify_question_quiz_toggle(is_toggle_on=True)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Enable Scoring by selecting checkbox score this question",
                                 "Verifies that the checkbox is selected.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that the checkbox is selected."

        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myOptions.verify_quiz_toggle(is_toggle_on=True)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Check QUIZ in Options in the accordion",
                                 "Verifies that the Quiz is automatically turned on.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that the Quiz is automatically turned on."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.quiz
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C16638897
def test_max_score_multi_select(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify Max Score gets updated while deleting an answer choice in Multi Select question")
    try:
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title("What is your favourite color?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Red")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Blue")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Green")
        mySurvey.myQuestion.turn_on_multiple_answers()
        mySurvey.myQuestion.question_quiz_toggle_on()

        ex = mySurvey.myQuestion.verify_row_quiz_points()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Select the checkbox Score this question for multiple choice",
                                 "Verifies value drop down appears in front of all the answer choices.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify drop down appears in front of all the answer choices."

        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(1, 10)
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(2, 20)
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(3, 30)
        ex = mySurvey.myQuestion.verify_max_quiz_score(60)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Enter scores for answer choices",
                                 "Verifies that the max score for multi choice multi select.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that the max score for multi choice multi select."
        mySurvey.myQuestion.delete_multipleChoice_answerRow(1)
        ex = mySurvey.myQuestion.verify_max_quiz_score(50)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Delete a row choice",
                                 "Verifies that the max score for multi choice multi select.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that the max score for multi choice multi select."

        mySurvey.myQuestion.click_question_save_from_edit_tab()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.quiz
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C16440780
def test_quiz_radio_button(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify clicking on left Icon on answer option add value as 1")
    try:
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title("What is your favourite color?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Red")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Blue")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Green")
        mySurvey.myQuestion.question_quiz_toggle_on()

        ex = mySurvey.myQuestion.verify_row_quiz_points()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Select the checkbox Score this question for multiple choice",
                                 "Verifies value drop down appears in front of all the answer choices.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify drop down appears in front of all the answer choices."

        mySurvey.myQuestion.click_quiz_radio_button(1)
        ex = mySurvey.myQuestion.verify_quiz_score(antNum=1, expected_score=1)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Select the Left icon for answer choice",
                                 "Check that the score of Red gets 1 from 0.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify check that the score of Red gets 1 from 0."

        mySurvey.myQuestion.click_quiz_radio_button(1)
        ex = mySurvey.myQuestion.verify_quiz_score(antNum=1, expected_score=0)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Select the Left icon for answer choice",
                                 "Check that the score of Red gets 0 from 1.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify check that the score of Red gets 0 from 1."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.quiz
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C12809413
def test_score_persist_quiz_turned_off(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify the Scores persist when the Quiz is turned \
         off at Survey level and the scoring is Enabled at Question level")
    try:
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.question_quiz_toggle_on()
        ex = mySurvey.myQuestion.verify_question_quiz_toggle(is_toggle_on=True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Scoring Checkbox",
                                 "Verifies that that scoring checkbox is present and checked in multiple "
                                 "choice question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scoring checkbox is present and checked in multiple choice question type."

        mySurvey.myQuestion.enter_question_title("What is your favourite color?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Red")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Blue")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Green")
        score_input = (2, 4, 6)
        for i in range(1, 4):
            mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(i, score_input[i - 1])
            ex = mySurvey.myQuestion.verify_quiz_score(i, score_input[i - 1])
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Dropdown Score Value",
                                     "Verifies that dropdown value of answer field " + str(i) + " is " +
                                     str(score_input[i - 1]),
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify that dropdown value of answer field " + str(i) + " is " + str(
                score_input[i - 1])
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

        mySurvey.myBuilder.click_DropdownAddButton()
        mySurvey.myQuestion.enter_question_title("This wormhole leads to...")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "A room with a moose")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Fluffy Pillows")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Pixels")
        score_input = (5, 10, 15)
        for i in range(1, 4):
            mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(i, score_input[i - 1])
            ex = mySurvey.myQuestion.verify_quiz_score(i, score_input[i - 1])
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Dropdown Score Value",
                                     "Verifies that dropdown value of answer field " + str(i) + " is " +
                                     str(score_input[i - 1]),
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify that dropdown value of answer field " + str(i) + " is " + str(
                score_input[i - 1])

        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Dropdown Question Type",
                                 "Verifies that Dropdown question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Dropdown question added to live preview."

        mySurvey.myOptions.unfold_OptionsRegion()
        mySurvey.myOptions.on_off_quiz_mode()
        quiz_mode_title = mySurvey.myQuestion.check_quiz_mode_popup_title()
        popup_title = "Disabling quiz mode will remove scoring from all your questions."
        ex = False
        if quiz_mode_title == popup_title:
            ex = True
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify popup title",
                                 "Checks title of quiz mode popup to make sure it appears.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify quiz mode popup title existence."

        ex = mySurvey.myQuestion.check_quiz_mode_popup_cancel()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify popup cancel button",
                                 "Checks cancel button exist into quiz mode popup window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify cancel button exist into quiz mode popup window."

        ex = mySurvey.myQuestion.check_quiz_mode_popup_unscore()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify popup unscore all button",
                                 "Checks unscore all button exist into quiz mode popup window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify unscore all button exist into quiz mode popup window."

        mySurvey.myQuestion.click_quiz_mode_popup_unscore()
        ex = mySurvey.myOptions.verify_quiz_toggle(False)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Quiz Mode is OFF",
                                 "Verifies that quiz mode is OFF",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify quiz mode is OFF."
        mySurvey.myOptions.wait_until_accordion_quiz_update()

        ex1 = mySurvey.myQuestion.verifyQuizIndicator(1)
        ex2 = mySurvey.myQuestion.verifyQuizIndicator(2)
        ex = not (ex1 and ex2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Turn off Quiz",
                                 "Verifies that Quiz is turned off and all the socring questions are Unscored",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Quiz is turned off and all the socring questions are Unscored"

        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.question_quiz_toggle_on()
        ex1 = mySurvey.myQuestion.verify_quiz_score(1, 2)
        ex2 = mySurvey.myQuestion.verify_quiz_score(2, 4)
        ex3 = mySurvey.myQuestion.verify_quiz_score(3, 6)
        ex = ex1 and ex2 and ex3
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Select the checkbox Score this question for multiple choice",
                                 "Verifies that assigned scores are persist.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that assigned scores are persist."
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Multiple Choice Question Type",
                                 "Verifies that Multiple Choice question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Multiple Choice question added to live preview."
        mySurvey.myOptions.wait_until_accordion_quiz_update()

        mySurvey.myQuestion.click_on_question_to_edit(2)

        ex1 = mySurvey.myQuestion.verify_quiz_score(1, 5)
        ex2 = mySurvey.myQuestion.verify_quiz_score(2, 10)
        ex3 = mySurvey.myQuestion.verify_quiz_score(3, 15)
        ex = ex1 and ex2 and ex3
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Select the checkbox Score this question for drop down",
                                 "Verifies that assigned scores are persist.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that assigned scores are persist."
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Dropdown Question Type",
                                 "Verifies that Dropdown question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Dropdown question added to live preview."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.quiz
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C16616144
def test_quiz_off_in_accordion(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify if user unscores all quizzable question or removes \
         quiz setting from all quizzable question, should turn off in accordion")
    try:
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title("What is your favourite color?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Red")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Blue")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Green")
        mySurvey.myQuestion.question_quiz_toggle_on()
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(1, 10)
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(2, 20)
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(3, 30)

        ex1 = mySurvey.myQuestion.verify_quiz_score(1, 10)
        ex2 = mySurvey.myQuestion.verify_quiz_score(2, 20)
        ex3 = mySurvey.myQuestion.verify_quiz_score(3, 30)
        ex = ex1 and ex2 and ex3
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Select the checkbox Score this question for multiple \
                                  choice and assign values to the answer choices",
                                 "Verifies that scores are assigned to answer choices.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scores are assigned to answer choices."
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

        mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myBuilder.click_DropdownAddButton()
        mySurvey.myQuestion.enter_question_title("What is your favourite ice cream?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Vanilla")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Strawberry")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Butter scotch")
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(1, 5)
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(2, 10)
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(3, 15)

        ex1 = mySurvey.myQuestion.verify_quiz_score(1, 5)
        ex2 = mySurvey.myQuestion.verify_quiz_score(2, 10)
        ex3 = mySurvey.myQuestion.verify_quiz_score(3, 15)
        ex = ex1 and ex2 and ex3
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Select the checkbox Score this question for drop \
                                  down and assign values to the answer choices",
                                 "Verifies that scores are assigned to answer choices.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scores are assigned to answer choices."
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(2, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Dropdown Question Type",
                                 "Verifies that Dropdown question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Dropdown question added to live preview."

        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.question_quiz_toggle_off()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myQuestion.question_quiz_toggle_off()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myOptions.verify_quiz_toggle(False)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Quiz Mode is OFF",
                                 "Verifies that quiz mode is OFF",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify quiz mode is OFF."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.quiz
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C16594738
def test_quiz_sub_options(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify the Quiz sub options Display quiz results and Show correct answer \
         to incorrect responses are checked by default on turning ON Quiz from accordion")
    try:
        mySurvey.myOptions.unfold_OptionsRegion()
        mySurvey.myOptions.toggle_quiz_mode(display_quiz_result=False, show_collect_answers=False)
        ex = mySurvey.myOptions.check_quiz_selected_options()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Turn ON quiz from options in accordion",
                                 "Verifies that Display Quiz results \
                                 and Show correct answers to incorrect responses are selected.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Verifies that Display Quiz results \
                    and Show correct answers to incorrect responses are selected."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.quiz
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C16602659
def test_enable_quiz_sub_options_in_accordion(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify the Quiz sub options Display quiz results and Show correct answer to \
         incorrect responses are checked by default when Quiz is turned ON from accordion by entering "
        "scoring questions")
    try:
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title("What is your favourite color?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Red")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Blue")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Green")
        mySurvey.myQuestion.question_quiz_toggle_on()
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(1, 10)
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(2, 20)
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(3, 30)
        ex = mySurvey.myQuestion.verify_row_quiz_points()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Select the checkbox Score this question for multiple choice",
                                 "Verifies points drop down appears in front of all the answer choices.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that points drop down appears in front of all the answer choices."
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

        mySurvey.myOptions.unfold_OptionsRegion()
        ex = mySurvey.myOptions.verify_quiz_toggle(True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Quiz Mode is ON",
                                 "Verifies that quiz mode is ON",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify quiz mode is ON."

        ex = mySurvey.myOptions.check_quiz_selected_options()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Turn ON quiz from options in accordion",
                                 "Verifies that Display Quiz results \
                                 and Show correct answers to incorrect responses are selected.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Verifies that Display Quiz results \
                    and Show correct answers to incorrect responses are selected."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.quiz
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C16605024
def test_up_and_down_score_arrow(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify user can set score on funneled answer options by clicking on up and down arrow")
    try:
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title("What is your favourite color?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Red")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Blue")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Green")
        mySurvey.myQuestion.question_quiz_toggle_on()
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(1, 10)
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(2, 20)
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(3, 30)

        ex1 = mySurvey.myQuestion.verify_quiz_score(1, 10)
        ex2 = mySurvey.myQuestion.verify_quiz_score(2, 20)
        ex3 = mySurvey.myQuestion.verify_quiz_score(3, 30)
        ex = ex1 and ex2 and ex3
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Select the checkbox Score this question for multiple \
                                  choice and assign values to the answer choices",
                                 "Verifies that scores are assigned to answer choices.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scores are assigned to answer choices for multiple choice."
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

        mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myBuilder.click_DropdownAddButton()
        mySurvey.myQuestion.enter_question_title("What is your favourite ice cream?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Vanilla")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Strawberry")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Butter scotch")
        mySurvey.myQuestion.question_quiz_toggle_on()
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(1, 5)
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(2, 10)
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(3, 15)

        ex1 = mySurvey.myQuestion.verify_quiz_score(1, 5)
        ex2 = mySurvey.myQuestion.verify_quiz_score(2, 10)
        ex3 = mySurvey.myQuestion.verify_quiz_score(3, 15)
        ex = ex1 and ex2 and ex3
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Select the checkbox Score this question for drop \
                                  down and assign values to the answer choices",
                                 "Verifies that scores are assigned to answer choices.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scores are assigned to answer choices for drop down."

        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(2, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Dropdown Question Type",
                                 "Verifies that Dropdown question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Dropdown question added to live preview."

        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myLogic.toggleQuestionFunneling()
        ex1 = mySurvey.myQuestion.verify_added_funnel_rows(num_rows=3, q_num=2)
        ex2 = mySurvey.myQuestion.check_funnel_selected(selected=True)
        ex3 = mySurvey.myQuestion.check_funnel_unselected()
        ex = ex1 and ex2 and ex3
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Select the option User previous answer choices and Choose Q1",
                                 "Verifies Answer choices from Q1 appears in answer choices for Q2 and radio buttons.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Answer choices from Q1 appears in answer choices for Q2 and radio buttons."
        mySurvey.myQuestion.click_quiz_score_up_arrow(4)
        mySurvey.myQuestion.click_quiz_score_up_arrow(5)
        mySurvey.myQuestion.click_quiz_score_up_arrow(6)

        ex1 = mySurvey.myQuestion.verify_quiz_score(4, 1)
        ex2 = mySurvey.myQuestion.verify_quiz_score(5, 1)
        ex3 = mySurvey.myQuestion.verify_quiz_score(6, 1)
        ex = ex1 and ex2 and ex3
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Set scores for funneled answer choices using Up and Down arrows at the score field",
                                 "Verifies that the user is able to set scores using Up and down arrows.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that the user is able to set scores using Up and down arrows."
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(2, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Dropdown Question Type",
                                 "Verifies that Dropdown question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Dropdown question added to live preview."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.quiz
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C16711853
def test_quiz_in_category_drop_down(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify Quiz is present in the Category at Step 2 Survey Title")
    try:
        ex = mySurvey.myCreate.verify_category_drop_down('Quiz')
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Open the Category Drop down",
                                 "Verifies that Quiz as a category is present.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Quiz as a category is present."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
