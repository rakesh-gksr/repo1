#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify default slider position is left.

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
                               "TestSliderQuestionVerifyDefaultSliderPositionToLeft/",  # report_relative_location
                               "test_sliderQuestionVerifyDefaultSliderPositionToLeft",  # report_file_name_prefix
                               "verify default slider position is left ",  # test_suite_title
                               "Test verify default slider position is left",  # test_suite_description
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
@pytest.mark.C284115
@pytest.mark.IB
def test_sliderQuestionVerifyDefaultSliderPositionToLeft(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify default slider position is left")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title("Your expectation?")
        mySurvey.myQuestion.click_question_options_tab()
        mySurvey.myQuestion.checkSliderScaleCheckbox()
        ex = mySurvey.myQuestion.verify_slider_position("left")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that slider question is saved with default position as left",
                                 "checks to make sure that slider question is saved with slider position in left.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify saving of slider question"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.slider_question
@pytest.mark.C1055371
@pytest.mark.IB
def test_sliderQuestionVerifyDefaultSliderPositionToLeftCheck(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify default slider checkbox not ticked")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myQuestion.click_on_question_to_edit()
        mySurvey.myQuestion.click_question_options_tab()
        ex = not (mySurvey.myQuestion.get_slider_scale_option_status())
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that slider question is saved with default position",
                                 "checks to make sure that slider question is saved with Adjust scale option not ticked.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Adjust scale option not ticked"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
