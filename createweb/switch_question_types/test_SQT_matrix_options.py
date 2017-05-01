from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):

    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSQTMatrixOptions/",  # report_relative_location
                               "test_SQT_matrix_options",  # report_file_name_prefix
                               "verify switching from ranking to matrix question ",  # test_suite_title
                               ("This test suite adds a ranking question and switches it to a matrix question   "
                                " Test verifies question options and question saves."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_SQT_matrix_options(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify switching from ranking to matrix question")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_RankingAddButton()
        title = mySurvey.myLogic.RNG(30)
        answerRows = []
        matrixRows = []
        mySurvey.myQuestion.enter_question_title(title)
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[0])
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[1])
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, answerRows[2])
        mySurvey.myQuestion.changeQType("Matrix")
        ex = mySurvey.myQuestion.verifyQuestionSwitchState(title, answerRows, ["multipleChoice", "Matrix"], matrixRows)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify state of question after changing to Matrix",
                                 "verifies that the state of the question remains switching to Matrix",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Matrix"
        matrixRows.append(mySurvey.myLogic.RNG(10))
        matrixRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_matrix_answerText(1, matrixRows[0])
        mySurvey.myQuestion.enter_matrix_answerText(2, matrixRows[1])
        mySurvey.myQuestion.click_question_options_tab()
        ex = mySurvey.myQuestion.verify_all_options(["required", "change_layout", "random_choice", "adjust_layout", "question_a_b"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question options present",
                                 "verifies that all options are present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question options"
        mySurvey.myQuestion.click_question_save_from_options_tab()
        mySurvey.myDesign.scroll_to_top()
        ex = True if mySurvey.myQuestion.verifyMatrixQuestionAnswer(1, 1) == answerRows[0] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 1 answer is correct",
                                 "verifies that the answer of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer row 1"
        ex = True if mySurvey.myQuestion.verifyMatrixQuestionAnswer(1, 2) == answerRows[1] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 2 answer is correct",
                                 "verifies that the answer of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer row 2"
        ex = True if mySurvey.myQuestion.verifyMatrixQuestionAnswer(1, 3) == answerRows[2] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify row 3 answer is correct",
                                 "verifies that the answer of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer row 3"
        ex = True if mySurvey.myQuestion.verifyMatrixColumnAnswer(1, 1) == matrixRows[0] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify column 1 answer is correct",
                                 "verifies that the answer of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer column 1"
        ex = True if mySurvey.myQuestion.verifyMatrixColumnAnswer(1, 2) == matrixRows[1] else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify column 2 answer is correct",
                                 "verifies that the answer of the switched question is correct",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify answer column 2"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
