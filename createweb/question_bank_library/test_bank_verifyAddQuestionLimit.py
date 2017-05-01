from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest

open_category = "AllCategories"
keyword = "School"


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestBankVerifyAddQuestionLimit",  # report_relative_location
                               "test_bank_verifyAddQuestionLimit",  # report_file_name_prefix
                               "Verify Preview Box Limit Validation",  # test_suite_title
                               "Testing of validation of preview box limitation by adding more than 100 questions ",
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})

    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.QBL
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C281124
def test_bank_verify_add_question_limit(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify Preview Box Limit Validation")
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
        assert ex, open_category + "Category closing the modal failed"

        for i in range(100):
            mySurvey.myQBank.add_first_question_from_question_box_by_plus_icon_click()
        total_questions = 100
        ex = mySurvey.myQBank.verifyTotalQuestionAddedInPreview(total_questions)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that All questions from the template added "
                                 "to Preview in the right column",
                                 "check to make sure that All questions from the "
                                 "template should then be added to Preview in the right column",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify all questions from the template added to Preview in the right column"

        ex = mySurvey.myQBank.preview_box_question_limit_validation()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Preview Box Warning Message For 100 Questions",
                                 "check to make sure that preview box warning message should not display for 100 "
                                 "questions",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex is False, "Failed to verify preview box warning message, Warning is displayed for 100 question"

        # add 101th question i.e. maximum limit exceeds
        mySurvey.myQBank.add_question_from_question_box_by_plus_icon_click()
        ex = mySurvey.myQBank.preview_box_question_limit_validation()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Preview Box Message For more than 100 Questions",
                                 "check to make sure that preview box warning message should be displayed for more than"
                                 "100 questions",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify preview validation, Preview box not giving proper error validation " \
                   "on adding questions more than max limit i.e. 100"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()