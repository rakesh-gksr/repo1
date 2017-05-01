from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestVerifyQuizOptions/",  # report_relative_location
                               "test_verifyQuizOptions",  # report_file_name_prefix
                               # test_suite_title
                               ("Verify the option 'Show correct answers to incorrect responses' is active only "
                                "when the 'Display Quiz Results' is checked"),
                               ("Test to verify the option 'Show correct answers to incorrect responses' is "
                                "active only when the 'Display Quiz Results' is checked"),  # test_suite_description
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
@pytest.mark.C12809415
def test_verify_quiz_score_on_spage(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify the option 'Show correct answers to incorrect responses' is active only when the 'Display "
        "Quiz Results' is checked")
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
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "a")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "b")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "c")
        score_input = (2, 4, 6)
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
        mySurvey.myBuilder.click_DropdownAddButton()
        mySurvey.myQuestion.question_quiz_toggle_on()
        ex = mySurvey.myQuestion.verify_question_quiz_toggle(True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Scoring Checkbox",
                                 "Verifies that that scoring checkbox is present and checked in dropdown "
                                 "question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that scoring checkbox is present and checked in dropdown question type."
        mySurvey.myQuestion.enter_question_title("This wormhole leads to...")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "e")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "f")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Yuudachi")
        score_input = (5, 10, 15)
        for i in range(1, 4):
            mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(i, str(score_input[i-1]))
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
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Dropdown Question Type",
                                 "Verifies that Dropdown question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Dropdown question added to live preview."
        mySurvey.myOptions.unfold_OptionsRegion()
        ex = mySurvey.myOptions.check_quiz_selected_options(True, True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Quiz Results and Answers Checkboxes",
                                 "Verifies that quiz results and answers checkboxes are checked",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify quiz results and answers checkboxes are checked."
        ex = mySurvey.myOptions.toggle_on_quiz_display_correct_answer()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Quiz Answers Checkboxes",
                                 "Verifies that quiz answers checkboxes is turned on",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify quiz answers checkboxes is turned on."
        ex = mySurvey.myOptions.toggle_off_quiz_display_correct_answer()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Quiz Answers Checkboxes",
                                 "Verifies that quiz answers checkboxes is turned off",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify quiz answers checkboxes is turned off."
        import time
        time.sleep(20)

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
