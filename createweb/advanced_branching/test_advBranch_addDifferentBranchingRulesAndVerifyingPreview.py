#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is common test method. It verifies the advanced branching functionality for different types of page logic
and action options.

1. It adds the page logic on page 1 and verifies that the page logic rule is applied by preview & test window.

"""

from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from dynamic_tests.dynamic_tests_config import adv_branch_test_info
import traceback
import pytest

survey_id_dict= {
    "single_textbox": "130246718"
}


def pre_setup_survey(mySurvey, driver, report, survey_type):
    survey_title = mySurvey.myCreate.get_survey_title()
    new_survey_id = mySurvey.myCreate.copy_exiting_survey_via_svysvc(survey_id_dict[survey_type], "58237384", survey_title +
                                                          " Copied via svysvc")
    url = mySurvey.myCreate.open_copied_survey(new_survey_id["survey_id"])
    driver.get(url)
    report.add_report_record(ReportMessageTypes.TEST_STEP, "Survey Loaded or recreated",
                             "The survey has either been copied or recreated and is ready for the test",
                             True,
                             True,
                             False,
                             driver)


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAdvBranch_addDifferentBranchingRulesAndVerifyingPreview/",
                               # report_relative_location
                               "test_advBranch_addDifferentBranchingRulesAndVerifyingPreview",
                               # report_file_name_prefix
                               "Test different advanced branching rules and verify that they works as "
                               "expected in Preview & Test.",
                               # test_suite_title
                               ("This test suite adds different different advanced branching rules and verify "
                                "that they works as expected in Preview & Test."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    env_init("platinum_advanced_branching")
    import datetime
    import os
    testcasename = os.path.basename(__file__).split(".")[0] + "--" + datetime.datetime.now().strftime("%I:%M%p %b %d,"
                                                                                                      " %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.advBranch
@pytest.mark.IB
@pytest.mark.C246587
@pytest.mark.C246588
@pytest.mark.C246568
@pytest.mark.C246582
@pytest.mark.C246583
@pytest.mark.C246584
@pytest.mark.parametrize("test_info", adv_branch_test_info,
                         ids=[dict["test_case_title"] for dict in adv_branch_test_info])
def test_advBranch_addDifferentBranchingRulesAndVerifyingPreview(create_survey, test_info):
    """
     Description :

        This is parametrized test method. It verifies the advanced branching functionality for different types of
        page logic and action options. And it verifies that the page logic rule is applied by preview & test window.
        This test method covers following TestRail Test Cases

        C246587 - Test adding other branching action Hide question
        C246588 - Test adding other branching action show question
        C246568 - Test adding branching condition "AND"
        C246582 - Test adding branching condition "OR"
        C246583 - Test adding branching action End Survey
        C246584 - Test adding branching action Disqualify respondent
        
    Args:
        create_survey: fixture to create new survey
        test_info: dictionary (contains information of test case title, branching rules and verifying branching
        parameters for the test case )
                           {
                               "test_case_title": string,
                               "jira_id": string,
                               "rule_params": dictionary,
                               "branching_rule": list
                               "verify_advBranch_step_title": string,
                               "verify_advBranch_step_desc": string,
                               "error_message": string
                           }

    """

    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, test_info["test_case_title"])
    try:
        rule_params = test_info["rule_params"]
        pre_setup_survey(mySurvey, driver, report, "single_textbox")
        # code to add advance branching logic
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule(test_info["branching_rule"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Advanced Logic",
                                 "Verifies advanced logic window closed and logic saved.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to save advanced logic"

        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks preview button, in order to verify theme in preview window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        mySurvey.myDesign.click_off_preview_warning()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.switch_to_preview_iframe()
        ex = mySurvey.myLogic.verify_advanced_branching(rule_params["qType"],
                                                        rule_params["qNum"],
                                                        rule_params["inputList"],
                                                        rule_params["logicType"],
                                                        rule_params["logicOptions"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, test_info["verify_advBranch_step_title"],
                                 test_info["verify_advBranch_step_desc"],
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, test_info["error_message"]
        mySurvey.myDesign.return_from_preview_window()

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()