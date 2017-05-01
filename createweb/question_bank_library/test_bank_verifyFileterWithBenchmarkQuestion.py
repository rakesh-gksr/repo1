from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestBankVerifyFileterWithBenchmarkQuestion/",  # report_relative_location
                               "test_bank_verifyFileterWithBenchmarkQuestion",  # report_file_name_prefix
                               "Verify filter with Benchmarkable questions",  # test_suite_title
                               ("Test to verify filter with Benchmarkable questions"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})

    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename

@pytest.mark.C280971
@pytest.mark.IB
@pytest.mark.QBL
def test_bank_verifyFileterWithBenchmarkQuestion(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify filter with Benchmarkable questions")

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
        ex = mySurvey.myQBank.applyFilterToQuestionBankQuestions()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify filter applied to QB questions",
                                 "check to make sure that filter applied to QB questions",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to apply filter"
        ex = mySurvey.myQBank.verifyAppliedBenchmarkFilter()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Benchmarkable question "
                                                               "filter shows on top-bar with green background",
                                 "check to make sure that 'Benchmarkable question' "
                                 "filter shows on top-bar with green background",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify 'Benchmarkable question' filter on top-bar with green background"
        ex = mySurvey.myQBank.verifyAvailableBenchmarkQuestion()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify 'Benchmarkable question' "
                                                               "filter has some questions",
                                 "check to make sure that there are some "
                                 "questions available for 'Benchmarkable question' filter",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question present in 'Benchmarkable question' filter"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
