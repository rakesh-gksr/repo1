from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestMaxLogo/",  # report_relative_location
                               "test_max_logo",  # report_file_name_prefix
                               "Size of images uploaded logo",  # test_suite_title
                               ("This test adds a logo exactly 1MB in size "
                                " and then checks to make sure image over this limit results in an error."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_max_logo(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, " size of images uploaded logo.")
    try:
        mySurvey.myDesign.click_add_logo()
        mySurvey.myDesign.click_upload_logo("1MB_test_logo.jpg")
        ex = True if mySurvey.myDesign.check_if_logo_exist() is not None else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify logo uploaded successfully",
                                 "checks to make sure that 1MB logo appears in survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify max limit logo."
        mySurvey.myOptions.click_remove_logo_by_accordion()
        mySurvey.myDesign.click_add_logo()
        ex = True if mySurvey.myDesign.click_upload_logo("too_big_logo.jpg") == "size_except" else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify error of logo",
                                 "checks to make sure that logo that is too large results in an error",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify logo error exceeding max size."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
