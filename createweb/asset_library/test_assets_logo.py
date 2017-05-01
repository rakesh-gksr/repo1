from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest
pytestmark = pytest.mark.MT1


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAssetLogo/",  # report_relative_location
                               "test_asset_logo",  # report_file_name_prefix
                               "Enterprise: Test each account in a enterprise group can use image assets from library",  # test_suite_title
                               ("Adds an logo question using library assets."
                                " and verifies that image were successfully added from assets."),  # test_suite_description
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


def test_asset_logo(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Enterprise: Test each account in a enterprise group can use image assets from library.")
    try:
        mySurvey.myDesign.click_add_logo()
        mySurvey.myDesign.click_upload_logo_fromLib(1)
        ex = mySurvey.myDesign.verify_logo_assetLib()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify logo source",
                                 "checks for logo source containing assets directory",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify logo source"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test ",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
