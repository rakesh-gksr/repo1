#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify syncing ranges on edit tab.

"""

from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSliderQTypeVerifySyncingRangesOnEditTab/",  # report_relative_location
                               "test_sliderQType_verifySyncingRangesOnEditTab",  # report_file_name_prefix
                               # test_suite_title
                               "verify syncing ranges on edit tab",
                               "Test to verify syncing ranges on edit tab",  # test_suite_description
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
@pytest.mark.C424125
def test_sliderQType_verifySyncingRangesOnEditTab(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "verify syncing ranges on edit tab.")
    try:

        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.click_question_options_tab()
        mySurvey.myQuestion.checkSliderScaleCheckbox()
        mySurvey.myQuestion.enter_min_max_range(2,99)
        ex = mySurvey.myQuestion.click_question_save_from_options_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider question",
                                 "checks Slider question is saved",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify slider question is saved."
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question Add to Live Preview",
                                 "Verifies that question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question added to live preview."
        mySurvey.myQuestion.click_on_question_to_edit(1)
        ex = mySurvey.myQuestion.verify_range_on_edit(2,99)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify range on Edit Tab",
                                 "checks Slider question is saved with range.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify on edit tab."
        ex = mySurvey.myQuestion.click_question_options_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Update range on Option Tab",
                                 "Updates the range on Option tab.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myQuestion.enter_min_max_range(4, 100)
        mySurvey.myQuestion.click_question_edit_tab()
        ex = mySurvey.myQuestion.verify_range_on_edit(4,100)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify updated range on Edit Tab",
                                 "checks updated range with valid range on Edit Tab.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify updated range on Edit Tab."
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider question",
                                 "checks Slider question is saved",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify slider question is saved."
        mySurvey.myQuestion.click_on_question_to_edit(1)
        ex = mySurvey.myQuestion.verify_range_on_edit(4,100)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify updated range on Edit Tab",
                                 "checks Slider question is saved with valid range on Edit Tab.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify updated range on Edit Tab."
        mySurvey.myQuestion.click_question_options_tab()
        ex = mySurvey.myQuestion.verify_range_on_option_tab(4,100)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify updated range on Options Tab",
                                 "checks updated range with valid range on Options Tab.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify updated range on Options Tab."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
