from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "test_verifyQuizzableQuestions/",  # report_relative_location
                               "test_verifyQuizzableQuestions",  # report_file_name_prefix
                               # test_suite_title
                               ("Verify Quiz is turned on and scoring is enabled for all the quizzable questions "
                                "that are added"),
                               ("Test to Verify Quiz is turned on and scoring is enabled for all the quizzable "
                                "questions that are added"),  # test_suite_description
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
@pytest.mark.C37908159
def test_verify_quizzable_questions(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify Quiz is turned on and scoring is enabled for all the quizzable questions that are added")
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
        ex = mySurvey.myOptions.check_quiz_selected_options(display_quiz_result=True, show_collect_answers=True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Quiz Results and Answers Checkboxes",
                                 "Verifies that quiz results and answers checkboxes are checked",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify quiz results and answers checkboxes are checked."

        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        ex = mySurvey.myQuestion.verify_score_this_question_checkbox(choice_count=3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Score Checkbox and Score Input field",
                                 "Verifies that Score Checkbox and Score Input field present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that score checkbox and score input field present"

        mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "a")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "b")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "c")
        score_input = (2, 4, 6)
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
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Multiple Choice Question Type",
                                 "Verifies that Multiple Choice question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Multiple Choice question added to live preview."

        mySurvey.myBuilder.click_DropdownAddButton()
        ex = mySurvey.myQuestion.verify_score_this_question_checkbox(choice_count=3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Score Checkbox and Score Input field",
                                 "Verifies that Score Checkbox and Score Input field present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that score checkbox and score input field present"

        mySurvey.myQuestion.enter_question_title("This wormhole leads to...")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "e")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "f")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Yuudachi")
        score_input = (5, 10, 15)
        for i in range(1, 4):
            mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(i, str(score_input[i - 1]))
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
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Dropdown Question Type",
                                 "Verifies that Dropdown question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Dropdown question added to live preview."

        mySurvey.myBuilder.click_star_rating_add_button()
        ex = mySurvey.myQuestion.verify_score_this_question_checkbox(is_present=False)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Score Checkbox is not Present",
                                 "Verifies that score checkbox is not present in Star Rating question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that score checkbox is not present in Star Rating question type"

        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add star question type to survey ",
                                 "Verified that star question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add star question to survey."

        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify star question Add to Live Preview",
                                 "Verifies that star question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star question added to live preview."

        mySurvey.myBuilder.click_SliderAddButton()
        ex = mySurvey.myQuestion.verify_score_this_question_checkbox(is_present=False)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Score Checkbox is not Present",
                                 "Verifies that score checkbox is not present in Slider question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that score checkbox is not present in Slider question type"
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Slider question type to survey ",
                                 "Verified that slider question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add slider question to survey."
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 4)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider question Add to Live Preview",
                                 "Verifies that Slider question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Slider question added to live preview."

        mySurvey.myBuilder.click_SingleTextboxAddButton()
        ex = mySurvey.myQuestion.verify_score_this_question_checkbox(is_present=False)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Score Checkbox is not Present",
                                 "Verifies that score checkbox is not present in Single Textbox question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that score checkbox is not present in Single Textbox question type"
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 5)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Single Textbox question Add to Live Preview",
                                 "Verifies that Single Textbox question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Single Textbox question added to live preview."

        mySurvey.myBuilder.click_CommentBoxAddButton()
        ex = mySurvey.myQuestion.verify_score_this_question_checkbox(is_present=False)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Score Checkbox is not Present",
                                 "Verifies that score checkbox is not present in Comment question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that score checkbox is not present in Comment question type"
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 6)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Comment question Add to Live Preview",
                                 "Verifies that Comment question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Comment question added to live preview."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
