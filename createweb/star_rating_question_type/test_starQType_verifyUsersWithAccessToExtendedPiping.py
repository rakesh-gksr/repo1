from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from smsdk.qafw.rpage import pyramidsurveypage as Spage
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestStarQTypeVerifyUsersWithAccessToExtendedPiping/",  # report_relative_location
                               "test_starQType_verifyUsersWithAccessToExtendedPiping",  # report_file_name_prefix
                               "Verify users with access to extended piping should be able to pipe in the respondent's "
                               "answer to a star question into question text, labels of a following question.",
                               # test_suite_title
                               ("Test to verify users with access to extended piping should be able to pipe in the "
                                "respondent's answer to a star question into question text, labels of a following "
                                "question.."),
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


@pytest.mark.star_question
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C812375
def test_starQType_verifyUsersWithAccessToExtendedPiping(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify users with access to extended piping should be able "
                                                           "to pipe in the respondent's answer to a star question into "
                                                           "question text, labels of a following question.")
    try:
        # code to add star question to survey
        mySurvey.myBuilder.click_star_rating_add_button()
        mySurvey.myQuestion.enter_question_title('Rate SurveyMonkey services')
        ex = mySurvey.myQuestion.toggle_star_rating_label_checkbox()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Turn on ratings labels",
                                 "checks that checkbox is checked to turn on ratings label"
                                 " option for star rating question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to turn rating labels option"
        sender_label_list = ["label1", "label2", "label3", "label4", "label5"]
        ex = mySurvey.myQuestion.enter_range_label_for_star_rating_question(sender_label_list)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Fill range labels",
                                 "Verify the range labels are filled correctly or not",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to fill range labels for star rating question"
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify Save Star question type",
                                 "verifies that Star question type saved",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Star question type saved"
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Star question Add to Live Preview",
                                 "Verifies that Star question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Star question added to live preview."

        mySurvey.myBuilder.click_NewPageAddButton()

        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        answerRows = ["row one", "row two"]
        mySurvey.myQuestion.enter_question_title("TEST")

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
        mySurvey.myQuestion.addPipingtoQuestionTitle("1.R1")
        # Code to add piping on question answer choice
        mySurvey.myQuestion.addPipingtoQuestionAnswer("1.R1", 1)
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
        attempt_star = Spage.attempt_star_rating_question(driver, 1, 4)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify attempting star rating question",
                                 "Verify attempting star rating question",
                                 attempt_star, True, not attempt_star, driver)
        assert attempt_star, "Failed to attempt star rating question"

        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        title_verify = Spage.verify_preview_question_title(driver, sender_label_list[3], 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify piping in multi choice question title",
                                 "Verify piping in multi choice question title",
                                 title_verify, False, not title_verify, driver)
        assert title_verify, "Failed to verify piping in multi choice question title"

        piped_mc_answer_rows = [sender_label_list[3], "row two"]
        option_assert = Spage.verify_question_answers_preview(driver, 1, piped_mc_answer_rows)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify piping in multi choice answer option",
                                 "Verify piping in multi choice answer option",
                                 option_assert,
                                 True,
                                 not option_assert,
                                 driver)
        assert option_assert, "Failed to verify piping in answer options"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
