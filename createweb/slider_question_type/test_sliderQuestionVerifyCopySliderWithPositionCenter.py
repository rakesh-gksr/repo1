#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify copying slider with position to the center.

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
                               "TestSliderQuestionVerifyCopySliderWithPositionCenter/",  # report_relative_location
                               "test_sliderQuestionVerifyCopySliderWithPositionCenter",  # report_file_name_prefix
                               # test_suite_title
                               "verify copying slider with position to the center",
                               "Test to verify copying slider with position to the center",  # test_suite_description
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
@pytest.mark.C286971
def test_sliderQuestionVerifyCopySliderWithPositionCenter(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify copying slider with position to the center")
    try:

        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title("Your expectation?")
        mySurvey.myQuestion.click_question_options_tab()
        mySurvey.myQuestion.checkSliderScaleCheckbox()
        mySurvey.myQuestion.selectSliderStartPosition('center')
        ex = mySurvey.myQuestion.click_question_save_from_options_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that slider question is saved with slider position in center",
                                 "checks to make sure that slider question is saved with slider position in center.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify saving of slider question"
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider question Add to Live Preview",
                                 "Verifies that Slider question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Slider question added to live preview."
        mySurvey.myQuestion.click_on_question_to_edit()
        mySurvey.myQuestion.click_question_copy_tab()
        ex = mySurvey.myLogic.copyQuestion(1, 1)
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myQuestion.click_question_options_tab()
        mySurvey.myQuestion.checkSliderScaleCheckbox()
        ex = mySurvey.myQuestion.verify_slider_position("center")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that copied question is saved with slider position in center",
                                 "checks to make sure that copied slider question is saved with slider position in "
                                 "center.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify position of copied slider question"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
