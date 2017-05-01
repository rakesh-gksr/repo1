#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify user can't add any additional rows.

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
                               "TestSliderQTypeCountQuestionRows/",  # report_relative_location
                               "test_sliderQType_countQuestionRows",  # report_file_name_prefix
                               # test_suite_title
                               "verify user can't add any additional rows",
                               "Test to verify user can't add any additional rows",  # test_suite_description
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
@pytest.mark.C284108
def test_sliderQType_countQuestionRows(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "verify user can't add any additional rows")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SliderAddButton()
        ex = True if mySurvey.myQuestion.count_rows_in_edit() == 3 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "verify rows in edit Slider Question",
                                 "verify user can't add any additional rows",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify the rows"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
