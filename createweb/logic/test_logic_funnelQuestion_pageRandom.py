from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicFunnelQuestionPageRandom/",  # report_relative_location
                               "test_logic_funnelQuestion_pageRandom",  # report_file_name_prefix
                               "Randomize Pages with sender and receiver question together",  # test_suite_title
                               ("This test adds a sender and receiver question with one funneled into the other "
                                " Test then verifies that page randomization cannot be applied."),  # test_suite_description
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
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Randomize Pages with sender and receiver question together.")
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
        # time.sleep(3)
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageRandomization()
        ex = mySurvey.myLogic.verifyDisabledPageRandomization()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify disabled page randomization",
                                 "checks to make sure that there page randomization options are disabled",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify disabled page randomization options."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()