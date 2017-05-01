#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify adding and removing AB test on slider - option tab

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
                               "test_sliderQType_questionAddAndRemoveABText",  # report_file_name_prefix
                               # test_suite_title
                               "verify adding and removing AB test on slider - option tab",
                               "Test to verify adding and removing AB test on slider - option tab",
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


@pytest.mark.slider_question
@pytest.mark.IB
@pytest.mark.C284117
def test_sliderQType_questionAddAndRemoveABText(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "verify adding and removing AB test on slider - option tab")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SliderAddButton()
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
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Slider question type to survey ",
                                 "Verified that slider question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add slider question to survey."
        # Code to open question in edit mode
        mySurvey.myQuestion.click_on_question_to_edit()

        mySurvey.myQuestion.click_question_options_tab()
        # Code to deselect AB texts
        mySurvey.myQuestion.click_question_ABtest_option()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question edit do not show A B question text",
                                 "Verified that question edit is not showing A B question text",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question edit is not showing A B question text."
        mySurvey.myQuestion.click_question_edit_tab()
        # Code to save question
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Slider question type to survey ",
                                 "Verified that slider question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add slider question to survey."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
