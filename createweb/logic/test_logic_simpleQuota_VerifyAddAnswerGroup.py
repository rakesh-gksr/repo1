
"""
Quota type : Simple quota
Test case for verifying add answer group logic
"""

from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest

__author__ = 'mangesh'

@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicSimpleQuota/",  # report_relative_location
                               "test_logic_simpleQuota_add_answer_group",  # report_file_name_prefix
                               "Verify add answer group status",  # test_suite_title
                               ("This test applies a simple page quota "
                                " to verify that Add answer group button appearance."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.quota
@pytest.mark.C83913
@pytest.mark.IB
def test_logic_simpleQuota_verifyAddAnswerGroup(create_survey):
    """
    Test case name : verify +Add Answer group if not all the answer options are selected in previous group
    Args:
    create_survey: fixture to create survey

    """
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify appearance of the Add answer group button.")
    try:
        # parameters that has to be passed for searchForQuestion function
        answers = ["Very noisy", "Somewhat noisy", "not at all"]
        # parameters that has to be passes for selectAnswersForGroup function
        answers_for_group = [2, 3]
        # Add multiple choice question
        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "How noisy is this neighborhood?", answers)
        mySurvey.myLogic.pushQuestionToStack("How noisy is this neighborhood?")

        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_Quota()
        mySurvey.myLogic.quotaSetupWizard("simple", 1, 1, [1])
        # function call to verify that Add Answer Group button is present or not
        ex = mySurvey.myLogic.verifyAddAnswerGroup()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that Add answer group button appears",
                                 "checks to make sure that the Add answer Group button appears.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of Add answer group button"
        # function call to add another answer group
        mySurvey.myLogic.addAnotherAnswerGroup(1)
        # function call to select the answers for quota group
        mySurvey.myLogic.selectAnswersForGroup(answers_for_group)
        ex = mySurvey.myLogic.verifyAddAnswerGroup(False)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that Add answer group button do not appear",
                                 "checks to make sure that the Add answer Group button do not appear.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify absence of Add answer group button"
        mySurvey.myLogic.click_QuotaDone()

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.quota
@pytest.mark.C83905
@pytest.mark.Infobeans
def test_logic_simpleQuota_verifyAddAnswerGroupWithAllAnswerSelected(create_survey):
    """
    Test case name : select all the answer options in a group and verify +Add answer group is not displayed

    Args:
    create_survey: fixture to create survey
    """
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify appearance of the Add answer group button")
    try:
        # parameters that has to be passed for searchForQuestion function
        answers = ["Very noisy", "Somewhat noisy", "not at all"]
        # Add multiple choice question
        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "How noisy is this neighborhood?", answers)
        mySurvey.myLogic.pushQuestionToStack("How noisy is this neighborhood?")

        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_Quota()
        mySurvey.myLogic.quotaSetupWizard("simple", 1, 1, [1, 2, 3])
        # call to function to verify that Add Answer Group button is present or not
        ex = mySurvey.myLogic.verifyAddAnswerGroup(False)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that Add answer group button do not appear",
                                 "checks to make sure that the Add answer Group button do not appear.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify absence of Add answer group button"
        mySurvey.myLogic.click_QuotaDone()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
