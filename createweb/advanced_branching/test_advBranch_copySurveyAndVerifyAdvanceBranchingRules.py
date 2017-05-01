#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verifies that the advance branching logic is deleted by deleting source answer choice deletes branching logic and
check copying this survey to account without branching FF.

"""

from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from dynamic_tests.dynamic_tests_config import adv_branch_copy_survey
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAdvBranchCopySurveyAndVerifyAdvanceBranchingRules/",
                               # report_relative_location
                               "test_advBranch_copySurveyAndVerifyAdvanceBranchingRules",
                               # report_file_name_prefix
                               "Test branching rule is deleted by deleting source answer choice and copy survey "
                               "without branching FF",  # test_suite_title
                               ("It verifies that the advance branching logic is deleted by deleting source answer "
                                "choice deletes branching logic and check copying this survey to account without "
                                "branching FF"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    env_init("platinum_default")
    import datetime
    import os
    testcasename = os.path.basename(__file__).split(".")[0] + "--" + datetime.datetime.now().\
        strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename

adv_branch_copy_survey = adv_branch_copy_survey[pytest.config.option.domain[:3].upper()]


@pytest.mark.advBranch
@pytest.mark.IB
@pytest.mark.C252015
@pytest.mark.parametrize("test_info", adv_branch_copy_survey, ids=[dict["AdvanceBranching"] for dict in
                                                                   adv_branch_copy_survey])
def test_advBranch_copySurveyAndVerifyAdvanceBranchingRules(create_survey, test_info):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE,
                             "that the advance branching logic is deleted by deleting source answer choice deletes"
                             " branching logic and check copying this survey to account without branching FF")
    try:
        new_survey_id = mySurvey.myCreate.copy_exiting_survey_via_svysvc(test_info["copy_survey_id"],
                                                              test_info["original_user_id"],
                                                              test_info["survey_title"]+"_Create_via_svysrv")
        url = mySurvey.myCreate.open_copied_survey(new_survey_id["survey_id"])
        driver.get(url)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Survey Loaded or recreated",
                                 "The survey has either been copied or recreated and is ready for the test",
                                 True,
                                 True,
                                 False,
                                 driver)
        ex = mySurvey.myLogic.verifyAdvanceBranchingStatus(test_info["AdvanceBranching"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, test_info["verify_advBranch_step_title"],
                                 test_info["verify_advBranch_step_desc"],
                                 True,
                                 True,
                                 False,
                                 driver)
        assert ex, test_info["error_message"]
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
