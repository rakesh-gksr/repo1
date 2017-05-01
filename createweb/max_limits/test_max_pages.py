from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestMaxPages/",  # report_relative_location
                               "test_max_pages",  # report_file_name_prefix
                               "Test Maximum Limit of Pages",  # test_suite_title
                               ("This test adds 400 Pages "
                                " and then checks to make sure survey throws error for adding one more page (going over limit)."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_max_pages(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "number of pages for a survey.")
    try:
        survey_title = mySurvey.myCreate.get_survey_title()
        new_survey_id = mySurvey.myCreate.copy_exiting_survey_via_svysvc("100709075", "57725445", survey_title + " Copied via svysvc")
        url = mySurvey.myCreate.open_copied_survey(new_survey_id['survey_id'])
        driver.get(url)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Survey Loaded or recreated",
                                 "The survey has either been copied or recreated and is ready for the test",
                                 True,
                                 True,
                                 False,
                                 driver)
        ex = True if mySurvey.myCreate.get_num_pages() == 400 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify 400 Pages added",
                                 "checks to make sure that we 400 Pages are in the survey via svysvc",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify page limit added."
        mySurvey.myDesign.scroll_to_bottom()
        mySurvey.myBuilder.click_NewPageAddButton()
        ex = mySurvey.myCreate.verifyMaxPagesError()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify limit error notice",
                                 "checks to make sure that user notification of max limit appears",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify max limit."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
