#!/usr/bin/env python
# -*- coding: utf-8 -*-

from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from smsdk.qafw.rpage import pyramidsurveypage as Spage
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestStarQTypeVerifyCopyingStarWithThumbShape/",  # report_relative_location
                               "test_starQType_verifyCopyingStarWithThumbShape",  # report_file_name_prefix
                               # test_suite_title
                               "verify copying star with thumb shape and 5 scale",
                               "Test to verify copying star with thumb shape and 5 scale",  # test_suite_description
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
@pytest.mark.C819966
def test_starQType_verifyCopyingStarWithThumbShape(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify copying star with thumb shape and 5 scale")
    try:
        # code to add star question to survey
        mySurvey.myBuilder.click_star_rating_add_button()
        mySurvey.myQuestion.enter_question_title('Rate SurveyMonkey services')
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify Save Star question type",
                                 "verifies that Star question type saved",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Star question type saved"
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Star question Add to Live Preview",
                                 "Verifies that Star question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Star question added to live preview."

        mySurvey.myQuestion.click_on_question_to_edit()
        ex = mySurvey.myQuestion.change_star_rating_question_scale("5")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that star question scale",
                                 "checks to make sure that star question scale changed to 5.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star question scale changed to 5"
        ex = mySurvey.myQuestion.change_star_rating_question_shape("thumb")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that star question shape",
                                 "checks to make sure that star question shape changed to Thumb.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star question shape changed to Thumb"
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify Save Star question type",
                                 "verifies that Star question type saved",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Star question type saved"
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify star question Add to Live Preview",
                                 "Verifies that star question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star question added to live preview."
        mySurvey.myQuestion.click_on_question_to_edit()
        mySurvey.myQuestion.click_question_copy_tab()
        mySurvey.myLogic.copyQuestion(1, 1)
        ex = Spage.verify_star_elements(driver, 2, 5, "thumb")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify copied question shows 5 thumbs",
                                 "checks to make sure that copied star question is showing 5 thumbs",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify copied star question is showing 5 thumbs"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
