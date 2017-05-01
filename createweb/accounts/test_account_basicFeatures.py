from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAccountsMonthlyFeatures/",  # report_relative_location
                               "test_accounts_monthlyFeatures",  # report_file_name_prefix
                               "Verify Select Monthly Account Features and Upgrades",  # test_suite_title
                               ("This test adds all upgrade features to a survey "
                                " and then verifies usage notification."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    env_init('MONTHLY')
    import datetime
    import os

    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime(
        "%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()

    request.addfinalizer(fin)
    return report, testcasename


def test_accounts_monthlyVerifyAll(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test all features that Select Monthly Account can use.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myDesign.clickNextButton()
        mySurvey.myDesign.select_collector_type("weblink")
        mySurvey.myDesign.wait_collectorPage()
        mySurvey.myDesign.click_designSurvey_tab()
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best KanMusu?", 1,
                                                          ["Haruna", "Kongou", "Yuudachi"])
        mySurvey.myQuestion.click_on_question_to_edit()
        mySurvey.myQuestion.addPipingtoQuestion(4)
        ex = mySurvey.myLogic.verify_upgradeNotify("Piping")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify upgrade notification for piping feature",
                                 "verifies select user gets upgrade notification for piping a question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify upgrade notification for question piping."

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()