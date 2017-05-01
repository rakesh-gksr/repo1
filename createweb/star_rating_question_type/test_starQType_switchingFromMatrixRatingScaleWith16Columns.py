from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):

    report = reporting_wrapper("Create",  # report_feature_name
                               "TestStarQTypeSwitchingFromMatrixRatingScaleWith16Columns/",  # report_relative_location
                               "test_starQType_switchingFromMatrixRatingScaleWith16Columns",  # report_file_name_prefix
                               "verify switching from matrix/rating scale with 16 columns to star",
                               # test_suite_title
                               "Test to verify switching from matrix/rating scale with 16 columns to star",
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


@pytest.mark.IB
@pytest.mark.star_question
@pytest.mark.BVT
@pytest.mark.C822557
def test_starQType_switchingFromMatrixRatingScaleWith16Columns(create_survey):
    driver, mySurvey, report = create_survey
    # driver.maximize_window()
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify switching from matrix/rating scale with 16 columns "
                                                           "to star.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        # code to add star question to survey
        mySurvey.myBuilder.click_MatrixRatingScaleAddButton()
        title = mySurvey.myLogic.RNG(30)
        answerRows = []
        mySurvey.myQuestion.enter_question_title(title)
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[0])
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[1])
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, answerRows[2])

        for i in range(6, 17):
            mySurvey.myQuestion.add_matrix_columnRow(i - 1)
        # code to toggle N/A column
        mySurvey.myQuestion.toggle_star_rating_na_column()
        for i in range(1, 17):
            row = mySurvey.myLogic.RNG(20)
            mySurvey.myQuestion.enter_matrix_answerText(i, row)

        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Matrix Rating scale question",
                                 "Verifies that matrix rating scale question is saved.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify matrix rating scale question is saved."
        mySurvey.myQuestion.click_on_question_to_edit()
        # code to change star question type to MatrixRatingScale textbox
        mySurvey.myQuestion.changeQType("StarRating")
        ex = mySurvey.myQuestion.verify_question_in_edit_mode('question-emoji-rating')
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify change question type from MatrixRatingScale to Star",
                                 "verifies that changed question type from MatrixRatingScale to Star",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to StarRating"
        ex = mySurvey.myQuestion.verify_range_labels_count(16)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify range labels columns",
                                 "Verify that range labels columns count is 16",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify range labels columns count is 16"
        # Code to verify that question can not be saved with 16 columns
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_star_rating_max_label_limit_err()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify max label limit error",
                                 "Verify that max label limit error message present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify max label limit error message present"
        for i in range(11, 17):
            mySurvey.myQuestion.delete_columnChoice_answerRow(11)
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify Save Star Rating question type",
                                 "verifies that Star Rating question type saved",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Star Rating question type saved"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
