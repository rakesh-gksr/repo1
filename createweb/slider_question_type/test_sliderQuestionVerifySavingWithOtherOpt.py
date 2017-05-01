#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify saving question with 'other' answer option selected.

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
                               "TestSliderQuestionVerifySavingWithOtherOpt/",  # report_relative_location
                               "test_sliderQuestionVerifySavingWithOtherOpt",  # report_file_name_prefix
                               # test_suite_title
                               "verify saving question with 'other' answer option selected",
                               "Test to verify saving question with 'other' answer option selected",
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

@pytest.mark.skipif(True, reason="skip other option for slider")
@pytest.mark.the_other_slider_option
@pytest.mark.slider_question
@pytest.mark.IB
@pytest.mark.C284109
def test_sliderQuestionVerifySavingWithOtherOpt(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "verify saving question with 'other' answer option selected.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title("Your expectation?")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myQuestion.click_on_question_to_edit(1)
        ex = mySurvey.myQuestion.turn_on_multichoice_otheroption()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Turn on other option",
                                 "checks that checkbox is checked to turn on other option for slider question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add Other answer option"
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider saved",
                                 "Verified that slider question is saved",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to save slider question"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
