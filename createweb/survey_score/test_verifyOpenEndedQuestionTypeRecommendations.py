# This Python file uses the following encoding: utf-8
from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from dynamic_tests.dynamic_tests_config import recommendation_slides_data
from smsdk.qafw.rpage import pyramidsurveypage as Spage
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestVerifyOpenEndedQuestionTypeRecommendations",  # report_relative_location
                               "test_verifyOpenEndedQuestionTypeRecommendations",  # report_file_name_prefix
                               "Verify Questions type Recommendations in Survey Score modal",
                               # test_suite_title
                               "Test to verify Questions type Recommendations in Survey Score modal",
                               # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, "
                                                                                                      "%Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.survey_score
@pytest.mark.IB
@pytest.mark.parametrize("test_info", recommendation_slides_data,
                         ids=[dict["test_rail_id"] for dict in recommendation_slides_data])
def test_verify_question_type_recommendations(create_survey, test_info):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, test_info['test_case_title'])
    try:

        if test_info['q_type'] == 'comment_box':
            mySurvey.myBuilder.click_CommentBoxAddButton()

        elif test_info['q_type'] == 'single_text_box':
            mySurvey.myBuilder.click_SingleTextboxAddButton()
        else:
            mySurvey.myBuilder.click_MultipleTextboxesAddButton()
            answerRows = []
            answerRows.append(mySurvey.myLogic.RNG(10))
            answerRows.append(mySurvey.myLogic.RNG(10))
            answerRows.append(mySurvey.myLogic.RNG(10))
            mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[0])
            mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[1])
            mySurvey.myQuestion.enter_multipleChoice_answerText(3, answerRows[2])

        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question Add to Live Preview",
                                 "Verifies that " + test_info['q_type'] + " question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify " + test_info['q_type'] + " question added to live preview."

        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        answerRows = []
        mySurvey.myQuestion.enter_question_title("Rate SurveyMonkey services")
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[0])
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[1])
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Multiple Choice question Add to Live Preview",
                                 "Verifies that Multiple Choice question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Multiple Choice question added to live preview."

        ex = mySurvey.myCreate.click_survey_score()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check Rate My Survey CTA",
                                 "verifies Rate My Survey CTA present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that create Rate My Survey present"

        ex = mySurvey.myCreate.verify_survey_score_modal()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Rate My Survey Modal",
                                 "verifies Rate My Survey modal box appears on screen",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Rate My Survey modal box appears on screen"

        ex = mySurvey.myCreate.verify_recommendation(recommendation_title=test_info["recommendation_title"],
                                                     recommendation_text=test_info["recommendation_text"],
                                                     recommendation_q_nums=test_info["recommendation_q_nums"],
                                                     is_single_recommendation=True)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify Recommendation for open ended question type : " + test_info['q_type'],
                                 "Verifies recommendation message for open ended question type:  " +
                                 test_info['q_type'],
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify recommendation message for open ended question type:  " + test_info['q_type']
        mySurvey.myCreate.click_tip_section_cta("Comment")
        # ex = mySurvey.myDesign.click_preview_button()
        # report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
        #                          "Clicks and opens preview window.",
        #                          ex,
        #                          True,
        #                          not ex,
        #                          driver)
        # assert ex, "Failed to click Preview Button"
        mySurvey.myDesign.switch_to_preview_window()
        mySurvey.myDesign.click_to_hide_preview_warning()
        mySurvey.myDesign.switch_to_preview_iframe()

        # verify comment icon in question
        ex = Spage.verify_question_comment_count(driver, 1, 0)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "verify question comment count",
                                 "verify comment icon and count for a second question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question comment count for first"

        ex = Spage.verify_question_comment_count(driver, 2, 0)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "verify question comment count",
                                 "verify comment icon and count for a second question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question comment count for second question"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

test_info = {
    'recommendation_title': u'A question in your survey is too long.',
    'recommendation_text': u'Long questions can sometimes be misinterpreted or boring to read—try to keep the length '
                           u'to 50 words or fewer.',
    'recommendation_q_nums': u'Applies to question 1'
}


@pytest.mark.survey_score
@pytest.mark.IB
@pytest.mark.C48268728
def test_verify_long_question_title_recommendations(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify Long Question title recommendation in Survey "
                                                           "Score modal")
    try:

        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        answerRows = []
        mySurvey.myQuestion.enter_question_title("abcd " * 61)
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[0])
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[1])
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Multiple Choice question Add to Live Preview",
                                 "Verifies that Multiple Choice question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Multiple Choice question added to live preview."

        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        answerRows = []
        mySurvey.myQuestion.enter_question_title("abcd " * 40)
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[0])
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[1])
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Multiple Choice question Add to Live Preview",
                                 "Verifies that Multiple Choice question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Multiple Choice question added to live preview."
        ex = mySurvey.myCreate.click_survey_score()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check Rate My Survey CTA",
                                 "verifies Rate My Survey CTA present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that create Rate My Survey present"

        ex = mySurvey.myCreate.verify_survey_score_modal()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Rate My Survey Modal",
                                 "verifies Rate My Survey modal box appears on screen",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Rate My Survey modal box appears on screen"

        ex = mySurvey.myCreate.verify_recommendation(recommendation_title=test_info["recommendation_title"],
                                                     recommendation_text=test_info["recommendation_text"],
                                                     recommendation_q_nums=test_info["recommendation_q_nums"],
                                                     is_single_recommendation=True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Long Question title recommendation",
                                 "Verifies Long Question title recommendation is shown",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Long Question title recommendation is shown"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
