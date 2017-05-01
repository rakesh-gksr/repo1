from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestVerifyQuizUpDownArrow/",  # report_relative_location
                               "test_verifyQuizUpDownArrow",  # report_file_name_prefix
                               # test_suite_title
                               ("Verify user is able to Score Multiple choice question and Drop down questions "
                                "by assigning values"),
                               ("Test to verify user is able to Score Multiple choice question and Drop down "
                                "questions by assigning values"),  # test_suite_description
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
@pytest.mark.C12809383
@pytest.mark.C12809384
def test_verify_quiz_up_down_arrow(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify user is able to Score Multiple choice question and Drop down questions by assigning values")
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
        for i in range(1, 4):
            mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(i, 5)
            ex = mySurvey.myQuestion.increase_quiz_points(i, 6)
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Up Arrow for Increasing Answer Choices"
                                                                   " Points",
                                     "Verifies that clicking on up arrow increased the points for answer "
                                     "choice - " + str(i),
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify that clicking on up arrow increased the points for answer choice - " + str(i)

        for i in range(1, 4):

            ex = mySurvey.myQuestion.decrease_quiz_points(i, 5)
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Down Arrow for Decreasing Answer Choices"
                                                                   " Points",
                                     "Verifies that clicking on down arrow decreased the points for answer "
                                     "choice - " + str(i),
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify that clicking on down arrow increased the points for answer choice - " + str(i)

        mySurvey.myQuestion.turn_on_multichoice_otheroption()
        ex = mySurvey.myQuestion.check_quiz_input_field_in_question_other_field()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Quiz Dropdown in Other Field",
                                 "Verifies that Other field does not display the Quiz Dropdown field"
                                 "choice - " + str(i),
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Other field does not display the Quiz Dropdown field"

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
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "g")
        for i in range(1, 4):
            mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(i, 5)
            ex = mySurvey.myQuestion.increase_quiz_points(i, 6)
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Up Arrow for Increasing Answer Choices"
                                                                   " Points",
                                     "Verifies that clicking on up arrow increased the points for answer "
                                     "choice - " + str(i),
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify that clicking on up arrow increased the points for answer choice - " + str(i)

        for i in range(1, 4):
            ex = mySurvey.myQuestion.decrease_quiz_points(i, 5)
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Down Arrow for Decreasing Answer Choices"
                                                                   " Points",
                                     "Verifies that clicking on down arrow decreased the points for answer "
                                     "choice - " + str(i),
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify that clicking on down arrow increased the points for answer choice - " + str(i)

        mySurvey.myQuestion.turn_on_multichoice_otheroption()
        ex = mySurvey.myQuestion.check_quiz_input_field_in_question_other_field()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Quiz Dropdown in Other Field",
                                 "Verifies that Other field does not display the Quiz Dropdown field"
                                 "choice - " + str(i),
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Other field does not display the Quiz Dropdown field"

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
        mySurvey.myQuestion.turn_on_multiple_answers()
        mySurvey.myQuestion.question_quiz_toggle_on()
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
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "a")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "b")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "c")
        for i in range(1, 4):
            mySurvey.myQuestion.enter_multiple_choice_answer_row_quiz_points(i, 5)
            ex = mySurvey.myQuestion.increase_quiz_points(i, 6)
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Up Arrow for Increasing Answer Choices"
                                                                   " Points",
                                     "Verifies that clicking on up arrow increased the points for answer "
                                     "choice - " + str(i),
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify that clicking on up arrow increased the points for answer choice - " + str(i)

        for i in range(1, 4):
            ex = mySurvey.myQuestion.decrease_quiz_points(i, 5)
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Down Arrow for Decreasing Answer Choices"
                                                                   " Points",
                                     "Verifies that clicking on down arrow decreased the points for answer "
                                     "choice - " + str(i),
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify that clicking on down arrow increased the points for answer choice - " + str(i)

        mySurvey.myQuestion.turn_on_multichoice_otheroption()
        ex = mySurvey.myQuestion.check_quiz_input_field_in_question_other_field()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Quiz Dropdown in Other Field",
                                 "Verifies that Other field does not display the Quiz Dropdown field"
                                 "choice - " + str(i),
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Other field does not display the Quiz Dropdown field"

        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Multiple Choice Multi Select Question Type",
                                 "Verifies that Multiple Choice  Multi Select question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Multiple Choice  Multi Select question added to live preview."

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
