from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestMaxMenuMatrixDropdown/",  # report_relative_location
                               "test_max_menuMatrix_dropdown",  # report_file_name_prefix
                               "verify adding max column dropdown choices on menu matrix question type",  # test_suite_title
                               ("This test adds a menu matrix with 200 dropdown choices "
                                " and then checks to make sure that an error notification appears when adding another one."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver

    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_max_menuMatrix_dropdown(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify adding max column dropdown choices on menu matrix question type.")
    try:
        mySurvey.myQuestion.create_question_massNewRow_insert(mySurvey.survey_id, "matrix", "menu", 195, "column_dropdown")
        driver.refresh()

        mySurvey.myQuestion.click_on_question_to_edit()
        # add 5 more rows (menu matrix rows) via GUI
        for i in xrange(5):
            mySurvey.myQuestion.add_menuMatrix_dropdownRowText()

        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question saved",
                                 "checks to make sure that save button not visible.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question saved."
        mySurvey.myQuestion.click_on_question_to_edit()
        ex = mySurvey.myQuestion.add_menuMatrix_dropdownRow()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify maximum column dropdown options",
                                 "checks to make sure that the warning pops up with maximum column dropdowns reached",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify maximum column dropdowns for menu matrix."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
