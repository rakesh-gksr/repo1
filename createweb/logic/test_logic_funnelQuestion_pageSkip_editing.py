from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicFunnelQuestionPageSkipEditing/",  # report_relative_location
                               "test_logic_funnelQuestion_pageSkip_editing",  # report_file_name_prefix
                               "Test delete a sender question which has multiple receiver",  # test_suite_title
                               ("This test adds 3 questions(1 sender and 2 receiver) "
                                " and then funnels questions the questions. Test then deletes sender which"
                                " deletes all questions its attached to."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_logic_funnelQuestion_pageSkip_editing(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test delete a sender question which has multiple receiver.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        ex = mySurvey.myBuilder.click_MultipleChoiceAddButton()
        # time.sleep(3)
        ex = mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Kongou")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Hiei")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Kirishima")
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        # time.sleep(1)
        mySurvey.myBuilder.click_NewPageAddButton()
        # time.sleep(1)
        ex = mySurvey.myBuilder.click_MatrixRatingScaleAddButton()
        ex = mySurvey.myQuestion.enter_question_title("Please classify the following Ships")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Haruna")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Yuudachi")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Naka")
        mySurvey.myLogic.toggleQuestionFunneling()
        ex = mySurvey.myQuestion.enter_matrix_answerText(1, "Destroyer(DD)")
        ex = mySurvey.myQuestion.enter_matrix_answerText(2, "Light Cruiser(CL)")
        ex = mySurvey.myQuestion.enter_matrix_answerText(3, "Battleship(BB)")
        ex = mySurvey.myQuestion.enter_matrix_answerText(4, "Aircraft Carrier(CV)")
        ex = mySurvey.myQuestion.enter_matrix_answerText(5, "Submarine(SS)")
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myLogic.verifyNumFunneledRows(3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Funneled Rows",
                                 "checks to make sure that there are the same number of funneled rows "
                                 "present as rows in the previous question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify funneled rows."
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P2")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        mySurvey.myLogic.select_PageSkipTypeDropdown("End of Survey")
        mySurvey.myLogic.click_PageSkipLogicTargetApplyButton()
        ex = mySurvey.myLogic.verify_page_skip_logic_applied(0, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add page skip logic to P1",
                                 "Adds page skip logic to P1 to skip to EOS.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add page skip logic from P1 to EOS"
        mySurvey.myQuestion.click_on_question_to_edit(2)
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
