from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestMaxCustomVar/",  # report_relative_location
                               "test_max_customVar",  # report_file_name_prefix
                               "verify adding max characters for custom variable label and custom variable name",  # test_suite_title
                               ("This test adds tests maximum characters for both name and label for custom vars"
                                " and then checks to make sure the maximum limit was not breached."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_max_customVarLabel(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify adding max characters for custom variable label.")
    try:
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_CustomVarsButton()
        mySurvey.myLogic.enter_CustomVarName()
        mySurvey.myLogic.enter_CustomVarLabel(mySurvey.myLogic.RNG(250))
        mySurvey.myLogic.click_CustomVarNextButton()
        mySurvey.myDesign.clickNextButton()
        mySurvey.myDesign.select_collector_type("weblink")
        ex = mySurvey.myLogic.verifyCustomVarsUrl("single")  # single variable test = True
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify maximum character limit for custom variable label",
                                 "checks to make sure that the variable was saved correctly.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify maximum characters for custom variable label."
        mySurvey.myDesign.click_designSurvey_tab()
        mySurvey.myLogic.click_CustomVarsButton()
        mySurvey.myLogic.click_CustomVarNewButton()
        mySurvey.myLogic.enter_CustomVarName()
        mySurvey.myLogic.enter_CustomVarLabel(mySurvey.myLogic.RNG(251))  # due to maxlength attribute only 250 get entered
        mySurvey.myLogic.click_CustomVarNextButton()
        mySurvey.myDesign.clickNextButton()
        # mySurvey.myDesign.select_collector_type("weblink")
        ex = mySurvey.myLogic.verifyCustomVarsUrl("double")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify maximum character limit for custom variable label",
                                 "checks to make sure that the variable was saved correctly and cuts off the 251st character.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify over maximum characters for custom variable label."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_max_customVarName(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify adding max characters for custom variable name.")
    try:
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_CustomVarsButton()
        mySurvey.myLogic.enter_CustomVarName(mySurvey.myLogic.RNG(25))
        mySurvey.myLogic.enter_CustomVarLabel()
        mySurvey.myLogic.click_CustomVarNextButton()
        mySurvey.myDesign.clickNextButton()
        mySurvey.myDesign.select_collector_type("weblink")
        ex = mySurvey.myLogic.verifyCustomVarsUrl("single")  # single variable test = True
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify maximum character limit for custom variable name",
                                 "checks to make sure that the variable was saved correctly.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify maximum characters for custom variable name."
        mySurvey.myDesign.click_designSurvey_tab()
        mySurvey.myLogic.click_CustomVarsButton()
        mySurvey.myLogic.click_CustomVarNewButton()
        mySurvey.myLogic.enter_CustomVarName(mySurvey.myLogic.RNG(26))  # due to maxlength attribute only 250 get entered
        mySurvey.myLogic.enter_CustomVarLabel()
        mySurvey.myLogic.click_CustomVarNextButton()
        mySurvey.myDesign.clickNextButton()
        mySurvey.myDesign.select_collector_type("weblink")
        ex = mySurvey.myLogic.verifyCustomVarsUrl("double")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify maximum character limit for custom variable name",
                                 "checks to make sure that the variable was saved correctly and cuts off the 26th character.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify over maximum characters for custom variable name."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
