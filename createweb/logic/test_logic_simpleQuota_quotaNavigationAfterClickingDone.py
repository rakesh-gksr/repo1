from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest

__author__ = 'rajat'

#testrail('C83904')
@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicQuotaNavigation/",  # report_relative_location
                               "test_logic_QuotaNavigationAfterClickingDone",  # report_file_name_prefix
                               "verify navigation after clicking done button ",  # test_suite_title
                               ("This test applies a simple quota navigation"
                                "To verify navigation after clicking done button"),  # test_suite_description
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
@pytest.mark.C83904
@pytest.mark.Infobeans
@pytest.mark.IB
def test_logic_simpleQuota_quotaNavigationAfterClickingDone(create_survey):
    driver, mySurvey, report = create_survey
    answer_rows = ["Regularly","Sometimes", "Occasionally"]

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify navigation after clicking done button.")
    try:
        mySurvey.myBank.searchForQuestion(mySurvey.survey_id, "How often you travel?", answer_rows)
        mySurvey.myLogic.pushQuestionToStack("How often you travel?")

        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_Quota()
        mySurvey.myLogic.quotaSetupWizard("simple", 1, 1, [1])
        mySurvey.myLogic.click_QuotaDone()
        ex = mySurvey.myLogic.verifyQuotaStatus("On")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify navigation after clicking done button",
                                 "checks to verify navigation after clicking done button.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)

        assert ex, "Failed to verify Quota Status ON"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

