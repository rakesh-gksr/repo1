from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSliderQTypeVerifyUsersWithAccessToExtendedPiping/",  # report_relative_location
                               "test_sliderQType_verifyUsersWithAccessToExtendedPiping",  # report_file_name_prefix
                               "Verify users with access to extended piping should be able to pipe in the respondent's "
                               "answer to a slider question into question text of a following question.",
                               # test_suite_title
                               ("Test to verify users with access to extended piping should be able to pipe in the "
                                "respondent's answer to a slider question into question text of a following question."),
                               # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    # for user under group platinum_advanced_branching has enabled extended piping feature
    env_init("platinum_advanced_branching")
    import datetime
    import os

    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime(
        "%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()

    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.slider_question
@pytest.mark.IB
@pytest.mark.C284519
def test_sliderQType_verifyUsersWithAccessToExtendedPiping(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify users with access to extended piping should be able "
                                                           "to pipe in the respondent's answer to a slider question "
                                                           "into question text of a following question.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        # code to add slider question to survey
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title('Rate SurveyMonkey services')
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify Save Slider question type",
                                 "verifies that Slider question type saved",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Slider question type saved"
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider question Add to Live Preview",
                                 "Verifies that Slider question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Slider question added to live preview."

        mySurvey.myBuilder.click_NewPageAddButton()

        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        answerRows = []
        mySurvey.myQuestion.enter_question_title("TEST")
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[0])
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[1])

        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify Save Multiple Choice question type",
                                 "verifies that Multiple Choice question type saved",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Multiple Choice question type saved"
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Multiple Choice question Add to Live Preview",
                                 "Verifies that Multiple Choice question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Multiple Choice question added to live preview."
        # Code to edit multiple choice question to add piping
        mySurvey.myQuestion.click_on_question_to_edit(2)
        # Code to add piping on question title
        mySurvey.myQuestion.addPipingtoQuestionTitle(1)
        # Code to add piping on question answer choice
        mySurvey.myQuestion.addPipingtoQuestionAnswer(1,1)
        # Code to save the question
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify Save Multiple Choice question type",
                                 "verifies that Multiple Choice question type saved",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Multiple Choice question type saved"
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Multiple Choice question Add to Live Preview",
                                 "Verifies that Multiple Choice question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Multiple Choice question added to live preview."

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
        mySurvey.myLogic.enter_textType_preview_answer(1, 20)
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.verify_preview_question_title("20", 1)

        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title Piped from Q1",
                                 "Verify question title is the same that we entered in Q1.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question title piping"
        # Code to verify preview question answer
        ex = mySurvey.myDesign.verify_preview_question_answer("20", 1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Answer Row Piped from Q1",
                                 "Verify answer row title is the same that we entered in Q1.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer row piping"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()