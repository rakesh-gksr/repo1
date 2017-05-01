from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest
pytestmark = pytest.mark.LONGRUN

@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestMaxQuestions/",  # report_relative_location
                               "test_max_questions",  # report_file_name_prefix
                               "total questions on a survey",  # test_suite_title
                               ("This test adds 5000 questions "
                                " and then checks to make sure survey warning pops up trying to add 5001th question."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver

    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_max_questions(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Total questions on a survey.")
    try:
        survey_title = mySurvey.myCreate.get_survey_title()
        new_survey_id = mySurvey.myCreate.copy_exiting_survey_via_svysvc("100709281", "57725445", survey_title + " Copied via svysvc")
        url = mySurvey.myCreate.open_copied_survey(new_survey_id['survey_id'])
        driver.get(url)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Survey Loaded or recreated",
                                 "The survey has either been copied or recreated and is ready for the test",
                                 True,
                                 True,
                                 False,
                                 driver)
        mySurvey.myCreate.single_page_goto(51)
        mySurvey.myBuilder.click_MultipleTextboxesAddButtonNoWait()
        ex = mySurvey.myQuestion.verify_max_question_popup()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify maximum questions warning",
                                 "checks to make sure that we warning pops up with maximum question reached",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify maximum question."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
