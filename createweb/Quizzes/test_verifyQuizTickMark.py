from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestVerifyQuizTickMark/",  # report_relative_location
                               "test_verifyQuizTickMark",  # report_file_name_prefix
                               # test_suite_title
                               "Verify the ticks appear/disappear in place of radio buttons when scoring is "
                               "enabled/disabled",
                               "Test to verify the ticks appear/disappear in place of radio buttons when scoring is "
                               "enabled/disabled",
                               # test_suite_description
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
@pytest.mark.C12809396
def test_verify_answer_choice_tick_mark_appears(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify the ticks appear in place of radio buttons when scoring is enabled")
    try:
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.question_quiz_toggle_on()
        ex = mySurvey.myQuestion.verify_question_quiz_toggle(True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Scoring Checkbox",
                                 "Verifies that scoring checkbox is present and checked in multiple "
                                 "choice question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scoring checkbox is present and checked in multiple choice question type."
        ex = mySurvey.myQuestion.verify_answer_choices_display_type("quiz-radio", 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Tick Marks",
                                 "Verifies that all the answer choices showing are tick marks",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that all the answer choices showing are tick marks."
        ex = mySurvey.myQuestion.verify_answer_choices_display_type("radio", 3)
        ex = True if not ex else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Radio Buttons",
                                 "Verifies that all the answer choices not not showing radio buttons",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that all the answer choices not not showing radio buttons."

        mySurvey.myQuestion.click_question_cancel_from_edit_tab()
        mySurvey.myBuilder.click_DropdownAddButton()
        mySurvey.myQuestion.question_quiz_toggle_on()
        ex = mySurvey.myQuestion.verify_question_quiz_toggle(True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Scoring Checkbox",
                                 "Verifies that scoring checkbox is present and checked in dropdown "
                                 "question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scoring checkbox is present and checked in dropdown question type."
        ex = mySurvey.myQuestion.verify_answer_choices_display_type("quiz-radio", 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Tick Marks",
                                 "Verifies that all the answer choices are showing tick marks",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that all the answer choices are showing tick marks."

        mySurvey.myQuestion.click_question_cancel_from_edit_tab()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.turn_on_multiple_answers()
        mySurvey.myQuestion.question_quiz_toggle_on()
        ex = mySurvey.myQuestion.verify_question_quiz_toggle(True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Scoring Checkbox",
                                 "Verifies that scoring checkbox is present and checked in multiple "
                                 "choice multi select question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scoring checkbox is present and checked in multiple choice multi select " \
                   "question type."
        ex = mySurvey.myQuestion.verify_answer_choices_display_type("quiz-radio", 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Tick Marks",
                                 "Verifies that all the answer choices are showing tick marks",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that all the answer choices are showing tick marks."
        ex = mySurvey.myQuestion.verify_answer_choices_display_type("checkbox", 3)
        ex = True if not ex else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Checkboxes",
                                 "Verifies that all the answer choices are not showing checkboxes",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that all the answer choices are not showing checkboxes."
        mySurvey.myQuestion.click_question_cancel_from_edit_tab()

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
@pytest.mark.C12809397
def test_verify_answer_choice_tick_mark_disappears(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify the 'Ticks' disappear and radio buttons appears when the scoring is disabled")
    try:
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.question_quiz_toggle_off()
        ex = mySurvey.myQuestion.verify_question_quiz_toggle(False)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Scoring Checkbox",
                                 "Verifies that scoring checkbox is unchecked in multiple "
                                 "choice question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scoring checkbox is unchecked in multiple choice question type."
        ex = mySurvey.myQuestion.verify_answer_choices_display_type("quiz-radio", 3)
        ex = True if not ex else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Tick Mark",
                                 "Verifies that tick marks for all the answer choices are not showing",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that tick marks for all the answer choices are not showing."
        ex = mySurvey.myQuestion.verify_answer_choices_display_type("radio", 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Radio Button",
                                 "Verifies that radio buttons for all the answer choices are showing",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that radio buttons for all the answer choices are showing."

        mySurvey.myQuestion.click_question_cancel_from_edit_tab()
        mySurvey.myBuilder.click_DropdownAddButton()
        mySurvey.myQuestion.question_quiz_toggle_off()
        ex = mySurvey.myQuestion.verify_question_quiz_toggle(False)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Scoring Checkbox",
                                 "Verifies that scoring checkbox is unchecked in dropdown question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scoring checkbox is unchecked in dropdown question type."
        ex = mySurvey.myQuestion.verify_answer_choices_display_type("quiz-radio", 3)
        ex = True if not ex else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Tick Mark",
                                 "Verifies that tick marks for all the answer choices are not showing",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that tick marks for all the answer choices are not showing."

        mySurvey.myQuestion.click_question_cancel_from_edit_tab()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.turn_on_multiple_answers()
        mySurvey.myQuestion.question_quiz_toggle_off()
        ex = mySurvey.myQuestion.verify_question_quiz_toggle(False)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Scoring Checkbox",
                                 "Verifies that scoring checkbox is unchecked in multiple "
                                 "choice multi select question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scoring checkbox is unchecked in multiple choice multi select question type."
        ex = mySurvey.myQuestion.verify_answer_choices_display_type("quiz-radio", 3)
        ex = True if not ex else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Tick Mark",
                                 "Verifies that tick marks for all the answer choices are not showing",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that tick marks for all the answer choices are not showing."
        ex = mySurvey.myQuestion.verify_answer_choices_display_type("checkbox", 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Checkbox Input",
                                 "Verifies that checkboxes input for all the answer choices are showing",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that checkboxes input for all the answer choices are showing."
        mySurvey.myQuestion.click_question_cancel_from_edit_tab()

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
@pytest.mark.C12809398
def test_verify_active_tick_mark(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify the \"Ticks\" turn teal when score is assigned for an answer choice")
    try:
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.question_quiz_toggle_on()
        ex = mySurvey.myQuestion.verify_question_quiz_toggle(True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Scoring Checkbox",
                                 "Verifies that scoring checkbox is present and checked in multiple "
                                 "choice question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scoring checkbox is present and checked in multiple choice question type."
        ex = mySurvey.myQuestion.verify_answer_choices_display_type("quiz-radio", 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Tick Marks",
                                 "Verifies that all the answer choices showing are tick marks",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that all the answer choices showing are tick marks."
        for i in range(1, 4):
            mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(i, 5)
        ex = mySurvey.myQuestion.verify_active_tick_mark(3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Tick Marks Color",
                                 "Verifies that the 'tick' for the answer choice changes to teal on "
                                 "assigning some value",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that the 'tick' for the answer choice changes to teal on assigning some value."
        mySurvey.myQuestion.click_question_cancel_from_edit_tab()
        mySurvey.myBuilder.click_DropdownAddButton()
        mySurvey.myQuestion.question_quiz_toggle_on()
        ex = mySurvey.myQuestion.verify_question_quiz_toggle(True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Scoring Checkbox",
                                 "Verifies that scoring checkbox is present and checked in dropdown "
                                 "question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scoring checkbox is present and checked in dropdown question type."
        ex = mySurvey.myQuestion.verify_answer_choices_display_type("quiz-radio", 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Tick Marks",
                                 "Verifies that all the answer choices are showing tick marks",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that all the answer choices are showing tick marks."
        for i in range(1, 4):
            mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(i, 5)
        ex = mySurvey.myQuestion.verify_active_tick_mark(3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Tick Marks Color",
                                 "Verifies that the 'tick' for the answer choice changes to teal on "
                                 "assigning some value",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that the 'tick' for the answer choice changes to teal on assigning some value."

        mySurvey.myQuestion.click_question_cancel_from_edit_tab()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.turn_on_multiple_answers()
        mySurvey.myQuestion.question_quiz_toggle_on()
        ex = mySurvey.myQuestion.verify_question_quiz_toggle(True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Scoring Checkbox",
                                 "Verifies that scoring checkbox is present and checked in multiple "
                                 "choice multi select question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scoring checkbox is present and checked in multiple choice multi select " \
                   "question type."
        ex = mySurvey.myQuestion.verify_answer_choices_display_type("quiz-radio", 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Tick Marks",
                                 "Verifies that all the answer choices are showing tick marks",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that all the answer choices are showing tick marks."
        for i in range(1, 4):
            mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(i, 5)
        ex = mySurvey.myQuestion.verify_active_tick_mark(3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Tick Marks Color",
                                 "Verifies that the 'tick' for the answer choice changes to teal on "
                                 "assigning some value",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that the 'tick' for the answer choice changes to teal on assigning some value."
        mySurvey.myQuestion.click_question_cancel_from_edit_tab()

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
@pytest.mark.C12809399
def test_verify_inactive_tick_mark(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify the color of 'Ticks' turns back to white when the score for that answer choice gets 0")
    try:
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.question_quiz_toggle_on()
        ex = mySurvey.myQuestion.verify_question_quiz_toggle(True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Scoring Checkbox",
                                 "Verifies that scoring checkbox is present and checked in multiple "
                                 "choice question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scoring checkbox is present and checked in multiple choice question type."
        ex = mySurvey.myQuestion.verify_answer_choices_display_type("quiz-radio", 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Tick Marks",
                                 "Verifies that all the answer choices showing are tick marks",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that all the answer choices showing are tick marks."
        for i in range(1, 4):
            mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(i, 0)
        ex = mySurvey.myQuestion.verify_deactive_tick_mark(3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Tick Marks Color",
                                 "Verifies that the 'tick' for the answer choice changes to white on "
                                 "assigning zero value",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that the 'tick' for the answer choice changes to white on assigning zero value."
        mySurvey.myQuestion.click_question_cancel_from_edit_tab()
        mySurvey.myBuilder.click_DropdownAddButton()
        mySurvey.myQuestion.question_quiz_toggle_on()
        ex = mySurvey.myQuestion.verify_question_quiz_toggle(True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Scoring Checkbox",
                                 "Verifies that scoring checkbox is present and checked in dropdown "
                                 "question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scoring checkbox is present and checked in dropdown question type."
        ex = mySurvey.myQuestion.verify_answer_choices_display_type("quiz-radio", 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Tick Marks",
                                 "Verifies that all the answer choices are showing tick marks",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that all the answer choices are showing tick marks."
        for i in range(1, 4):
            mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(i, 0)
        ex = mySurvey.myQuestion.verify_deactive_tick_mark(3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Tick Marks Color",
                                 "Verifies that the 'tick' for the answer choice changes to white on "
                                 "assigning zero value",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that the 'tick' for the answer choice changes to white on assigning zero value."

        mySurvey.myQuestion.click_question_cancel_from_edit_tab()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.turn_on_multiple_answers()
        mySurvey.myQuestion.question_quiz_toggle_on()
        ex = mySurvey.myQuestion.verify_question_quiz_toggle(True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Scoring Checkbox",
                                 "Verifies that scoring checkbox is present and checked in multiple "
                                 "choice multi select question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scoring checkbox is present and checked in multiple choice multi select " \
                   "question type."
        ex = mySurvey.myQuestion.verify_answer_choices_display_type("quiz-radio", 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Tick Marks",
                                 "Verifies that all the answer choices are showing tick marks",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that all the answer choices are showing tick marks."
        for i in range(1, 4):
            mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(i, 0)
        ex = mySurvey.myQuestion.verify_deactive_tick_mark(3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Tick Marks Color",
                                 "Verifies that the 'tick' for the answer choice changes to white on "
                                 "assigning zero value",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that the 'tick' for the answer choice changes to white on assigning zero value."
        mySurvey.myQuestion.click_question_cancel_from_edit_tab()

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
@pytest.mark.C12809400
def test_verify_score_after_tick_mark_on_and_tick_mark_off(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify the socring value gets 0 when a scored answer choice Tick is clicked and the value should "
        "persist on clicking back the same answer choice")
    try:
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.question_quiz_toggle_on()
        ex = mySurvey.myQuestion.verify_question_quiz_toggle(True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Scoring Checkbox",
                                 "Verifies that scoring checkbox is present and checked in multiple "
                                 "choice question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scoring checkbox is present and checked in multiple choice question type."
        ex = mySurvey.myQuestion.verify_answer_choices_display_type("quiz-radio", 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Tick Marks",
                                 "Verifies that all the answer choices showing are tick marks",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that all the answer choices showing are tick marks."

        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(1, 5)
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(2, 10)
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(3, 15)

        ex = mySurvey.myQuestion.tick_mark_toggle_off(2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Deselect Tick Mark",
                                 "Verifies that tick mark button is deselected",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that tick mark button is deselected."

        ex = mySurvey.myQuestion.verify_quiz_score(2, 0)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check Dropdown Score Value of deselected tick "
                                                               "mark field",
                                 "Verifies that dropdown value became zero once tick mark got deslected",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that dropdown value became zero once deselect tick mark."
        ex = mySurvey.myQuestion.tick_mark_toggle_on(2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Select Tick Mark",
                                 "Verifies that tick mark button is selected",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that dropdown value became 1 once tick mark got deslected."

        ex = mySurvey.myQuestion.verify_quiz_score(2, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check Dropdown Score Value of selected tick "
                                                               "mark field",
                                 "Verifies that dropdown value became 1 once tick mark got re selected",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that dropdown value became 1 once tick mark got re selected."

        mySurvey.myQuestion.click_question_cancel_from_edit_tab()
        mySurvey.myBuilder.click_DropdownAddButton()
        mySurvey.myQuestion.question_quiz_toggle_on()
        ex = mySurvey.myQuestion.verify_question_quiz_toggle(True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Scoring Checkbox",
                                 "Verifies that scoring checkbox is present and checked in dropdown "
                                 "question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scoring checkbox is present and checked in dropdown question type."
        ex = mySurvey.myQuestion.verify_answer_choices_display_type("quiz-radio", 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Tick Marks",
                                 "Verifies that all the answer choices are showing tick marks",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that all the answer choices are showing tick marks."
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(1, 5)
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(2, 10)
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(3, 15)

        ex = mySurvey.myQuestion.tick_mark_toggle_off(2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Deselect Tick Mark",
                                 "Verifies that tick mark button is deselected",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that tick mark button is deselected."

        ex = mySurvey.myQuestion.verify_quiz_score(2, 0)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check Dropdown Score Value of deselected tick "
                                                               "mark field",
                                 "Verifies that dropdown value became zero once tick mark got deslected",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that dropdown value became zero once deselect tick mark."
        ex = mySurvey.myQuestion.tick_mark_toggle_on(2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Select Tick Mark",
                                 "Verifies that tick mark button is selected",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that dropdown value became 1 once tick mark got deslected."

        ex = mySurvey.myQuestion.verify_quiz_score(2, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check Dropdown Score Value of selected tick "
                                                               "mark field",
                                 "Verifies that dropdown value became 1 once tick mark got re selected",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that dropdown value became 1 once tick mark got re selected."

        mySurvey.myQuestion.click_question_cancel_from_edit_tab()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.turn_on_multiple_answers()
        mySurvey.myQuestion.question_quiz_toggle_on()
        ex = mySurvey.myQuestion.verify_question_quiz_toggle(True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Scoring Checkbox",
                                 "Verifies that scoring checkbox is present and checked in multiple "
                                 "choice multi select question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scoring checkbox is present and checked in multiple choice multi select " \
                   "question type."
        ex = mySurvey.myQuestion.verify_answer_choices_display_type("quiz-radio", 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Tick Marks",
                                 "Verifies that all the answer choices are showing tick marks",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that all the answer choices are showing tick marks."
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(1, 5)
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(2, 10)
        mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(3, 15)

        ex = mySurvey.myQuestion.tick_mark_toggle_off(2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Deselect Tick Mark",
                                 "Verifies that tick mark button is deselected",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that tick mark button is deselected."

        ex = mySurvey.myQuestion.verify_quiz_score(2, 0)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check Dropdown Score Value of deselected tick "
                                                               "mark field",
                                 "Verifies that dropdown value became zero once tick mark got deslected",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that dropdown value became zero once deselect tick mark."
        ex = mySurvey.myQuestion.tick_mark_toggle_on(2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Select Tick Mark",
                                 "Verifies that tick mark button is selected",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that dropdown value became 1 once tick mark got deslected."

        ex = mySurvey.myQuestion.verify_quiz_score(2, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check Dropdown Score Value of selected tick "
                                                               "mark field",
                                 "Verifies that dropdown value became 1 once tick mark got re selected",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that dropdown value became 1 once tick mark got re selected."

        mySurvey.myQuestion.click_question_cancel_from_edit_tab()

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
