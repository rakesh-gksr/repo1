from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicSinglePageBlock/",  # report_relative_location
                               "test_logic_singlePageBlock",  # report_file_name_prefix
                               # test_suite_title
                               "Verify question logic within a single page block",
                               ("This test adds 8 pages with questions. "
                                "Test verifies you can't add logic within single page block"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename

def _setup_questions(mySurvey, driver, report):
    survey_title = mySurvey.myCreate.get_survey_title()
    new_survey_id = mySurvey.myCreate.copy_exiting_survey_via_svysvc("130473859",
                                                          "58310199",
                                                          survey_title + " Copied via svysvc")
    url = mySurvey.myCreate.open_copied_survey(new_survey_id['survey_id'])
    driver.get(url)
    report.add_report_record(ReportMessageTypes.TEST_STEP,
                             "Survey Loaded or recreated",
                             "The survey has either been copied or recreated and is ready for the test",
                             True,
                             True,
                             False,
                             driver)

def test_logic_singlePageBlock(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify logic disabled within single page block.")
    try:
        _setup_questions(mySurvey, driver, report)
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_blockRandomizationButton()
        mySurvey.myLogic.click_blockRandom_newBlock()
        mySurvey.myLogic.addSequentialBlocks([1])
        mySurvey.myLogic.addSequentialBlocks([2, 3, 4, 5])
        mySurvey.myLogic.addSequentialBlocks([6, 7, 8])
        mySurvey.myLogic.blockRandomDone()
        mySurvey.myLogic.click_blockRandomizationButton()
        ex = mySurvey.myLogic.singlePageBLockLogicDisabled(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Attempts to add logic within a single page block",
                                 "verifies adding logic within a single page block is disabled.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify disabled logic within a single page block"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
