from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest

#testrail('C83902')
@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicSimpleQuota_verifyDeleteQuotaHittingCancelButton",  # report_relative_location
                               "test_logic_simpleQuota_deleteQuota",  # report_file_name_prefix
                               "Verify deleting Quota on hitting Cancel button ",  # test_suite_title
                               ("This test applies validating Quota is deleted on hitting cancel button "
                                "To verify deleting Quota hitting Cancel button"),  # test_suite_description
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
@pytest.mark.C83902
@pytest.mark.Infobeans
@pytest.mark.IB
def test_logic_simpleQuota_errorMessage_notSelectingQuestion(create_survey):
    driver, mySurvey, report = create_survey
    answer_rows = ["Regularly", "Sometimes", "Occasionally"]

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify deleting Quota on hitting Cancel button.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "How often you do trekking?", answer_rows)
        mySurvey.myLogic.pushQuestionToStack("How often you do trekking?")

        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_Quota()
        mySurvey.myLogic.quotaSetupWizardwithoutSelectingAnswerChecklist("simple",1,1)
        ex = mySurvey.myLogic.verifyQuotaStatus("Off")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify deleting Quota on hitting Cancel button.",
                                "checks to verify deleting Quota on hitting Cancel button.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)

        assert ex, "Failed to verify Quota status OFF"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

