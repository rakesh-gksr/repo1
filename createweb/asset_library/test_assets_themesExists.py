from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest
from test_assets_themes import build_survey_questions

pytestmark = pytest.mark.MT1


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAssetsThemesExist/",  # report_relative_location
                               "test_assets_themesExists",  # report_file_name_prefix
                               "test group themes tab under Themes accordion with enterprise accnt having feature flag",  # test_suite_title
                               ("Applies group theme created in previous test, "
                                " verifies theme applied."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    env_init('JoshGroup')
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_assets_themesExists(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "test group themes tab under Themes accordion with enterprise accnt having feature flag.")
    try:
        build_survey_questions(mySurvey, driver, report, True)
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
    try:
        mySurvey.myTheme.unfold_ThemeRegion()
        # time.sleep(1)
        ex = mySurvey.myTheme.clickGroupTheme("testCustomTheme1")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Apply testCustomTheme1 from group",
                                 "Open the theme accordion and select the testCustomTheme1",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to apply testCustomTheme1 theme from group"
        ex = mySurvey.myTheme.verifyThemeApplied("testCustomGroupTheme1")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify testCustomTheme1 Theme",
                                 "Compares current theme with values of what the theme should have",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify testCustomTheme1 theme " + str(ex)
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
