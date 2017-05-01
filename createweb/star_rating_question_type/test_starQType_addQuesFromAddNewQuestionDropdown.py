#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify adding star rating question from 'add a new question button' dropdown.

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
                               "TestStarQTypeAddQuesFromAddNewQuestionDropdown/",  # report_relative_location
                               "test_StarQType_addQuesFromAddNewQuestionDropdown",  # report_file_name_prefix
                               # test_suite_title
                               "verify adding star rating question from 'add a new question button' dropdown.",
                               "Test to verify adding star rating question from 'add a new question button' dropdown.",
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


@pytest.mark.Star_question
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C812361
def test_StarQType_addQuesFromAddNewQuestionDropdown(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "verify adding star rating question from 'add a new question button' dropdown.")
    try:
        mySurvey.myCreate.add_a_new_question("StarRating")
        ex = mySurvey.myQuestion.verify_question_in_edit_mode("question-emoji-rating")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify star rating question is added to live preview",
                                 "checks star rating question is added to live preview on clicking the Add button from"
                                 " Builder",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star rating question on preview."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
