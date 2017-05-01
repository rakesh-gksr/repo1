#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify setting min number in the range lower than saved min number and saving question.

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
                               "TestSliderQTypeVerifySavingAfterUpdatingMinRangeLowerThanPrevVal/",
                               # report_relative_location
                               "test_sliderQType_verifySavingAfterUpdatingMinRangeLowerThanPrevVal",
                               # report_file_name_prefix
                               # test_suite_title
                               ("verify setting min number in the range lower than saved min number and saving "
                                "question"),
                               ("verify setting min number in the range lower than saved min number and saving "
                                "question"),  # test_suite_description
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
@pytest.mark.C508172
def test_sliderQType_verifySavingAfterUpdatingMinRangeLowerThanPrevVal(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "verify setting min number in the range lower than saved min number and saving question")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider question",
                                 "checks Slider question is saved",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify slider question is saved."
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider question Add to Live Preview",
                                 "Verifies that Slider question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Slider question added to live preview."
        mySurvey.myQuestion.click_on_question_to_edit()
        mySurvey.myQuestion.click_question_options_tab()
        mySurvey.myQuestion.checkSliderScaleCheckbox()
        mySurvey.myQuestion.enter_min_max_range(4, 100)
        ex = mySurvey.myQuestion.click_question_save_from_options_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Slider question saved with range value 4-100.",
                                 "checks Slider question is saved with updated values i.e 4-100",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to save slider question with range value 4-100."
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider question saved with range value 4-100",
                                 "Verifies that Slider question saved with range value 4-100 to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Slider question saved with range value 4-100 to live preview."
        mySurvey.myQuestion.click_on_question_to_edit()
        mySurvey.myQuestion.click_question_options_tab()
        ex = mySurvey.myQuestion.get_slider_scale_option_status()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that slider question Adjust scale option status",
                                 "checks to make sure that slider question is saved with Adjust scale option  ticked.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Adjust scale option  ticked"
        ex = mySurvey.myQuestion.verify_range_on_option_tab(4, 100)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify updated range i.e 4-100 on Options Tab",
                                 "checks updated range with valid range on Options Tab.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify updated range on Options Tab i.e 4-100."
        ex = mySurvey.myQuestion.click_question_save_from_options_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider question",
                                 "checks Slider question is saved",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify slider question is saved."

        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider question Add to Live Preview",
                                 "Verifies that Slider question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Slider question added to live preview."

        mySurvey.myQuestion.click_on_question_to_edit()
        mySurvey.myQuestion.click_question_options_tab()
        mySurvey.myQuestion.enter_min_max_range(3, 100)
        ex = mySurvey.myQuestion.click_question_save_from_options_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Slider question saved with lower range value i.e 3-100.",
                                 "checks Slider question is saved with minimum value lower than previous value",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to save slider question with updated lower range value."
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider question saved with lower range "
                                                               "value i.e 3-100 to live preview",
                                 "Verifies that Slider question saved with minimum value lower than previous value to "
                                 "live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Slider question saved with minimum value lower than previous value to live " \
                   "preview."

        mySurvey.myQuestion.click_on_question_to_edit()
        mySurvey.myQuestion.click_question_options_tab()
        ex = mySurvey.myQuestion.get_slider_scale_option_status()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that slider question Adjust scale option status",
                                 "checks to make sure that slider question is saved with Adjust scale option  ticked.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Adjust scale option  ticked"
        ex = mySurvey.myQuestion.verify_range_on_option_tab(3, 100)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify updated range i.e 3-100 on Options Tab",
                                 "checks updated range with valid range on Options Tab.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify updated range on Options Tab i.e 3-100."
        ex = mySurvey.myQuestion.click_question_save_from_options_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider question",
                                 "checks Slider question is saved",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify slider question is saved."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
