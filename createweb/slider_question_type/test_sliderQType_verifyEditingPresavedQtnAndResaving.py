#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify adding and removin AB test on slider - option tab

"""

from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSliderQTypeQuestionAddAndRemoveABText/",  # report_relative_location
                               "test_sliderQTypeVerifyEditingPresavedQtnAndResaving",  # report_file_name_prefix
                               # test_suite_title
                               "verify editing presaved question and resaving it works",
                               "Test to verify editing presaved question and resaving it works",  # test_suite_description
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
@pytest.mark.IB
@pytest.mark.C284110
def test_sliderQTypeVerifyEditingPresavedQtnAndResaving(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "verify editing presaved question and resaving it works")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Slider question type to survey",
                                 "Verified that slider question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add slider question to survey."
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider Question Add to Live Preview",
                                 "Verifies that slider question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify slider question added to live preview."
        ex = mySurvey.myQuestion.click_on_question_to_edit()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Open Slider question in edit mode",
                                 "Verified that slider question opened in edit mode",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify slider question opened in edit mode."
        # code to select other answer option checkbox
        mySurvey.myQuestion.turn_on_multichoice_otheroption()
        mySurvey.myQuestion.enter_otheroption_labletext('Hello Test')
        ex = mySurvey.myQuestion.changeOtherAnswerOptionSize("Single Line of Text", "10 characters")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Set Other Answer Option Input Width",
                                 "Verified that slider question other answer option input width is set to 10",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify slider question selected options are still appears as checked."
        mySurvey.myQuestion.click_question_options_tab()
        # Code to turning on required answer checkbox
        mySurvey.myQuestion.turn_on_answer_required()
        mySurvey.myQuestion.click_question_edit_tab()
        # code to click on save question button
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Slider question type to survey",
                                 "Verified that slider question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add slider question to survey."
        # Code to open question in edit mode
        mySurvey.myQuestion.click_on_question_to_edit()
        # code to verify whether the options such as other answer option, text size and width of text is appear
        # as checked or not
        ex = mySurvey.myQuestion.verify_selected_options()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify selected options",
                                 "Verified that slider question selected options are still appears as checked",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify slider question selected options are still appears as checked."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
