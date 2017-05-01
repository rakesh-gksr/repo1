from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestMaxLargeSurvey/",  # report_relative_location
                               "test_max_largeSurvey",  # report_file_name_prefix
                               "Test large survey page and lack of bananas",  # test_suite_title
                               ("Verifies CREATE-5072."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.serial
def test_max_largeSurvey(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test Large Survey.")
    try:
        driver.get("https://www.monkeytest1.com/create/?sm=YwWx8ACFGjLeSHVODAHj8hNJnWLBcLPj51CuwFQZd70_3D")
        ex = mySurvey.myCreate.check_bananas()
        ex = not ex
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Survey does not contain bananas",
                                 "checks that oh bananas error is not present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify lack of bananas."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
