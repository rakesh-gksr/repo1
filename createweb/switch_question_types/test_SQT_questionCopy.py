from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSQTQuestionCopy/",  # report_relative_location
                               "test_SQT_questionCopy",  # report_file_name_prefix
                               "Copy switched question to same page and separate page",  # test_suite_title
                               ("This test adds a datetime question and switches it to a single textbox question.  "
                                " Test copies question to new and existing pages and verifies this."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_SQT_questionCopy(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Copy switched question to same page and separate page")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_DateTimeAddButton()
        title = mySurvey.myLogic.RNG(30)
        mySurvey.myQuestion.enter_question_title(title)
        mySurvey.myQuestion.changeQType("SingleTextbox")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.click_question_copy_tab()
        mySurvey.myLogic.copyQuestion(2, 1)
        ex = True if mySurvey.myCreate.num_questions_in_page(1) == 1 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify page 1 contains original question",
                                 "verifies that the question was copied from page 1",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question move from page 1"
        ex = True if mySurvey.myCreate.num_questions_in_page(2) == 1 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verifies question added to page 2",
                                 "Verifies that the question was copied to page 2",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question copied"
        mySurvey.myDesign.scroll_to_top()
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.click_question_copy_tab()
        mySurvey.myLogic.copyQuestion(1, 1)
        ex = True if mySurvey.myCreate.num_questions_in_page(1) == 2 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify page 1 has two questions",
                                 "verifies that the question was copied to same page",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question copy from/to page 1"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
