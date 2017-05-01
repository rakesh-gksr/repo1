from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest

@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicComboQuota/",  # report_relative_location
                               "test_logic_comboQuota_delete_group_equations",  # report_file_name_prefix
                               "verify deleting group equation on combination quota logic",  # test_suite_title
                               ("This test verifies if delete group equation "
                                " works for combo quota logic."),  # test_suite_description
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
@pytest.mark.combo_quota
@pytest.mark.C83896
@pytest.mark.IB
def test_logic_comboQuota_delete_group_equations(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify applying page quota logic equation.")
    try:
        # set survey question and option used for test case
        survey_questions = [
            [
                "How noisy is this neighborhood?",
                [
                    "Very Noisy",
                    "Silent",
                ],
            ],
            [
                "In a typical month, about how much money, in U.S. dollars, do you spend on your cable service?",
                [
                    "upto 10$",
                    "more than 10$",
                ],
            ],
        ]

        for question, answer_rows in survey_questions:
            mySurvey.myBank.searchForQuestion(mySurvey.survey_id, question, answer_rows)
            mySurvey.myLogic.pushQuestionToStack(question)

        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_Quota()
        # setup Comboinational Quota - Group 1 for question 1 and 2
        mySurvey.myLogic.quotaSetupWizardComboWithGroup([1, 1], [1, 2], [1, 1])

        # add group 2 for question 1
        mySurvey.myLogic.addAnotherAnswerGroup(1)
        # function call to select the answers for quota group
        mySurvey.myLogic.selectAnswersForGroup([2])
        ex = mySurvey.myLogic.verifyAddAnswerGroup(False, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that Add answer group button do not appear for question 1.",
                                 "checks to make sure that the Add answer Group button do not appear for question 1.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify absence of Add answer group button for question 1."

        # add group 2 for question 2
        mySurvey.myLogic.addAnotherAnswerGroup(2)
        # function call to select the answers for quota group
        mySurvey.myLogic.selectAnswersForGroup([2])
        ex = mySurvey.myLogic.verifyAddAnswerGroup(False, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that Add answer group button do not appear for question 2",
                                 "checks to make sure that the Add answer Group button do not appear for question 2.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify absence of Add answer group button for question 2"

        mySurvey.myLogic.click_comboQuota_AssignValues()
        # set the group equation
        mySurvey.myLogic.setup_comboQuota_SetAnswerGroups([1, 2], [1, 1])

        ex = mySurvey.myLogic.checkQuotaIcon(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page quota icon appears for question 2",
                                 "checks to make sure that the page quota icon appears for question 2.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of page quota icon for question 2."

        mySurvey.myLogic.click_comboQuota_SelectEquationGroup()
        mySurvey.myLogic.click_comboQuota_DeleteEquationGroup()

        ex = mySurvey.myLogic.check_comboQuota_AddEquationGroupVisible()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that add equation group button is visible",
                                 "checks to make sure that Add Equation button appears.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of Add Equation button"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
