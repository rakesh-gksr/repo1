#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verify transferring survey with star to another account.

"""

from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from dynamic_tests.dynamic_tests_config import survey_dict
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestStarQTypeTransferSurveyToAnotherAcc/",  # report_relative_location
                               "test_starQType_transferSurveyToAnotherAcc",  # report_file_name_prefix
                               # test_suite_title
                               "Verify transferring survey with star to another account.",
                               "Test to verify transferring survey with star to another account.",
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


@pytest.mark.star_question
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C812419
def test_starQType_transferSurveyToAnotherAcc(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify transferring survey with star to another account.")
    try:
        survey_info = survey_dict[pytest.config.option.domain[:3].upper()]["star_qtype_copy_transfer_survey"]

        ex = mySurvey.myCreate.transfer_survey(survey_info["survey_id"], survey_info["user_id"], "to")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify survey transferred",
                                 "Check the survey transferred correctly",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to transfer survey "
        url = mySurvey.myCreate.open_copied_survey(survey_info["survey_id"])
        driver.get(url)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Survey Loaded or recreated",
                                 "The survey has either been copied or recreated and is ready for the test",
                                 True,
                                 True,
                                 False,
                                 driver)
        mySurvey.myQuestion.click_on_question_to_edit()
        ex = mySurvey.myQuestion.verify_question_in_edit_mode("question-emoji-rating")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Star Question Exist In Survey",
                                 "Verifies that star question exist in survey.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star question exist in survey."
        ex = mySurvey.myQuestion.verifyQuestionTitleString(survey_info['star_qtn_title'])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Title",
                                 "Verifies that star question title matched.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star question title matched."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
    finally:
        mySurvey.myCreate.transfer_survey(survey_info["survey_id"], survey_info["user_id"], "from")
