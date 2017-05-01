from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicQVarsRefresh/",  # report_relative_location
                               "test_logic_qVars_refresh",  # report_file_name_prefix
                               "Test refresh a test with an AB question and verify survey has not broken",  # test_suite_title
                               ("This Test performs a test for CREATE-4486. We generate a survey with an AB enabled question."
                                " Test proceeds to refresh the browser and open an accordion section to ensure "
                                "survey still functions."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_logic_qVars_refresh(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Add AB Test to survey, refresh page and make sure survey is still functional.")
    try:
        ex = mySurvey.myBuilder.click_MultipleChoiceAddButton()
        # time.sleep(3)
        ex = mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Kongou")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Hiei")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Kirishima")
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        # time.sleep(1)
        mySurvey.myQuestion.click_on_question_to_edit()
        mySurvey.myQuestion.click_question_options_tab()
        mySurvey.myQuestion.toggleQuestionABTest()
        mySurvey.myQuestion.editQuestionABTest("KONGOU DESU?!!~~~~")
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myLogic.unfold_LogicRegion()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Test that accordion still functions following browser refresh",
                                 "checks to make sure that a the accordion still works following a browser refresh,"
                                 " by refreshing the page and attempting to open the logic accordion.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify logic accordion following browser refresh."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
