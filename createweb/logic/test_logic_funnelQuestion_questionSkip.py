from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicFunnelQuestionQuestionSkip/",  # report_relative_location
                               "test_logic_funnelQuestion_questionSkip",  # report_file_name_prefix
                               "Test editing for funneling if the question has question skip",  # test_suite_title
                               ("This test adds 2 questions and funnels accordingly "
                                " Test then adds a question skip to the receiver and then"
                                " attempts to edit the receiver."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_logic_funnelQuestion_questionSkip(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test editing for funneling if the question has question skip.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Kongou")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Hiei")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Kirishima")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Haruna")
        mySurvey.myLogic.toggleQuestionFunneling()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myLogic.verifyNumFunneledRows(3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Funneled Rows",
                                 "checks to make sure that there are now 3 total funneled questions in the survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify total funneled rows."
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myQuestion.click_question_logic_tab()
        mySurvey.myLogic.setQuestionSkipLogic(1, "End of survey", True)
        mySurvey.myQuestion.click_on_question_to_edit(2)
        ex = mySurvey.myLogic.verify_disabledFunneling()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that editing of funneling disabled",
                                 "checks to make sure that the questions funneled questions cannot be edited.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence disabled funneling question editing"
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myQuestion.click_question_logic_tab()
        mySurvey.myLogic.clearAll_questionSkipLogic()
        mySurvey.myQuestion.click_on_question_to_edit(2)
        mySurvey.myLogic.toggleQuestionFunneling()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myLogic.verifyEmpytyFunnelRows()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify no funneling",
                                 "checks to make sure that we were able to disable funneling following the removal of logic",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify funneling turned off."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()