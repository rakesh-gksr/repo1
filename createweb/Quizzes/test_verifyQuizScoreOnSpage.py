from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from smsdk.qafw.rpage import quiz_result_page as QR_Page
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestVerifyQuizScoreOnSpage/",  # report_relative_location
                               "test_verifyQuizScoreOnSpage",  # report_file_name_prefix
                               # test_suite_title
                               ("Verify the 'Display Quiz Results' checkbox is present in the accordion in "
                                "Options and selecting it displayed Quiz results page at the end of the survey"),
                               ("Test to verify the 'Display Quiz Results' checkbox is present in the accordion "
                                "in Options and selecting it displayed Quiz results page at the end of the survey"),
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
@pytest.mark.C12809415
def test_verify_quiz_score_on_spage(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify the 'Display Quiz Results' checkbox is present in the accordion in Options and selecting it "
        "displayed Quiz results page at the end of the survey")
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
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks preview button, in order to verify theme in preview window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        mySurvey.myDesign.click_off_preview_warning()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.switch_to_preview_iframe()
        mySurvey.myLogic.process_multichoice_preview(1, 2)
        mySurvey.myDesign.enter_dropdown_preview(2, "Yuudachi")

        ex = mySurvey.myDesign.click_preview_done_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Submit Survey",
                                 "Verified that survey submitted successfully",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify survey submitted successfully."
        ex = QR_Page.verify_question_score(driver, 1, 4, 6)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify 1st question score",
                                 "Verify 1st question score",
                                 ex, True, not ex, driver)
        assert ex, "Failed to verify 1st question score"
        ex = QR_Page.verify_question_score(driver, 2, 15, 15)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify 2nd question score",
                                 "Verify 2nd question score",
                                 ex, True, not ex, driver)
        assert ex, "Failed to verify 2nd question score"

        ex = QR_Page.verify_quiz_percentage_score(driver, 90)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify quiz percentage on result page",
                                 "Verify quiz percentage on result page",
                                 ex, True, not ex, driver)
        assert ex, "Failed to verify quiz percentage on result page"

        ex = QR_Page.verify_quiz_total_points(driver, 19, 21)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify quiz points on result page",
                                 "Verify quiz points on result page",
                                 ex, True, not ex, driver)
        assert ex, "Failed to verify quiz points on result page"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
