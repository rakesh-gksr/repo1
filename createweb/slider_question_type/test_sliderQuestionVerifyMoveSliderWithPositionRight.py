#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify moving slider with position to the right.

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
                               "TestSliderQuestionVerifyMoveSliderWithPositionRight/",  # report_relative_location
                               "test_sliderQuestionVerifyMoveSliderWithPositionRight",  # report_file_name_prefix
                               # test_suite_title
                               "verify moving slider with position to the right",
                               "Test to verify moving slider with position to the right",  # test_suite_description
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
@pytest.mark.C286972
def test_sliderQuestionVerifyMoveSliderWithPositionRight(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify moving slider with position to the right")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title("Your expectation?")
        mySurvey.myQuestion.click_question_options_tab()
        mySurvey.myQuestion.checkSliderScaleCheckbox()
        ex = mySurvey.myQuestion.selectSliderStartPosition('right')
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that slider question right position selected",
                                 "checks to make sure that slider question right is selected.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify slider question right is selected"
        ex = mySurvey.myQuestion.click_question_save_from_options_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that slider question is saved with slider position in right",
                                 "checks to make sure that slider question is saved with slider position in right.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify saving slider question"
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider question Add to Live Preview",
                                 "Verifies that Slider question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Slider question added to live preview."

        mySurvey.myBuilder.click_SingleTextboxAddButton()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Single Textbox question Add to Live Preview",
                                 "Verifies that Single Textbox question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Single Textbox question added to live preview."
        mySurvey.myQuestion.click_on_question_to_edit()
        mySurvey.myQuestion.click_question_move_tab()
        mySurvey.myLogic.moveQuestion(1, 2)
        mySurvey.myQuestion.click_on_question_to_edit(2)
        ex = mySurvey.myQuestion.verify_slider_position("right")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "verify moving slider question with slider positioned at right",
                                 "checks to make sure that slider question is saved with slider position in "
                                 "right.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify slider question after moving."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
