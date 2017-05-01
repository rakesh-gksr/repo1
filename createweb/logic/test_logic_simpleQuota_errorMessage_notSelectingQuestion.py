from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest

__author__ = 'rajat'

#testrail('C83898')
@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicSimpleQuota_NotselectingQuestionAndPage_ErrorMessage/",  # report_relative_location
                               "test_logic_simpleQuota_ErrorMessage",  # report_file_name_prefix
                               "verify error message validating when not selecting Question and Page ",  # test_suite_title
                               ("This test applies a validating error message "
                                "To verify error messages on quota by not selecting page and question"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import time
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename

@pytest.mark.quota
@pytest.mark.C83898
@pytest.mark.Infobeans
@pytest.mark.IB
def test_logic_simpleQuota_errorMessage_notSelectingQuestion(create_survey):
    driver, mySurvey, report = create_survey
    answer_rows = ["Regularly", "Sometimes", "Occasionally"]

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify error message when not selecting question for quota.")
    try:
        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "How often you do trekking?", answer_rows)
        mySurvey.myLogic.pushQuestionToStack("How often you travel?")

        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_Quota()
        mySurvey.myLogic.checkQuotaIcon(1)
        mySurvey.myLogic.quotaSetupWizardwithoutSelectingQuestion("simple")
        ex = mySurvey.myLogic.verifyErrorMessageForQuota("Please select a question.")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify error message when not selecting question for quota.",
                                "checks to verify error message when not selecting question for quota.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)

        assert ex, "Error message got validated."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

