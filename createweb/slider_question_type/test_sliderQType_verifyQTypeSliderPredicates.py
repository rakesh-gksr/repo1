#!/usr/bin/env python
# -*- coding: utf-8 -*-

from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from dynamic_tests.dynamic_tests_config import slider_qtype_predicates, survey_dict
import traceback
import pytest


def pre_setup_survey(mySurvey, driver, report):
    survey_title = mySurvey.myCreate.get_survey_title()
    survey_info = survey_dict[pytest.config.option.domain[:3].upper()]["slider_qtype_adv_branch"]
    new_survey_id = mySurvey.myCreate.copy_exiting_survey_via_svysvc(survey_info["survey_id"],
                                                          survey_info["user_id"],
                                                          survey_title +
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
                               "TestSliderQTypeVerifyQTypeSliderPredicates/",
                               # report_relative_location
                               "test_sliderQType_verifyQTypeSliderPredicates",
                               # report_file_name_prefix
                               "Verify hiding and showing slider question on branching action condition",
                               # test_suite_title
                               ("This test suite adds show and hide slider question predicates in condition menu "
                                "and select diff actions for both and verify "
                                "that they works as expected in Preview & Test."),
                               # test_suite_description
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


@pytest.mark.slider_question
@pytest.mark.IB
@pytest.mark.C284514
@pytest.mark.parametrize("test_info", slider_qtype_predicates,
                         ids=[dict["predicate_label"] for dict in slider_qtype_predicates])
def test_sliderQType_verifyQTypeSliderPredicates(create_survey, test_info):
    """
        Description :

            This is parametrized test method. This test case adds different predicates in condition menu
            and select different actions for each predicate. And it verifies that the page logic rule is
            applied by preview & test window.

        Args:
            create_survey: fixture to create new survey
            test_info: dictionary (contains information of branching rules and verifying branching
            parameters for the test case )
                {
                "predicate_label": string,
                "branching_rule": dictionary,
                "rule_params": dictionary,
                }

        """

    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, dict["predicate_label"])
    try:
        rule_params = test_info["rule_params"]
        pre_setup_survey(mySurvey, driver, report)
        # code to add advance branching logic
        driver.refresh()
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
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Advanced Branching - "
                                 + test_info["predicate_label"],
                                 "verifies current advanced branching ruleset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify advanced branching - " + test_info["predicate_label"]
        mySurvey.myDesign.return_from_preview_window()

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()