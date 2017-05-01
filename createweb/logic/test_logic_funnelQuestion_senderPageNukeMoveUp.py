from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicFunnelQuestionSenderPageNukeMoveUp/",  # report_relative_location
                               "test_logic_funnelQuestion_senderPageNukeMoveUp",  # report_file_name_prefix
                               "Test delete a page with sender questions - moving questions to preceding page",  # test_suite_title
                               ("This test adds 2 questions seperated by a blank page "
                                " Test then deletes sender page and moves sender question up and doesn't"
                                " delete questions its attached to."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_logic_funnelQuestion_senderPageNukeMoveUp(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test delete a page with sender questions - moving questions to preceding page.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_NewPageAddButton()
        ex = mySurvey.myBuilder.click_MultipleChoiceAddButton()
        # time.sleep(3)
        ex = mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Kongou")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Hiei")
        ex = mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Kirishima")
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        # time.sleep(1)
        # time.sleep(1)
        mySurvey.myBuilder.click_NewPageAddButton()
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
                                 "checks to make sure that there are now 3 total funneled questions in the survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify total funneled rows."
        mySurvey.myCreate.nuke_page_move_questions_up(2)
        # time.sleep(5)
        temp = mySurvey.myCreate.num_questions_in_survey()
        ex = True if temp is 2 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify sender question moved",
                                 "checks to make sure that sender question moved after deletion",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify moved sender question."
        ex = mySurvey.myLogic.verifyNumFunneledRows(3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Funneled Rows",
                                 "checks to make sure that there are still 3 total funneled questions in the survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify total funneled rows."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
