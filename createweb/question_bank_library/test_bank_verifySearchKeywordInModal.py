from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from smsdk.qafw.create import create_utils
import time
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestBankVerifySearchKeywordInModal/",  # report_relative_location
                               "test_bank_verifySearchKeywordInModal",  # report_file_name_prefix
                               "Verify Search for keyword in Modal",  # test_suite_title
                               ("Testto verify search keyword in Modal results"
                                " questions with searched keyword"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})

    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename

@pytest.mark.C280949
@pytest.mark.IB
@pytest.mark.QBL
def test_bank_verifySearchKeywordInModal(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify Search for keyword in Modal")

    open_category = "Community"
    auto_complete_str = "what"

    try:
        mySurvey.myBank.unfold_QuestionBankRegion()
        ex = mySurvey.myQBank.openCategory(open_category)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify open "+ open_category + " Category",
                             "Clicks on " + open_category + " and makes sure that "
                             "it opens with " + open_category + " as hero button",
                             ex,
                             True,
                             not ex,
                             driver)
        assert ex, open_category + " Category closing the modal failed"

        oldQuestionCount = mySurvey.myQBank.totalCategoryQuestions()

        ex = mySurvey.myQBank.typePartialQuestion(auto_complete_str)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify text entry",
                                 "Enter a partial question to get an autocomplete list",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Verify Text Entry verification failure"
        time.sleep(create_utils.auto_complete_delay)
        ex = mySurvey.myQBank.verifyTwoColumnModal()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify two column modal result",
                                 "Check to make sure that modal result is in two column",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify two column modal result"

        ex = mySurvey.myQBank.verifyQuestionChangesAfterSearchText(oldQuestionCount)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question changes after entering search text",
                                 "Check to make sure that question changes after entering search text",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question changes after entering search text"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
