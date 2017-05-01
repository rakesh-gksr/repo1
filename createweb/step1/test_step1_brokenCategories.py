from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from smsdk.qafw.create.create_start_new import NewSurvey as create_new
import traceback
import pytest

@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestStep1BrokenCategories/",  # report_relative_location
                               "test_step1_brokenCategories",  # report_file_name_prefix
                               "Test for broken or missing elements in step 1",  # test_suite_title
                               ("Test to make sure Survey Title box, categories dropdown, and submit button are not intermittently gone "),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_step1_brokenCategories(create_survey):
    driver, mySurvey, report = create_survey

    #mySurvey.myTheme.setUp_Microdex()
    try:
        mySurvey.myCreate.click_new_survey()
        NewSurvey = create_new(driver)
        NewSurvey.create_survey_from_scratch()
        ex = mySurvey.myCreate.verify_step1_elements_present()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify step 1 elements loaded",
                                 "verifies that survey name input, category dropdown, and submit button loaded.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify step 1 elements loaded"
        for x in xrange(20):

            NewSurvey.create_survey_from_scratch()
            ex = mySurvey.myCreate.verify_step1_elements_present()
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify step 1 elements loaded, iteration " + str(x+1),
                                     "verifies that survey name input, category dropdown, and submit button loaded.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify step 1 elements loaded"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()