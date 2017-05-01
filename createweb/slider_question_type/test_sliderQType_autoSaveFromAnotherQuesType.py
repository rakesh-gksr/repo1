#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify autosaving slider question from clicking on another question on the survey page.

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
                               "TestSliderQTypeAutoSaveFromAnotherQuesType/",  # report_relative_location
                               "test_sliderQType_autoSaveFromAnotherQuesType",  # report_file_name_prefix
                               # test_suite_title
                               ("verify autosaving slider question from clicking on another question on the survey "
                                "page"),
                               ("Test to verify autosaving slider question from clicking on another question on the "
                                "survey page"),  # test_suite_description
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


@pytest.mark.slider_quesiton
@pytest.mark.IB
@pytest.mark.C284102
def test_sliderQType_autoSaveFromAnotherQuesType(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "verify user can't add any additional rows")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myDesign.click_addPageTitle("Page 1", "This is test page 1")
        mySurvey.myQuestion.generate_single_textbox_question(mySurvey.survey_id, page_num, "Single Textbox", 1, False)
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.click_add_new_question()
        # code to verify that slider question type automatically saved
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider auto save",
                                 "Verified that slider question type automatically saved.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify slider question type automatically saved."
        ex = mySurvey.myQuestion.verify_question_in_edit_mode()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Multiple Choice Question Open In Edit Mode",
                                 "Verified that multiple choice question opened in edit mode",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify multiple choice question opened in edit mode."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
