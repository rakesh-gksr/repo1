#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
verify changing scale syncs with rating labels

"""

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
                               "TestStarQTypeVerifyChangingScaleSyncs/",  # report_relative_location
                               "test_starQType_verifyChangingScaleSyncs",  # report_file_name_prefix
                               # test_suite_title
                               "verify changing scale syncs with rating labels",
                               "Test to verify changing scale syncs with rating labels",  # test_suite_description
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
@pytest.mark.C831345
def test_starQType_verifyChangingScaleSyncs(create_survey):
    driver, mySurvey, report = create_survey
    driver.maximize_window()
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "verify changing scale syncs with rating labels.")
    try:
        mySurvey.myBuilder.click_star_rating_add_button()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        ex = mySurvey.myQuestion.change_star_rating_question_scale("2")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that star question scale",
                                 "checks to make sure that star question scale changed to 2.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star question scale changed to 2"
        ex = mySurvey.myQuestion.change_star_rating_question_shape("heart")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify that star question shape",
                                 "checks to make sure that star question shape changed to heart.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify star question shape changed to heart"
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that star question is saved",
                                 "checks to make sure that star question is saved with all required fields.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify saving of star question"
        ex = Spage.verify_star_elements(driver, 1, 2, "heart")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify moved question shows 2 heart",
                                 "checks to make sure that copied star question is showing 2 hearts",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify copied star question is showing 2 hearts"
        shape_list = ["heart", "thumb", "smiley", "star", "heart", "thumb", "smiley", "star"]
        for i in range(3, 11):
            mySurvey.myQuestion.click_on_question_to_edit(1)
            ex = mySurvey.myQuestion.change_star_rating_question_scale(str(i))
            report.add_report_record(ReportMessageTypes.TEST_STEP,
                                     "Verify that star question scale",
                                     "checks to make sure that star question scale changed to " + str(i),
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify star question scale changed to " + str(i)
            ex = mySurvey.myQuestion.change_star_rating_question_shape(shape_list[i-3])
            report.add_report_record(ReportMessageTypes.TEST_STEP,
                                     "Verify that star question shape",
                                     "checks to make sure that star question shape changed to " + shape_list[i-3],
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify star question shape changed to " + shape_list[i-3]
            mySurvey.myQuestion.click_question_save_from_edit_tab()
            ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that star question is saved",
                                     "checks to make sure that star question is saved with all required fields.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify saving of star question"
            ex = Spage.verify_star_elements(driver, 1, i, shape_list[i-3])
            report.add_report_record(ReportMessageTypes.TEST_STEP,
                                     "Verify moved question shows "+str(i)+" heart",
                                     "checks to make sure that copied star question is showing "+str(i)+" hearts",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify copied star question is showing "+str(i)+" hearts"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
