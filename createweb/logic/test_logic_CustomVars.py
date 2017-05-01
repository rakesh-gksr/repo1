from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicCustomVars/",  # report_relative_location
                               "test_logic_customVars",  # report_file_name_prefix
                               "verify applying two custom variables (with and without label)",  # test_suite_title
                               ("This test applies two custom variables "
                                " and verifies that the collector page url "
                                " contains the custom variables."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_logic_customVars_with_label(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify applying two custom variables with labels.")
    try:
        mySurvey.myLogic.unfold_LogicRegion()
        # time.sleep(1)
        mySurvey.myLogic.click_CustomVarsButton()
        # time.sleep(5)
        mySurvey.myLogic.enter_CustomVarName()
        mySurvey.myLogic.enter_CustomVarLabel()
        mySurvey.myLogic.click_CustomVarNextButton()
        mySurvey.myLogic.click_CustomVarNewButton()
        mySurvey.myLogic.enter_CustomVarName()
        mySurvey.myLogic.enter_CustomVarLabel()
        mySurvey.myLogic.click_CustomVarNextButton()
        mySurvey.myDesign.clickNextButton()
        mySurvey.myDesign.select_collector_type("weblink")
        ex = mySurvey.myLogic.verifyCustomVarsUrl()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "collector page url verification",
                                 "Verifies that custom variables appear in the collector page url",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify collector page url"
        mySurvey.myDesign.returnToDesignPage()
        mySurvey.myLogic.deleteAllCustomVars()
        mySurvey.myLogic.wipeCustomVarsLocal()
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_logic_customVars_without_label(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify applying two custom variables without labels.")
    try:
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_CustomVarsButton()
        mySurvey.myLogic.enter_CustomVarName()
        mySurvey.myLogic.click_CustomVarNextButton()
        mySurvey.myLogic.click_CustomVarNewButton()
        mySurvey.myLogic.enter_CustomVarName()
        mySurvey.myLogic.click_CustomVarNextButton()
        mySurvey.myDesign.clickNextButton()
        mySurvey.myDesign.select_collector_type("weblink")
        ex = mySurvey.myLogic.verifyCustomVarsUrl()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "collector page url verification",
                                 "Verifies that custom variables appear in the collector page url",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify collector page url"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
