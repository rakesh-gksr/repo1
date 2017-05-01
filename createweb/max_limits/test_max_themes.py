from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestMaxThemes/",  # report_relative_location
                               "test_max_themes",  # report_file_name_prefix
                               "verify adding max characters for theme name",  # test_suite_title
                               ("This test adds both max and one character over max to custom theme name"
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


def test_max_themeName(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify adding max characters for theme name.")
    try:
        mySurvey.myTheme.unfold_ThemeRegion()
        title = mySurvey.myLogic.RNG(50)
        ex = mySurvey.myTheme.createNewCustomTheme(title)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Create custom Theme length 50 chars",
                                 "Open the theme accordion and create new custom theme",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to create new custom theme with max limit chars"
        ex = mySurvey.myTheme.clickCustomTheme(title)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click on new theme",
                                 "Returns true if we are able to click on theme with this name",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify max char theme name"
        mySurvey.myTheme.deleteTheme(title)
        title = mySurvey.myLogic.RNG(51)
        ex = mySurvey.myTheme.createNewCustomTheme(title)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Create custom Theme length 51 chars",
                                 "Open the theme accordion and create new custom theme",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to create new custom theme over max limit"
        ex = mySurvey.myTheme.clickCustomTheme(title[:-1])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click on new theme",
                                 "Returns true if we are able to click on theme with this name",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify over max char theme name"
        mySurvey.myTheme.deleteTheme(title[:-1])
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
