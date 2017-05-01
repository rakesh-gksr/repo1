from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from smsdk.qafw.create.create_start import click_step_1_radio_button
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestStep1CopySurveyDropdown/",  # report_relative_location
                               "test_step1_copySurveyDropdown",  # report_file_name_prefix
                               "verify all user surveys appear in the dropdown for copying an existing survey",  # test_suite_title
                               ("This test adds a survey and verifies that the dropdown menu for copying an existing survey in step 1 "
                                " adds it to the scrollable list."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    env_init('3k_survey_user')
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.skipif(True, reason="Skip this test cases because new step1 design does not display the pagination links")
def test_step1_copySurveyDropdown_count(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify all user surveys appear in the dropdown for copying an existing survey")
    try:
        survey_title = mySurvey.myCreate.get_survey_title()
        mySurvey.myCreate.click_new_survey()
        click_step_1_radio_button(driver, 2)
        oldCount = mySurvey.myCreate.get_copySurvey_dropdownCount()
        mySurvey.myCreate.copy_exiting_survey_via_svysvc("100617006", "57496951", survey_title + " Copied via svysvc")
        driver.refresh()
        click_step_1_radio_button(driver, 2)
        ex = mySurvey.myCreate.verify_copySurvey_dropdownCount(int(oldCount) + 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verifying dropdown menu increased count by 1",
                                 "counts all option elements inside the select and verifies it has been incremented by 1.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify copy existing survey dropdown"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.skipif(True, reason="Skip this test cases because new step1 design does not display the pagination links")
def test_step1_copySurveyDropdown_paginationForward(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify copy survey dropdown pagination works going forwards")
    try:
        mySurvey.myCreate.click_new_survey()
        click_step_1_radio_button(driver, 2)
        oldCount = mySurvey.myCreate.get_copySurvey_dropdownCount()
        mySurvey.myCreate.toggle_copySurvey_dropdown()
        for x in xrange(min(int(oldCount) / 10, 5)):
            mySurvey.myCreate.click_copySurvey_dropdown_nextPage()
        if int(oldCount) / 10 > 5:
            mySurvey.myCreate.click_copySurvey_dropdown_skipLast()
        ex = mySurvey.myCreate.verify_copySuveyDropdown_lastPage(int(oldCount))
        mySurvey.myCreate.toggle_copySurvey_dropdown()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "verify on last page in pagination",
                                 "verifies max number vs current number to verify we are on last page.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify copy survey dropdown pagination forwards"
        mySurvey.myCreate.toggle_copySurvey_dropdown()
        mySurvey.myCreate.click_copySurvey_dropdown_skipFirst()
        ex = mySurvey.myCreate.verify_copySuveyDropdown_firstPage()
        mySurvey.myCreate.toggle_copySurvey_dropdown()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verifying skip to first page",
                                 "Verifies current location in pagination is page 1.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify skip to first page pagination"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.skipif(True, reason="Skip this test cases because new step1 design does not display the pagination links")
def test_step1_copySurveyDropdown_paginationBackwards(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify copy survey dropdown pagination works going backwards")
    try:
        mySurvey.myCreate.click_new_survey()
        click_step_1_radio_button(driver, 2)
        oldCount = mySurvey.myCreate.get_copySurvey_dropdownCount()
        mySurvey.myCreate.toggle_copySurvey_dropdown()
        ex = mySurvey.myCreate.verify_copySuveyDropdown_firstPage()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "verify on first page in pagination",
                                 "verifies we are on first page.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify first page pagination"
        mySurvey.myCreate.click_copySurvey_dropdown_skipLast()
        ex = mySurvey.myCreate.verify_copySuveyDropdown_lastPage(int(oldCount))
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verifying skip to last page",
                                 "Verifies current location in pagination is last.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify skip to last page pagination"
        for x in xrange(min(int(oldCount) / 10, 5)):
            mySurvey.myCreate.click_copySurvey_dropdown_previousPage()
        if int(oldCount) / 10 > 5:
            mySurvey.myCreate.click_copySurvey_dropdown_skipFirst()
        ex = mySurvey.myCreate.verify_copySuveyDropdown_firstPage()
        mySurvey.myCreate.toggle_copySurvey_dropdown()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "verify on first page in pagination",
                                 "verifies min number vs current number to verify we are on first page.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify copy survey dropdown pagination backwards"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.skipif(True, reason="Skip this test cases because new step1 design does not display the pagination links")
def test_step1_copySurveyDropdown_search(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify search function of copy survey dropdown menu")
    try:
        mySurvey.myCreate.click_new_survey()
        click_step_1_radio_button(driver, 2)
        oldCount = mySurvey.myCreate.get_copySurvey_dropdownCount()
        mySurvey.myCreate.enterText_copySurvey_dropdown("ab")
        ex = True if oldCount != mySurvey.myCreate.get_copySurvey_dropdownCount() else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verifying search results",
                                 "compares old max value with new value. If it has changed, search returned subset.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify search results"
        mySurvey.myCreate.toggle_copySurvey_dropdown()
        for x in xrange(10):
            mySurvey.myCreate.click_copySurvey_dropdown_nextPage()
        ex = mySurvey.myCreate.verify_copySuveyDropdown_CurPage(101)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify we have gone forward 10 pages in the pagination",
                                 "Checks that we have gone to page 10 by verifying current number of options.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify current page"
        mySurvey.myCreate.toggle_copySurvey_dropdown()
        mySurvey.myCreate.enterText_copySurvey_dropdown("c")
        mySurvey.myCreate.toggle_copySurvey_dropdown()
        ex = mySurvey.myCreate.verify_copySuveyDropdown_firstPage()
        mySurvey.myCreate.toggle_copySurvey_dropdown()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verifying first page after changing search term",
                                 "changes the search term, and verifying we are sent back to first page with results.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify first page with results after altering search term"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()