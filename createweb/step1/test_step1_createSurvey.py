from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest
from smsdk.qafw.create.create_start_new import NewSurvey


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestStep1CreateSurvey/",  # report_relative_location
                               "test_step1_CreateSurvey",  # report_file_name_prefix
                               "Test creating new survey via step1",  # test_suite_title
                               ("Test to make sure step 1 survey creation functions "),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_step1_createSurvey(create_survey):
    driver, mySurvey, report = create_survey

    #mySurvey.myTheme.setUp_Microdex()
    try:
        mySurvey.myCreate.click_new_survey()
        step1 = NewSurvey(driver)
        step1.create_survey_from_scratch()
        surveyTitle = 'test_' + mySurvey.myLogic.RNG(245)
        step1.enter_survey_title(surveyTitle)
        step1.click_lets_go_new()
        ex = mySurvey.myCreate.verify_survey_title(surveyTitle)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify step 1 Survey Creation",
                                     "verifies that survey title matches step 1 input.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
        assert ex, "Failed to verify step 1 survey Creations"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()