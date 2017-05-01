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
from dynamic_tests.dynamic_tests_config import answers


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSliderQTypeVerifyLimitationsOnceResponseCollected/",  # report_relative_location
                               "test_sliderQType_verifyLimitationsOnceResponseCollected",  # report_file_name_prefix
                               # test_suite_title
                               "verify limitations once responses have been collected",
                               "Test to verify limitations once responses have been collected",  # test_suite_description
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


@pytest.mark.slider_quesiton
@pytest.mark.IB
@pytest.mark.C284515
def test_sliderQType_verifyLimitationsOnceResponseCollected(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "verify limitations once responses have been collected")
    try:
        survey_id = mySurvey.survey_id
        user_id = mySurvey.user_id
        survey_json = mySurvey.mySvc_holder.svysvc.get_survey(survey_id, user_id)
        survey_title = survey_json["title"]["text"]
        survey_create_design_page_url = mySurvey.myDesign.get_url()
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Q1 Slider question type to survey ",
                                 "Verified that Q1 slider question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add Q1 slider question to survey."
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Q2 Slider question type to survey ",
                                 "Verified that Q2 slider question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add Q2 slider question to survey."

        # Code to open Q1 slider question in edit mode
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
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Update Q1 Slider question type to survey ",
                                 "Verified that Q1 slider question type updated to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Q1 slider question updated to survey."
        # code to generate collector url
        mySurvey.collector_id, mySurvey.collector_url = collector.create_collector(
            driver, mySurvey.user_id, mySurvey.survey_id)
        opened, total_load_time = Spage.open_survey(
                     driver, mySurvey.collector_url, survey_title)

        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verifying A B Text with Collector URL:" + mySurvey.collector_url,
                                 "Driver goes to the survey and it took " + str(total_load_time) +
                                 " to open page.",opened, False, not opened, driver)
        assert opened, "Failed to verify A B text with collector."

        ex = Spage.take_survey(driver, answers[1])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Take Survey",
                                 "Verified that both slider questions attempted successfully",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify slider questions attempted successfully."
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
        # Code to click on slider option tab to check editing limitations
        # Code to open Q1 slider question in edit mode
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
        # code to verify second slider question
        mySurvey.myQuestion.click_question_edit_tab()
        # code to save Q1 slider question
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Q1 Slider question type",
                                 "Verified that Q1 slider question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add Q1 slider question to survey."
        # code to edit Q2 slider question
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
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
