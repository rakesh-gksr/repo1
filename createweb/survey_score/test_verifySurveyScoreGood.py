from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestVerifySurveyScoreGood",  # report_relative_location
                               "test_verifySurveyScoreGood",  # report_file_name_prefix
                               "Verify the Survey Score 'Good' and its corresponding message in survey "
                               "recommendation panel",
                               # test_suite_title
                               "Test to verify the Survey Score 'Good' and its corresponding message in survey "
                               "recommendation panel",
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
@pytest.mark.C47669126
def test_verify_survey_score_good(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify the Survey Score 'Good' and its corresponding "
                                                           "message in survey recommendation panel")
    try:

        mySurvey.myBuilder.click_SingleTextboxAddButton()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Single Textbox question Add to Live Preview",
                                 "Verifies that Single Textbox question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Single Textbox question added to live preview."

        mySurvey.myBuilder.click_DropdownAddButton()
        title = mySurvey.myLogic.RNG(30)
        answerRows = []
        mySurvey.myQuestion.enter_question_title(title)
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[0])
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[1])
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, answerRows[2])
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[3])
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[4])
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, answerRows[5])

        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Dropdown question Add to Live Preview",
                                 "Verifies that Dropdown question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Dropdown question added to live preview."

        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        title = mySurvey.myLogic.RNG(30)
        mySurvey.myQuestion.enter_question_title(title)

        for i in range(1, 16):
            mySurvey.myQuestion.enter_multipleChoice_answerText(i, mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question Add to Live Preview",
                                 "Verifies that MultipleChoice question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify MultipleChoice question added to live preview."

        mySurvey.myBuilder.click_RankingAddButton()
        answerRows = []
        title = mySurvey.myLogic.RNG(30)
        mySurvey.myQuestion.enter_question_title(title)
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[0])
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[1])
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        # Code to verify that question successfully saved at live preview
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 4)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question Add to Live Preview",
                                 "Verifies that ranking question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify ranking question added to live preview."

        mySurvey.myBuilder.click_MatrixRatingScaleAddButton()
        mySurvey.myQuestion.enter_question_title("How silly is this Survey?")
        for i in range(1, 10):
            mySurvey.myQuestion.enter_multipleChoice_answerText(i, "poi?")
        for i in range(6, 9):
            mySurvey.myQuestion.add_matrix_columnRow(i - 1)

        for i in range(1, 9):
            mySurvey.myQuestion.enter_matrix_answerText(i, i)
        mySurvey.myQuestion.click_question_save_from_edit_tab()

        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 5)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question Add to Live Preview",
                                 "Verifies that matrix rating scale question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify matrix rating scale question added to live preview."

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

        ex = mySurvey.myCreate.verify_survey_score()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Survey Score",
                                 "verifies that the Survey Score is shown as Good",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that the Survey Score is shown as Good"

        ex = mySurvey.myCreate.verify_recommended_message()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Recommendation Message",
                                 "verifies that recommendation message is shown as Good",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that the recommendation message is shown as Good"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
