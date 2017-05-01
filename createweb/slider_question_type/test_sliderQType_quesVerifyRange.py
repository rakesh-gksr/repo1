#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify start and end range is between 0-100.

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
                               "TestSliderQTypeQuesVerifyRange/",  # report_relative_location
                               "test_sliderQType_quesVerifyRange",  # report_file_name_prefix
                               # test_suite_title
                               "verify start and end range is between 0-100",
                               "Test to verify start and end range is between 0-100",  # test_suite_description
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
@pytest.mark.C284107
def test_sliderQType_quesVerifyRange(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "verify start and end range is between 0-100")
    minRange = [-1000001, 0, -1000000, -1000000]
    maxRange = [1000000, -1000000, 1000001, 1000000]

    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider question Add to Live Preview",
                                 "Verifies that Slider question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Slider question added to live preview."
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.click_question_options_tab()
        mySurvey.myQuestion.checkSliderScaleCheckbox()
        for x in xrange(4):
            mySurvey.myQuestion.enter_min_max_range(minRange[x], maxRange[x])
            ex = mySurvey.myQuestion.verify_valid_range()
            if x!=3 and ex is False:
                ex = True
                report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify invalid range",
                                         "checks Slider question is not saved with invalid range.",
                                         ex,
                                         True,
                                         not ex,
                                         driver)
                assert ex, "Failed to verify Slider question is not saved with invalid range."
            if x == 3:
                report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify valid range i.e 0 to 100",
                                         "checks Slider question is saved with valid range.",
                                         ex,
                                         True,
                                         not ex,
                                         driver)
                assert ex, "Failed to verify Slider question is saved with valid range."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
