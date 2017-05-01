from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from smsdk.qafw.survey_util.survey_collectors import create_collector, get_collector_options, update_collector_options
import traceback
import pytest
from smsdk.qafw.rpage import pyramidsurveypage as Spage
from smsdk.qafw.create.svysvc_api_wrapper import get_question_responses


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestVerifyCustomEndPage/",  # report_relative_location
                               "test_verifyCustomEndPage",  # report_file_name_prefix
                               # test_suite_title
                               ("Verify that the Custom End page is displayed at the End of the Quiz results page "
                                "if the Custom End Page setting is enabled from Collector settings"),
                               ("Test to verify that the Custom End page is displayed at the End of the Quiz "
                                "results page if the Custom End Page setting is enabled from Collector settings"),
                               # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    env_init("platinum_advanced_branching")
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
@pytest.mark.C12809438
def test_verify_custom_end_page(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    survey_id = mySurvey.survey_id
    user_id = mySurvey.user_id

    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify that the Custom End page is displayed at the End of the Quiz results page if the Custom End Page "
        "setting is enabled from Collector settings")
    try:
        survey_json = mySurvey.mySvc_holder.svysvc.get_survey(survey_id, user_id)
        survey_title = survey_json["title"]["text"]
        mySurvey.myDesign.click_addPageTitle("Page 1", "This is test page 1")
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

        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_NewPageAddButton()

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
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "a")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "b")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "c")
        mySurvey.myQuestion.enter_multipleChoice_answerText(4, "d")
        mySurvey.myQuestion.enter_multipleChoice_answerText(5, "e")
        score_input = (2, 4, 6, 8, 10)
        for i in range(1, 6):
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
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(2, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Dropdown Question Type",
                                 "Verifies that Dropdown question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Dropdown question added to live preview."

        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()

        ex = mySurvey.myLogic.addNewBranchingRule([
            ("MultipleChoice", [1, 1], "response", [None], "finish", "default", None)])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Advanced Logic",
                                 "Verifies advanced logic window closed and logic saved.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to save advanced logic"

        driver, new_collector_id = create_collector(driver, user_id, survey_id, "weblink")
        new_collector_data = get_collector_options(new_collector_id, user_id)
        new_collector_url = new_collector_data["weblink"]["url"]

        updated_options = update_collector_options(
            new_collector_id, user_id, {"survey_completion_page": {
                "redirect_type": "weblink", "url": "https://www.google.co.in"}})

        result_updated_options = updated_options is not False
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Updating collector setting options for Survey end page to custom page",
                                 "Updating collector setting options for Survey end page to custom page using API",
                                 result_updated_options,
                                 False,
                                 not result_updated_options,
                                 driver)
        assert result_updated_options, "Failed to update Survey end page to custom page option using api"
        survey_list = [
            {
                "collector_id": new_collector_id,
                "url": new_collector_url,
                "survey_end_page": "custom",
                "end_url": "https://www.google.co.in"
            },

        ]

        answer_input_by_position = {
            1: {
                1: {'choices_list': [1]}
            }
        }

        for collector_data in survey_list:

            expected_answers_dict, expected_response_dict = get_question_responses(
                collector_data["url"], answer_input_by_position, collector_data["collector_id"])
            url = collector_data["url"]
            opened, total_load_time = Spage.open_survey(
                driver, url, survey_title)

            report.add_report_record(ReportMessageTypes.TEST_STEP,
                                     "Collector URL - Go to Survey: " + url + " to verify end page as " +
                                     collector_data["survey_end_page"],
                                     "Driver goes to the survey and it took " + str(total_load_time) +
                                     " to open page.",
                                     opened, False, not opened, driver)
            assert opened, "cannot open survey"

            take = Spage.take_survey(driver, expected_answers_dict[1])
            report.add_report_record(ReportMessageTypes.TEST_STEP,
                                     "Attempting first page question",
                                     "Attempting first page question",
                                     take, True, not take, driver)
            assert take, "cannot take survey"

        ex = mySurvey.myDesign.click_preview_next_button_noFrame()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Successfully Moved to the next page ",
                                 "Sucessfully Moved to the next page.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to move to next preview page"

        print "collector data", collector_data["survey_end_page"]
        # Verify that the Custom End page is shown on clicking Done at the Quiz results page
        check_end_url = collector_data["end_url"] in driver.current_url
        results_displayed = True if driver.title == "Google" and check_end_url else False
        report.add_report_record(
            ReportMessageTypes.TEST_STEP,
            "Verify custom survey end page is displayed",
            "Driver verifies redirect to survey results page: " +
            driver.current_url,
            results_displayed,
            False,
            not results_displayed,
            driver)
        assert results_displayed, "Instant Results url Failed"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
