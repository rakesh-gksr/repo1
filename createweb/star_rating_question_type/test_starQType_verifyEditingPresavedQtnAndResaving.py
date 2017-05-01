#!/usr/bin/env python
# -*- coding: utf-8 -*-

from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestStarQTypeQuestionAddAndRemoveABText/",  # report_relative_location
                               "test_starQTypeVerifyEditingPresavedQtnAndResaving",  # report_file_name_prefix
                               # test_suite_title
                               "verify editing presaved question and resaving it works",
                               "Test to verify editing presaved question and resaving it works",
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


@pytest.mark.star_question
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C812371
def test_starQTypeVerifyEditingPresavedQtnAndResaving(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE, "verify editing presaved question and resaving it works")
    try:

        mySurvey.myBuilder.click_star_rating_add_button()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Star question type to survey",
                                 "Verified that star rating question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add star rating question to survey."

        ex = mySurvey.myQuestion.click_on_question_to_edit()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Open Star question in edit mode",
                                 "Verified that star rating question opened in edit mode",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star rating question opened in edit mode."
        # Code to change the star rating question scale
        ex = mySurvey.myQuestion.change_star_rating_question_scale("6")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify star rating question scale",
                                 "checks to make sure that star rating question scale changed to 6.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star rating question scale changed to 6"
        # Code to change the star rating question shape
        ex = mySurvey.myQuestion.change_star_rating_question_shape("thumb")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify star rating question shape",
                                 "checks to make sure that star rating question shape changed to Thumb.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star rating question shape changed to Thumb"
        # code to select other answer option checkbox
        mySurvey.myQuestion.turn_on_multichoice_otheroption()
        # Code to turning on required answer checkbox
        mySurvey.myQuestion.click_question_options_tab()
        # Code to turning on required answer checkbox
        ex = mySurvey.myQuestion.turn_on_answer_required()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify star rating question required answer checkbox ",
                                 "checks to make sure that star rating question required answer checkbox is checked.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star rating question required answer checkbox is checked"
        mySurvey.myQuestion.click_question_edit_tab()
        # code to click on save question button
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Star Rating question type",
                                 "Verified that star rating question type saved",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star rating question saved."
        # Code to open question in edit mode
        mySurvey.myQuestion.click_on_question_to_edit()
        # code to verify whether the options such as other answer option, scale and shape are appear
        # as checked/selected or not
        ex = mySurvey.myQuestion.verify_star_rating_question_option("thumb", "6")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify other field, scale and shape options",
                                 "Verified that star rating question options (other field, scale and shape) are still "
                                 "appears as checked / selected",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star rating question options (other field, scale and shape) are still appears " \
                   "as checked / selected."
        mySurvey.myQuestion.click_question_options_tab()
        ex = mySurvey.myQuestion.verify_required_option(True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify required answer checkbox",
                                 "Verified that star rating question required answer checkbox is checked",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star rating question required answer checkbox is checked."
        mySurvey.myQuestion.click_question_edit_tab()
        # code to click on save question button
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Star Rating Question",
                                 "Verified that star rating question type added to survey without any error",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star rating question saved."

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
