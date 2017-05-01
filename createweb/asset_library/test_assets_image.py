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
                               "TestAssetImage/",  # report_relative_location
                               "test_asset_image",  # report_file_name_prefix
                               "Enterprise: add an image via library to image question",  # test_suite_title
                               ("Adds an image question using library assets."
                                " and verifies that images were successfully added from assets."),  # test_suite_description
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


def test_asset_image(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Enterprise: add an image via library to image question.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_ImageAddButton()
        mySurvey.myQuestion.enter_image_label("poi?", 1)
        mySurvey.myQuestion.enter_image_fromLib(2)
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_image_assetURL(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify image source",
                                 "checks for image source containing assets directory",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify image source"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test ",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
