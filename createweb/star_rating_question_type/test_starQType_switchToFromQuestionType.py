from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from smsdk.qafw.rpage import pyramidsurveypage as Spage
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):

    report = reporting_wrapper("Create",  # report_feature_name
                               "TestStarQTypeSwitchToFromQuestionType/",  # report_relative_location
                               "test_starQType_switchToFromQuestionType",  # report_file_name_prefix
                               "verify switching from star to matrix, menu matrix or slider question type and "
                               "switching back to star and save star.",
                               # test_suite_title
                               ("Test to verify switching from star to matrix, menu matrix or slider question "
                                "type and switching back to star and save star."),
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
@pytest.mark.C822502
def test_starQType_switchingToMatrixThenStarQuestion(create_survey):
    driver, mySurvey, report = create_survey
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify switching from star to matrix question type "
                                                           "and switching back to star and save star.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        # code to add star question to survey
        mySurvey.myBuilder.click_star_rating_add_button()
        question_title = "Rate SurveyMonkey services"
        mySurvey.myQuestion.enter_question_title(question_title)
        ex = mySurvey.myQuestion.change_star_rating_question_scale("7")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that star question scale",
                                 "checks to make sure that star question scale changed to 7.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star question scale changed to 7"
        ex = mySurvey.myQuestion.change_star_rating_question_shape("thumb")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that star question shape",
                                 "checks to make sure that star question shape changed to thumb.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star question shape changed to thumb"
        ex = mySurvey.myQuestion.toggle_star_rating_label_checkbox()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Turn on ratings labels",
                                 "checks that checkbox is checked to turn on ratings label"
                                 " option for star rating question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to turn rating labels option"
        sender_label_list = ["label1", "label2", "label3", "label4", "label5", "label6", "label7"]
        ex = mySurvey.myQuestion.enter_range_label_for_star_rating_question(sender_label_list)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Fill range labels",
                                 "Verify the range labels are filled correctly or not",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to fill range labels for star rating question"
        ex = mySurvey.myQuestion.toggle_star_rating_na_column()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Turn on N/A option",
                                 "checks that checkbox is checked to turn on N/A option for star rating question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to turn on N/A option"
        # code to select other answer option checkbox
        mySurvey.myQuestion.turn_on_multichoice_otheroption()
        mySurvey.myQuestion.select_other_validation_format("Make sure it's a date (DD/MM/YYYY)")
        mySurvey.myQuestion.enter_min_validation_range("30/01/2011")
        mySurvey.myQuestion.enter_max_validation_range("31/01/2012")

        # code to change star question type to MenuMatrix textbox
        mySurvey.myQuestion.changeQType("Matrix")
        ex = mySurvey.myQuestion.verify_question_in_edit_mode('question-matrix')
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify change question type from Star to Matrix",
                                 "verifies that changed question type from Star to Matrix",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Matrix"
        # code to verify "others" appears selected and question title is persisting
        ex = mySurvey.myQuestion.verify_other_option()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "verify others appears selected",
                                 "verifies that others appears selected",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify others appears selected"
        ex = mySurvey.myQuestion.verifyQuestionTitleString(question_title)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "verify question title persist",
                                 "verifies that question title is persisted",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question title is persisted"
        # code to change MenuMatrix textbox question type to star
        mySurvey.myQuestion.changeQType("StarRating")
        ex = mySurvey.myQuestion.verify_question_in_edit_mode('question-emoji-rating')
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify change question type from Matrix to Star",
                                 "verifies that changed question type from Matrix to Star",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Matrix"
        # code to verify whether the options such as other answer option, scale and shape are appear
        # as checked/selected or not
        ex = mySurvey.myQuestion.verify_star_rating_question_option("thumb", "7")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify other field, scale and shape options",
                                 "Verified that star rating question options (other field, scale and shape) are still "
                                 "appears as checked / selected",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star rating question options (other field, scale and shape) are still appears " \
                   "as checked / selected."
        ex = mySurvey.myQuestion.verify_range_label_for_star_rating_question(sender_label_list)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify range labels",
                                 "Verify that labels are showing as it was entered earlier",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify labels are showing as it was entered earlier"
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Star Rating Question",
                                 "Verified that star rating question type saved without any error",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star rating question saved."
        ex = Spage.verify_star_elements(driver, 1, 7, "thumb")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify copied question shows 7 thumbs",
                                 "checks to make sure that copied star question is showing 7 thumbs",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify copied star question is showing 7 thumbs"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.IB
@pytest.mark.star_question
@pytest.mark.BVT
@pytest.mark.C822503
def test_starQType_switchingToMenuMatrixThenStarQuestion(create_survey):
    driver, mySurvey, report = create_survey
    # driver.maximize_window()
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify switching from star to menu matrix question type "
                                                           "and switching back to star and save star.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        # code to add star question to survey
        mySurvey.myBuilder.click_star_rating_add_button()
        question_title = "Rate SurveyMonkey services"
        mySurvey.myQuestion.enter_question_title(question_title)
        ex = mySurvey.myQuestion.change_star_rating_question_scale("10")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that star question scale",
                                 "checks to make sure that star question scale changed to 10.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star question scale changed to 10"
        ex = mySurvey.myQuestion.change_star_rating_question_shape("heart")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that star question shape",
                                 "checks to make sure that star question shape changed to heart.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star question shape changed to heart"
        ex = mySurvey.myQuestion.toggle_star_rating_label_checkbox()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Turn on ratings labels",
                                 "checks that checkbox is checked to turn on ratings label"
                                 " option for star rating question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to turn rating labels option"
        sender_label_list = ["label1", "label2", "label3", "label4", "label5", "label6", "label7", "label8", "label9",
                             "label10"]
        ex = mySurvey.myQuestion.enter_range_label_for_star_rating_question(sender_label_list)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Fill range labels",
                                 "Verify the range labels are filled correctly or not",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to fill range labels for star rating question"
        ex = mySurvey.myQuestion.toggle_star_rating_na_column()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Turn on N/A option",
                                 "checks that checkbox is checked to turn on N/A option for star rating question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to turn on N/A option"
        # code to select other answer option checkbox
        mySurvey.myQuestion.turn_on_multichoice_otheroption()
        mySurvey.myQuestion.select_other_validation_format("Make sure it's a date (DD/MM/YYYY)")
        mySurvey.myQuestion.enter_min_validation_range("30/01/2011")
        mySurvey.myQuestion.enter_max_validation_range("31/01/2012")

        # code to change star question type to MenuMatrix textbox
        mySurvey.myQuestion.changeQType("MenuMatrix")
        ex = mySurvey.myQuestion.verify_question_in_edit_mode('question-menu-matrix')
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify change question type from Slider to MenuMatrix",
                                 "verifies that changed question type from Slider to MenuMatrix",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MenuMatrix"
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify change question type from Star to MenuMatrix",
                                 "verifies that changed question type from Star to MenuMatrix",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MenuMatrix"
        # code to verify "others" appears selected and question title is persisting
        ex = mySurvey.myQuestion.verify_other_option()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "verify others appears selected",
                                 "verifies that others appears selected",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify others appears selected"
        ex = mySurvey.myQuestion.verifyQuestionTitleString(question_title)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "verify question title persist",
                                 "verifies that question title is persisted",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question title is persisted"
        # code to change MenuMatrix textbox question type to star
        mySurvey.myQuestion.changeQType("StarRating")
        ex = mySurvey.myQuestion.verify_question_in_edit_mode('question-emoji-rating')
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify change question type from Matrix to Star",
                                 "verifies that changed question type from Matrix to Star",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Matrix"
        # code to verify whether the options such as other answer option, scale and shape are appear
        # as checked/selected or not
        ex = mySurvey.myQuestion.verify_star_rating_question_option("heart", "10")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify other field, scale and shape options",
                                 "Verified that star rating question options (other field, scale and shape) are still "
                                 "appears as checked / selected",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star rating question options (other field, scale and shape) are still appears " \
                   "as checked / selected."
        ex = mySurvey.myQuestion.verify_range_label_for_star_rating_question(sender_label_list)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify range labels",
                                 "Verify that labels are showing as it was entered earlier",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify labels are showing as it was entered earlier"
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Star Rating Question",
                                 "Verified that star rating question type saved without any error",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star rating question saved."
        ex = Spage.verify_star_elements(driver, 1, 10, "heart")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify copied question shows 7 hearts",
                                 "checks to make sure that copied star question is showing 7 hearts",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify copied star question is showing 5 hearts"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.IB
@pytest.mark.star_question
@pytest.mark.BVT
@pytest.mark.C822506
def test_starQType_switchingToSliderThenStarQuestion(create_survey):
    driver, mySurvey, report = create_survey
    # driver.maximize_window()
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify switching from star to slider question type and "
                                                           "switching back to star and save star.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        # code to add star question to survey
        mySurvey.myBuilder.click_star_rating_add_button()
        question_title = "Rate SurveyMonkey services"
        mySurvey.myQuestion.enter_question_title(question_title)
        ex = mySurvey.myQuestion.change_star_rating_question_scale("2")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that star question scale",
                                 "checks to make sure that star question scale changed to 2.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star question scale changed to 2"
        ex = mySurvey.myQuestion.change_star_rating_question_shape("thumb")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that star question shape",
                                 "checks to make sure that star question shape changed to thumb.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star question shape changed to thumb"
        ex = mySurvey.myQuestion.toggle_star_rating_label_checkbox()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Turn on ratings labels",
                                 "checks that checkbox is checked to turn on ratings label"
                                 " option for star rating question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to turn rating labels option"
        for i in range(3, 8):
            mySurvey.myQuestion.add_matrix_columnRow(i - 1)

        sender_label_list = ["label1", "label2", "label3", "label4", "label5", "label6", "label7"]
        ex = mySurvey.myQuestion.enter_range_label_for_star_rating_question(sender_label_list)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Fill range labels",
                                 "Verify the range labels are filled correctly or not",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to fill range labels for star rating question"
        ex = mySurvey.myQuestion.toggle_star_rating_na_column()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Turn on N/A option",
                                 "checks that checkbox is checked to turn on N/A option for star rating question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to turn on N/A option"
        # code to select other answer option checkbox
        mySurvey.myQuestion.turn_on_multichoice_otheroption()
        mySurvey.myQuestion.select_other_validation_format("Make sure it's a date (DD/MM/YYYY)")
        mySurvey.myQuestion.enter_min_validation_range("30/01/2011")
        mySurvey.myQuestion.enter_max_validation_range("31/01/2012")

        # code to change star question type to MenuMatrix textbox
        mySurvey.myQuestion.changeQType("Slider")
        ex = mySurvey.myQuestion.verify_question_in_edit_mode('question-open-ended-single', 'slider')
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify change question type from Star to Slider",
                                 "verifies that changed question type from Star to Slider",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Slider"
        # code to verify question title is persisted or not
        ex = mySurvey.myQuestion.verifyQuestionTitleString(question_title)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "verify question title persist",
                                 "verifies that question title is persisted",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question title is persisted"
        # code to change MenuMatrix textbox question type to star
        mySurvey.myQuestion.changeQType("StarRating")
        ex = mySurvey.myQuestion.verify_question_in_edit_mode('question-emoji-rating')
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify change question type from Matrix to Star",
                                 "verifies that changed question type from Matrix to Star",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Matrix"
        # code to verify whether the options such as other answer option, scale and shape are appear
        # as checked/selected or not
        ex = mySurvey.myQuestion.verify_star_rating_question_option("thumb", "7")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify other field, scale and shape options",
                                 "Verified that star rating question options (other field, scale and shape) are still "
                                 "appears as checked / selected",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star rating question options (other field, scale and shape) are still appears " \
                   "as checked / selected."
        ex = mySurvey.myQuestion.verify_range_label_for_star_rating_question(sender_label_list)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify range labels",
                                 "Verify that labels are showing as it was entered earlier",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify labels are showing as it was entered earlier"
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Star Rating Question",
                                 "Verified that star rating question type saved without any error",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star rating question saved."
        ex = Spage.verify_star_elements(driver, 1, 7, "thumb")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify copied question shows 7 thumbs",
                                 "checks to make sure that copied star question is showing 7 thumbs",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify copied star question is showing 7 thumbs"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
