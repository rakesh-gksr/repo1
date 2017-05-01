#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify adding slider question from Builder by dragging.

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
                               "TestSliderQTypeAddQuesFromBuilderByDragging/",  # report_relative_location
                               "test_sliderQType_addQuesFromBuilderByDragging",  # report_file_name_prefix
                               # test_suite_title
                               "verify adding slider question from Builder by dragging",
                               "Test to verify adding slider question from Builder by dragging",  # test_suite_description
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
@pytest.mark.C284097
def test_sliderQType_addQuesFromBuilderByDragging(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify adding slider question from Builder by dragging")
    try:
        we = mySurvey.myBuilder.getTargetPage(1)
        mySurvey.myBuilder.drag_n_drop_SliderAddButton(we)
        ex = mySurvey.myQuestion.verifySliderQuesOnPreview()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider question is added to live preview",
                                 "checks Slider question is added to live preview on clicking the Add button from"
                                 " Builder",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Slider question on preview."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
