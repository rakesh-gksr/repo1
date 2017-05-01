#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify limitations once responses have been collected

"""

from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest
from smsdk.qafw.create import collector
from smsdk.qafw.rpage import pyramidsurveypage as Spage
import time


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestStarQTypeVerifyLimitationsOnceResponseCollected/",  # report_relative_location
                               "test_starQType_verifyLimitationsOnceResponseCollected",  # report_file_name_prefix
                               # test_suite_title
                               "verify limitations on star once responses have been collected",
                               "Test to verify limitations on star once responses have been collected",
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


@pytest.mark.star_quesiton
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C812402
def test_starQType_verifyLimitationsOnceResponseCollected(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "verify limitations on star once responses have been collected")
    try:
        survey_id = mySurvey.survey_id
        user_id = mySurvey.user_id
        survey_json = mySurvey.mySvc_holder.svysvc.get_survey(survey_id, user_id)
        survey_title = survey_json["title"]["text"]
        survey_create_design_page_url = mySurvey.myDesign.get_url()
        mySurvey.myBuilder.click_star_rating_add_button()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Q1 Star question type to survey ",
                                 "Verified that Q1 star question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add Q1 star question to survey."

        mySurvey.myBuilder.click_star_rating_add_button()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Q2 Star question type to survey ",
                                 "Verified that Q2 star question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add Q2 star question to survey."

        # Code to open Q1 star question in edit mode
        mySurvey.myQuestion.click_on_question_to_edit()
        # code to swtich to option tab
        mySurvey.myQuestion.click_question_options_tab()
        ex = mySurvey.myQuestion.click_question_ABtest_option()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question edit show A B question text",
                                 "Verified that question edit is showing A B question text",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question edit is showing A B question text."
        # Code to enter values for A B text
        mySurvey.myQuestion.enter_questionAB_title()
        # Code to save question
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Update Q1 Star question type to survey ",
                                 "Verified that Q1 star question type updated to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Q1 star question updated to survey."
        # code to generate collector url
        mySurvey.collector_id, mySurvey.collector_url = collector.create_collector(
            driver, mySurvey.user_id, mySurvey.survey_id)
        opened, total_load_time = Spage.open_survey(
                     driver, mySurvey.collector_url, survey_title)

        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verifying A B Text with Collector URL:" + mySurvey.collector_url,
                                 "Driver goes to the survey and it took " + str(total_load_time) +
                                 " to open page.", opened, False, not opened, driver)
        assert opened, "Failed to verify A B text with Collector"

        ex = Spage.attempt_star_rating_question(driver, 1, 4)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Take Survey",
                                 "Verified that first star question attempted successfully",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify first star question attempted successfully."

        ex = Spage.attempt_star_rating_question(driver, 2, 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Take Survey",
                                 "Verified that second star question attempted successfully",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify second star question attempted successfully."

        ex = mySurvey.myDesign.click_preview_done_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Submit Survey",
                                 "Verified that survey submitted successfully",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify survey submitted successfully."
        # Code to go back to survey design page
        driver.get(survey_create_design_page_url)
        # Code to click on star option tab to check editing limitations
        # Code to open Q1 star question in edit mode
        mySurvey.myQuestion.click_on_question_to_edit()
        ex = mySurvey.myQuestion.verify_ab_text_boxes_disabled()

        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify A B text disabled",
                                 "Verified that A B text boxes are disabled",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify A B text boxes are disabled."
        mySurvey.myQuestion.click_question_options_tab()
        ex = mySurvey.myQuestion.verify_AB_Toggle_Disabled()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify user can't remove AB test setting on Q1",
                                 "Verified that user can't remove AB test setting on Q1",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify user can't remove AB test setting on Q1."
        mySurvey.myQuestion.click_question_edit_tab()
        # Code to fill rating labels
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
        # Code to turn on other comment option
        ex = mySurvey.myQuestion.turn_on_multichoice_otheroption()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Turn on other comment option",
                                 "checks that checkbox is checked to turn on other option for star rating question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add Other comment option"

        # code to save Q1 star question
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Q1 Star question type",
                                 "Verified that Q1 star question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add Q1 star question to survey."
        # code to edit Q2 star question
        mySurvey.myQuestion.click_on_question_to_edit(2)
        # code to switch to option tab
        mySurvey.myQuestion.click_question_options_tab()
        # code to verify A B text checkbox is disabled
        ex = mySurvey.myQuestion.verify_AB_Toggle_Disabled()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify user can't add AB test on Q2",
                                 "Verified that user can't add AB test on Q2",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify user can't add AB test on Q2."

        mySurvey.myQuestion.click_question_edit_tab()
        # Code to fill rating labels
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
        # Code to turn on other comment option
        ex = mySurvey.myQuestion.turn_on_multichoice_otheroption()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Turn on other comment option",
                                 "checks that checkbox is checked to turn on other option for star rating question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add Other comment option"
        # code to save Q2 star question
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Q2 Star question type",
                                 "Verified that Q2 star question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add Q2 star question to survey."

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.star_quesiton
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C874233
def test_starQType_verifyEditingLimitations(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE, "verify editing limitations for number of scales")
    try:
        survey_id = mySurvey.survey_id
        user_id = mySurvey.user_id
        survey_json = mySurvey.mySvc_holder.svysvc.get_survey(survey_id, user_id)
        survey_title = survey_json["title"]["text"]
        survey_create_design_page_url = mySurvey.myDesign.get_url()
        mySurvey.myBuilder.click_star_rating_add_button()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Q1 Star question type to survey ",
                                 "Verified that Q1 star question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add Q1 star question to survey."

        mySurvey.myBuilder.click_star_rating_add_button()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Q2 Star question type to survey ",
                                 "Verified that Q2 star question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add Q2 star question to survey."
        # Code to open Q1 star question in edit mode
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Q1 Star question type to survey ",
                                 "Verified that Q1 star question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add Q1 star question to survey."

        # Code to open Q2 star question in edit mode
        mySurvey.myQuestion.click_on_question_to_edit(2)
        # code to swtich to option tab
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
        sender_label_list = ["label1", "label2", "label3", "label4", "label5", "label6", "label7", "label8",
                             "label9", "label10"]
        ex = mySurvey.myQuestion.enter_range_label_for_star_rating_question(sender_label_list)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Fill range labels",
                                 "Verify the range labels are filled correctly or not",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to fill range labels for star rating question"
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that Q2 star question is saved",
                                 "checks to make sure that Q2 star question is saved with all required fields.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify saving of Q2 star question"
        ex = Spage.verify_star_elements(driver, 2, 10, "heart")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify Q2 star question shows 10 heart",
                                 "checks to make sure that Q2 star question is showing 10 hearts",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Q2 star question is showing 10 hearts"
        # code to generate collector url
        mySurvey.collector_id, mySurvey.collector_url = collector.create_collector(
            driver, mySurvey.user_id, mySurvey.survey_id)
        opened, total_load_time = Spage.open_survey(
                     driver, mySurvey.collector_url, survey_title)

        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verifying A B Text with Collector URL:" + mySurvey.collector_url,
                                 "Driver goes to the survey and it took " + str(total_load_time) +
                                 " to open page.", opened, False, not opened, driver)
        assert opened, "Failed to verify A B text with collector URL."

        ex = Spage.attempt_star_rating_question(driver, 1, 4)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Take Survey",
                                 "Verified that first star question attempted successfully",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify first star question attempted successfully."

        ex = Spage.attempt_star_rating_question(driver, 2, 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Take Survey",
                                 "Verified that second star question attempted successfully",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify second star question attempted successfully."

        ex = mySurvey.myDesign.click_preview_done_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Submit Survey",
                                 "Verified that survey submitted successfully",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify survey submitted successfully."
        # Code to go back to survey design page
        driver.get(survey_create_design_page_url)
        # Code to click on star option tab to check editing limitations
        # Code to open Q1 star question in edit mode
        time.sleep(5)
        mySurvey.myQuestion.click_on_question_to_edit()
        ex = mySurvey.myQuestion.verify_disabled_star_rating_question_scale()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Scale dropdown",
                                 "Verified that scale dropdown is disabled for Q1 star rating question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify scale dropdown is disabled for Q1 star rating question type."
        # code to save Q1 star question
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Q1 Star question type",
                                 "Verified that Q1 star question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add Q1 star question to survey."
        # code to edit Q2 star question
        mySurvey.myQuestion.click_on_question_to_edit(2)
        # Code to verify that scale should be disabled and user can't change them.
        ex = mySurvey.myQuestion.verify_disabled_star_rating_question_scale()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Scale dropdown",
                                 "Verified that scale dropdown is disabled for Q2 star rating question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify scale dropdown is disabled for Q2 star rating question type."
        # Code to verify that user can't delete/add/hide existing labels
        ex = mySurvey.myQuestion.verify_unable_to_add_delete_labels()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify add and remove actions",
                                 "checks that add and delete action button is not showing for exising labels for "
                                 "star rating question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add and delete action button is not showing for exising labels for " \
                   "star rating question"
        # Code to verify that user should be able to change the shape
        ex = mySurvey.myQuestion.change_star_rating_question_shape("thumb")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that star question shape",
                                 "checks to make sure that able to change the shape.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify user is able to change the shape"
        # code to save Q2 star question
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Q2 Star question type",
                                 "Verified that Q2 star question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add Q2 star question to survey."

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
