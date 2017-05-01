#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Verify deleting rule by deleting source answer choice deletes branching logic and check transferring this survey
to account with branching FF.

"""

from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from dynamic_tests.dynamic_tests_config import adv_branch_transfer_survey
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAdvBranchTransferSurveyToAnotherFFAccount/",
                               # report_relative_location
                               "test_advBranch_transferSurveyToAnotherFFAccount",
                               # report_file_name_prefix
                               "Test branching rule by deleting source answer choice and tranfer survey "
                               "with branching FF",  # test_suite_title
                               ("verify deleting rule by deleting source answer choice deletes branching logic"
                                " and check transferring this survey to account with branching FF"),
                               # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    env_init("platinum_advanced_branching")
    import datetime
    import os
    testcasename = os.path.basename(__file__).split(".")[0] + "--" + datetime.datetime.now(). \
        strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename

adv_branch_transfer_survey = adv_branch_transfer_survey[pytest.config.option.domain[:3].upper()]

@pytest.mark.advBranch
@pytest.mark.IB
@pytest.mark.C252016
@pytest.mark.parametrize("test_info", adv_branch_transfer_survey, ids=[dict["AdvanceBranching"] for dict in
                                                                       adv_branch_transfer_survey])
def test_advBranch_transferSurveyToAnotherFFAccount(create_survey, test_info):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE,
                             "verify deleting rule by deleting source answer choice deletes branching logic and check"
                             " transferring this survey to account with branching FF")
    try:
        ex = mySurvey.myCreate.transfer_survey(test_info["tranfer_survey_id"], test_info["original_user_id"], "to")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify survey transferred",
                                 "Check the survey transferred correctly",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to transfer survey "
        url = mySurvey.myCreate.open_copied_survey(test_info["tranfer_survey_id"])
        driver.get(url)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Survey Loaded or recreated",
                                 "The survey has either been copied or recreated and is ready for the test",
                                 True,
                                 True,
                                 False,
                                 driver)
        mySurvey.myLogic.verifyAdvanceBranchingStatus(test_info["AdvanceBranching"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, test_info["verify_advBranch_step_title"],
                                 test_info["verify_advBranch_step_desc"],
                                 True,
                                 True,
                                 False,
                                 driver)
        assert ex, test_info["assertion_error"]
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
    finally:
        mySurvey.myCreate.transfer_survey(test_info["tranfer_survey_id"], test_info["original_user_id"], "from")