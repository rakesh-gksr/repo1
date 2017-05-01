#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify survey creator should be able to define start position from dropdown-option tab.

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
                               "TestSliderQuestionVerifyAllStartPositionFromDropdown/",  # report_relative_location
                               "test_sliderQuestionVerifyAllStartPositionFromDropdown",  # report_file_name_prefix
                               ("verify survey creator should be able to define start position"
                                " from dropdown-option tab."),  # test_suite_title
                               ("verify survey creator should be able to define start position"
                                " from dropdown-option tab."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os

    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime(
        "%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()

    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.slider_question
@pytest.mark.C284114
@pytest.mark.IB
def test_sliderQuestionVerifyAllStartPositionFromDropdown(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify survey creator should be able to define start"
                                                           " position from dropdown-option tab")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        slider_positions = ["left", "center", "right"]
        for key, position in enumerate(slider_positions):
            if key > 0:
                mySurvey.myQuestion.click_on_question_to_edit(1)
            mySurvey.myQuestion.click_question_options_tab()
            if position != "right":
                mySurvey.myQuestion.checkSliderScaleCheckbox()

            mySurvey.myQuestion.selectSliderStartPosition(position)
            ex = mySurvey.myQuestion.click_question_save_from_options_tab()
            report.add_report_record(ReportMessageTypes.TEST_STEP,
                                     "Verify that slider question is saved.",
                                     "checks to make sure that slider question is saved.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify saving of slider question."
            mySurvey.myQuestion.click_on_question_to_edit(1)
            mySurvey.myQuestion.click_question_options_tab()
            if position == "left":
                mySurvey.myQuestion.checkSliderScaleCheckbox()
            ex = mySurvey.myQuestion.verify_slider_position(position)
            report.add_report_record(ReportMessageTypes.TEST_STEP,
                                     "Verify that slider saved with start position as "+str(position),
                                     "checks to make sure that slider saved with start"
                                     " position as "+str(position),
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify start position of slider question."
            mySurvey.myQuestion.click_question_save_from_options_tab()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
