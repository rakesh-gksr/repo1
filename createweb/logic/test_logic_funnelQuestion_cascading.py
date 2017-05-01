from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicFunnelQuestionCascading/",  # report_relative_location
                               "test_logic_funnelQuestion_cascading",  # report_file_name_prefix
                               "test cascading funnel choices",  # test_suite_title
                               ("This test adds a sender and receiver question and funnels accordingly."
                                " Test then adds another receiver and funnels the first receiver to the new question."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_logic_funnelQuestion_newQuestionRow(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Skip from sender page to receiver page.")
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
                                 "checks to make sure that there are now 3 total funneled questions in the survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify total funneled rows."
        # time.sleep(3)
        mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title("Favorite Kanmusu")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Shigure")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Sendai")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Nagato")
        mySurvey.myLogic.toggleQuestionFunneling(2)
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myLogic.verifyNumFunneledRows(6, 3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Funneled Rows",
                                 "checks to make sure that there are now 6 total funneled questions in the survey",
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