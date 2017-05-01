from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from smsdk.qafw.create.create_start import click_step_1_radio_button
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):

    report = reporting_wrapper("Create",  # report_feature_name
                               "TestMaxExistingSurveys",  # report_relative_location
                               "test_max_existingSurveys",  # report_file_name_prefix
                               "verify number of surveys display on copy survey dropdown on step 1",  # test_suite_title
                               ("This test creates a new survey"
                                " and then verifies max existing surveys on copy existing survey's dropdown"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    env_init('3k_survey_user')
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.skipif(True, reason="Skip this test cases because new step1 design does not display the pagination links")
def test_max_existingSurveys(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify number of surveys display on copy survey dropdown on step 1.")
    try:
        mySurvey.myCreate.click_new_survey()
        click_step_1_radio_button(driver, 2)
        oldCount = mySurvey.myCreate.get_copySurvey_dropdownCount()
        ex = oldCount>3000
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify maximum existing surveys",
                                 "checks to make sure dropdown contains max limit of existing surveys",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify maximum existing surveys."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
