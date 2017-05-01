from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestBankAddRemoveAllTagFilter/",  # report_relative_location
                               "test_bank_addRemoveAllTagFilter",  # report_file_name_prefix
                               "Verify add n remove all tag filters",  # test_suite_title
                               ("Test to verify add n remove all tag filters"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})

    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename

@pytest.mark.C280976
@pytest.mark.IB
@pytest.mark.QBL
def test_bank_addRemoveAllTagFilter(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify add n remove all tag filters")

    open_category = "AllCategories"

    try:
        mySurvey.myBank.unfold_QuestionBankRegion()
        ex = mySurvey.myQBank.verifyCategoryExists(open_category, "All Categories")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify open "+ open_category + " Category",
                             "Clicks on " + open_category + " and makes sure that "
                             "it opens with " + open_category + " as hero button",
                             ex,
                             True,
                             not ex,
                             driver)
        assert ex, open_category + " Category closing the modal failed"
        ex = mySurvey.myQBank.clickOnFilter()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify filter tab should open",
                                 "check to make sure that filter tab is open",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to open filter tab"
        ex = mySurvey.myQBank.refineByTag()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify select tag option from refine dropdown",
                                 "check to make sure that tag option from refine dropdown is selected",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to select tag option from refine dropdown"
        ex = mySurvey.myQBank.selectTagsFromTagFilter()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify filter tags are selected",
                                 "check to make sure that filter tags are selected",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to select filter tag"
        ex = mySurvey.myQBank.clickOnApplyFilterButton()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify filter is applied",
                                 "check to make sure that filter is applied",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify filter is applied"
        ex = mySurvey.myQBank.verfiyTagsAppearInTopBar()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify tag appear in blue in top bar",
                                 "check to make sure that verify tag appear in blue in top bar",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify tag appear in blue in top bar"
        ex = mySurvey.myQBank.removeAllTagsByClickingX()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify all tags are reomved at once",
                                 "check to make sure that all tags are removed at once",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to removed all tags at once"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
