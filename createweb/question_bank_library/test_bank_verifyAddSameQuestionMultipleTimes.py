from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestBankVerifyAddSameQuestionMultipleTimes/",  # report_relative_location
                               "test_bank_verifyAddSameQuestionMultipleTimes",  # report_file_name_prefix
                               "Add same question with drag & drop multiple times",  # test_suite_title
                               "Test Add same question with drag & drop multiple times",  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})

    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename

category_list = [
    {'category': "AllCategories",
     'category_name': "All Categories"}
]
numberOfQuestionsToAdd = 10

@pytest.mark.C280922
@pytest.mark.IB
@pytest.mark.QBL
def test_bank_verifyAddSameQuestionMultipleTimes(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Add same question with drag & drop multiple times")
    try:
        mySurvey.myBank.unfold_QuestionBankRegion()
        ex = mySurvey.myQBank.verifyCategoryExists(
                'AllCategories', 'All Categories')  # retry due to error from loading QB
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify All Categories category",
                                 "Clicks on All Categories and makes sure that "
                                 "it opens with All Categories as hero button",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
        assert ex, "All Categories Category verification failure"
        default_question_plats_count = mySurvey.myQBank.getDefaultQeustionPlatesCount()
        ex = True if (default_question_plats_count == 20) else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Cards",
                                 "Verified that 10 question cards are showing",
                             ex,
                             True,
                             not ex,
                             driver)
        assert ex, "Failed to verify question cards"

        for x in xrange(numberOfQuestionsToAdd):
            mySurvey.myQBank.add_question_from_question_box_by_plus_icon_click()

        ex = mySurvey.myQBank.verify_preview_page_question_count(1, numberOfQuestionsToAdd)
        report.add_report_record(ReportMessageTypes.TEST_STEP, ("Verify Able To Drag And Drop Same Question Card"
                                                                "Preview"),
                                 ("Verified that drag and drop same question card " + str(x+1) + " time to preview"),
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify drag and drop same question card " + str(x+1) + " time to preview"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
