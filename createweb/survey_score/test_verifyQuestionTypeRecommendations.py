# This Python file uses the following encoding: utf-8
from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestVerifyQuestionTypeRecommendations",  # report_relative_location
                               "test_verifyQuestionTypeRecommendations",  # report_file_name_prefix
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

recommendation_slides_data = {
    "1": {

            'recommendation_title': u'Your first question is a Matrix question type.',
            'recommendation_text': u'This question type can sometimes be overwhelming—ease your respondents into your '
                                   u'survey with a Multiple Choice or Dropdown question type.',
            'recommendation_q_nums': u'Applies to question 1'

        },
    "2": {

            'recommendation_title': u'A Matrix question in your survey has a lot of rows.',
            'recommendation_text': u'Large matrices can cause respondents to speed through their answers. For a '
                                   u'higher response rate, keep your row count to 5 or fewer.',
            'recommendation_q_nums': u'Applies to question 1'

        },
    "3": {

            'recommendation_title': u'A Matrix question in your survey has a lot of columns.',
            'recommendation_text': u'Large matrices can cause respondents to speed through their answers. For a '
                                   u'higher response rate, keep your column count to 5 or fewer.',
            'recommendation_q_nums': u'Applies to question 2'

        },
    "4": {

            'recommendation_title': u'A Matrix question in your survey can be further optimized.',
            'recommendation_text': u'Matrix question types should only be used if you need multiple items evaluated. '
                                   u'For a better experience, switch to Multiple Choice or Dropdown question types.',
            'recommendation_q_nums': u'Applies to question 3'

        },
    "5": {

            'recommendation_title': u'A Matrix of Dropdown Menus question in your survey has a lot of columns.',
            'recommendation_text': u'Large matrices can cause respondents to speed through their answers. For a '
                                   u'higher response rate, keep your column count to 4 or fewer.',
            'recommendation_q_nums': u'Applies to question 4'

        },
    "6": {

            'recommendation_title': u'A Matrix of Dropdown Menus question in your survey has a lot of rows.',
            'recommendation_text': u'Large matrices can cause respondents to speed through their answers. For a higher '
                                   u'response rate, keep your row count to 5 or fewer.',
            'recommendation_q_nums': u'Applies to question 5'

        },
    "7": {

            'recommendation_title': u'A Ranking question in your survey can be further optimized.',
            'recommendation_text': u'To make your survey faster to complete, switch all questions with 2 rows or fewer '
                                   u'to Multiple Choice question types.',
            'recommendation_q_nums': u'Applies to question 6'

        },
    "8": {

            'recommendation_title': u'A Ranking question in your survey has a lot of rows.',
            'recommendation_text': u'Asking respondents to rank too many items can be overwhelming. For a higher '
                                   u'response rate, keep your row count to 4 or fewer.',
            'recommendation_q_nums': u'Applies to question 7'

        }


}


@pytest.mark.survey_score
@pytest.mark.IB
@pytest.mark.C48262945
def test_verify_question_type_recommendations(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify Questions type Recommendations in Survey Score "
                                                           "modal")
    try:

        mySurvey.myBuilder.click_MatrixRatingScaleAddButton()
        mySurvey.myQuestion.enter_question_title("Q1")
        for i in range(1, 10):
            mySurvey.myQuestion.enter_multipleChoice_answerText(i, "row" + str(i))

        for i in range(0, 2):
            mySurvey.myQuestion.remove_matrix_columnRow(4)

        for i in range(1, 4):
            mySurvey.myQuestion.enter_matrix_answerText(i, "col" + str(i))
        mySurvey.myQuestion.click_question_save_from_edit_tab()

        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Q1 question Add to Live Preview",
                                 "Verifies that Q1 matrix rating scale question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Q1 matrix rating scale question added to live preview."

        mySurvey.myBuilder.click_MatrixRatingScaleAddButton()
        mySurvey.myQuestion.enter_question_title("Q2")
        for i in range(1, 3):
            mySurvey.myQuestion.enter_multipleChoice_answerText(i, "row" + str(i))
        for i in range(6, 9):
            mySurvey.myQuestion.add_matrix_columnRow(i - 1)
        for i in range(1, 9):
            mySurvey.myQuestion.enter_matrix_answerText(i, "col" + str(i))
        mySurvey.myQuestion.click_question_save_from_edit_tab()

        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Q2 question Add to Live Preview",
                                 "Verifies that Q2 matrix rating scale question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Q2 matrix rating scale question added to live preview."

        mySurvey.myBuilder.click_MatrixRatingScaleAddButton()
        mySurvey.myQuestion.enter_question_title("How silly is this Survey?")
        for i in range(1, 3):
            mySurvey.myQuestion.enter_multipleChoice_answerText(i, "row" + str(i))
        mySurvey.myQuestion.turn_off_setting("use_weight")
        for i in range(0, 4):
            mySurvey.myQuestion.remove_matrix_columnRow(2)
        mySurvey.myQuestion.enter_matrix_answerText(1, "col 1")
        mySurvey.myQuestion.click_question_save_from_edit_tab()

        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Q3 question Add to Live Preview",
                                 "Verifies that Q3 matrix rating scale question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Q3 matrix rating scale question added to live preview."

        mySurvey.myBuilder.click_MatrixOfDropdownMenusAddButton()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, mySurvey.myLogic.RNG(10))
        for i in range(3, 6):
            mySurvey.myQuestion.add_matrix_columnRow(i - 1)
        mySurvey.myQuestion.enter_matrix_answerText(1, mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_matrix_answerText(2, mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_matrix_answerText(3, mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_matrix_answerText(4, mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_matrix_answerText(5, mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_answer_choices_matrix_menu(1, mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_answer_choices_matrix_menu(2, mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_answer_choices_matrix_menu(3, mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_answer_choices_matrix_menu(4, mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_answer_choices_matrix_menu(5, mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 4)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Q4 question Add to Live Preview",
                                 "Verifies that Q4 matrix of dropdown menu question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Q4 matrix of dropdown question added to live preview."

        mySurvey.myBuilder.click_MatrixOfDropdownMenusAddButton()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        for i in range(1, 8):
            mySurvey.myQuestion.enter_multipleChoice_answerText(i, "row" + str(i))
        mySurvey.myQuestion.remove_matrix_columnRow(2)
        mySurvey.myQuestion.enter_matrix_answerText(1, mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_answer_choices_matrix_menu(1, mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 5)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Q5 question Add to Live Preview",
                                 "Verifies that Q5 matrix of dropdown menu question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Q5 matrix of dropdown question added to live preview."

        mySurvey.myBuilder.click_RankingAddButton()
        title = mySurvey.myLogic.RNG(30)
        mySurvey.myQuestion.enter_question_title(title)
        mySurvey.myQuestion.remove_matrix_columnRow(3)
        for i in range(1, 3):
            mySurvey.myQuestion.enter_multipleChoice_answerText(i, "row" + str(i))
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        # Code to verify that question successfully saved at live preview
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 6)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question Add to Live Preview",
                                 "Verifies that ranking question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify ranking question added to live preview."

        mySurvey.myBuilder.click_RankingAddButton()
        title = mySurvey.myLogic.RNG(30)
        mySurvey.myQuestion.enter_question_title(title)
        for i in range(1, 8):
            mySurvey.myQuestion.enter_multipleChoice_answerText(i, "row" + str(i))
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        # Code to verify that question successfully saved at live preview
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 7)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question Add to Live Preview",
                                 "Verifies that ranking question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify ranking question added to live preview."
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
        for slide, messages in recommendation_slides_data.iteritems():
            temp = int(slide) - 1
            ex = mySurvey.myCreate.survey_score_next_recommendation(str(temp))
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Click Down Arrow : " + str(slide),
                                     "Click and verifies down arrow for slide: " + str(slide),
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify click on slide: " + str(slide)
            ex = mySurvey.myCreate.verify_recommendation(recommendation_title=messages["recommendation_title"],
                                                         recommendation_text=messages["recommendation_text"],
                                                         recommendation_q_nums=messages["recommendation_q_nums"])
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Recommendation for Slide : " + str(slide),
                                     "Verifies recommendation message for slide:  " + str(slide),
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify recommendation message for slide:  " + str(slide)

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
