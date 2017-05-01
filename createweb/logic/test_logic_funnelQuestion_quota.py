from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicFunnelQuestionsQuota/",  # report_relative_location
                               "test_logic_funnelQuestions_quota",  # report_file_name_prefix
                               "Test editing for funneling if the question has quota",  # test_suite_title
                               ("This test adds 2 questions and funnels accordingly "
                                " Test then adds a simple quota to the receiver and then"
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


def test_logic_funnelQuestions_quota(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test editing for funneling if the question has quota.")
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
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_Quota()
        mySurvey.myLogic.quotaSetupWizard("simple", 2, 2, [3])

        ex = mySurvey.myLogic.checkQuotaIcon(2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page quota icon appears",
                                 "checks to make sure that the page quota icon appears.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of page quota icon"
        mySurvey.myQuestion.click_on_question_to_edit(2)
        ex = mySurvey.myLogic.verify_disabledFunneling()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that editing of funneling disabled",
                                 "checks to make sure that the questions funneled questions cannot be edited.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence disabled funneling question editing"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
