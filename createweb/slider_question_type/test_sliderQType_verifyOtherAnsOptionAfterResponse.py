#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify checking and unchecking 'other' answer option and saving question after responses have been collected

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
                               "TestSliderQType_verifyOtherAnsOptionAfterResponse/",  # report_relative_location
                               "test_sliderQType_verifyOtherAnsOptionAfterResponse",  # report_file_name_prefix
                               # test_suite_title
                               "verify checking and unchecking 'other' answer option and saving question after "
                               "responses have been collected",
                               "Test to verify checking and unchecking 'other' answer option and saving question after "
                               "responses have been collected",  # test_suite_description
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

@pytest.mark.skipif(True, reason="skip other option for slider")
@pytest.mark.the_other_slider_option
@pytest.mark.slider_question
@pytest.mark.BVT
@pytest.mark.IB
@pytest.mark.C284517
@pytest.mark.C284518
def test_sliderQType_verifyOtherAnsOptionAfterResponse(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "verify checking and unchecking 'other' answer option and saving question after responses have been collected")
    try:
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
        # code to select other answer option checkbox
        ex = mySurvey.myQuestion.turn_on_multichoice_otheroption()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Checked Other Answer Option checkbox on Q1 slider",
                                 "Verified that Other answer option checkbox is checked on Q1 slider question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Other answer option checkbox is checked on Q1 slider question"
        mySurvey.myQuestion.enter_otheroption_labletext('Hello Test')
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
                     driver, mySurvey.collector_url, mySurvey.survey_title)

        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verifying A B Text with Collector URL:" + mySurvey.collector_url,
                                 "Driver goes to the survey and it took " + str(total_load_time) +
                                 " to open page.",opened, False, not opened, driver)

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
        ex = mySurvey.myQuestion.turn_off_multichoice_otheroption()

        report.add_report_record(ReportMessageTypes.TEST_STEP, "Deselect other answer option",
                                 "Verified that other answer option is deselected",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify other answer option is deselected"
        # code to save Q1 slider question
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Save Q1 Slider question type",
                                 "Verified that Q1 slider question type is saved",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Q1 slider question type is saved."
        # code to edit Q2 slider question
        mySurvey.myQuestion.click_on_question_to_edit(2)
        ex = mySurvey.myQuestion.turn_on_multichoice_otheroption()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Checked Other Answer Option checkbox on Slider Q2",
                                 "Verified that Other answer option checkbox is checked on Q2 slider question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Other answer option checkbox is checked on Q2 slider question"
        mySurvey.myQuestion.enter_otheroption_labletext('Hello Test')
        # Code to save question
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Update Q2 Slider question type to survey",
                                 "Verified that Q2 slider question type updated to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Q2 slider question updated to survey."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
