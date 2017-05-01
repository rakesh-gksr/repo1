#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify adding slider question from clicking on 'add a new question button' and then switch to slider.

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
                               "TestSliderQTypeAddQuesFromAddANewQuesButton/",  # report_relative_location
                               "test_sliderQType_addQuesFromAddANewQuesButton",  # report_file_name_prefix
                               # test_suite_title
                               ("verify adding slider question from clicking on 'add a new question button' and then "
                                "switch to slider"),
                               ("Test to verify adding slider question from clicking on 'add a new question button'"
                                " and then switch to slider"),  # test_suite_description
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
@pytest.mark.C284100
def test_sliderQType_addQuesFromAddANewQuesButton(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "verify adding slider question from clicking on 'add a new question button' and then switch to slider")
    try:
        mySurvey.myQuestion.click_add_new_question()
        ex = mySurvey.myQuestion.verify_question_in_edit_mode()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Multiple Choice question",
                                 "checks multiple choice question is added",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify multiple choice question is added."
        mySurvey.myQuestion.changeQType("Slider")
        ex = mySurvey.myQuestion.verify_question_in_edit_mode('question-open-ended-single', 'slider')
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Type Switched to Slider Question",
                                 "Verifies that question type switched to Slider",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question type switched to Slider."
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question is updated to Slider question",
                                 "checks that question is updated to Slider question.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question is updated to slider question."
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Slider question Add to Live Preview",
                                 "Verifies that Slider question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Slider question added to live preview."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
