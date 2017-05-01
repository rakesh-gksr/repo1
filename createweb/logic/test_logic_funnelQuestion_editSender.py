from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicFunnelQuestionEditSender/",  # report_relative_location
                               "test_logic_funnelQuestion_editSender",  # report_file_name_prefix
                               "Test changing sender question",  # test_suite_title
                               ("This test adds 2 questions "
                                " and then funnels questions into the rows of the second matrix question "
                                "and then verifies updated rows after editing sender question"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_logic_verifyFunnelRow(create_survey):
    driver, mySurvey, report = create_survey

    driver.refresh()
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test changing sender question.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Kongou")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Hiei")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Kirishima")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myBuilder.click_MatrixRatingScaleAddButton()
        mySurvey.myQuestion.enter_question_title("Please classify the following Ships")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Haruna")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Yuudachi")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Naka")
        mySurvey.myLogic.toggleQuestionFunneling()
        mySurvey.myQuestion.enter_matrix_answerText(1, "Destroyer(DD)")
        mySurvey.myQuestion.enter_matrix_answerText(2, "Light Cruiser(CL)")
        mySurvey.myQuestion.enter_matrix_answerText(3, "Battleship(BB)")
        mySurvey.myQuestion.enter_matrix_answerText(4, "Aircraft Carrier(CV)")
        mySurvey.myQuestion.enter_matrix_answerText(5, "Submarine(SS)")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myLogic.verifyNumFunneledRows(3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Funneled Rows",
                                 "checks to make sure that there are the same number of funneled"
                                 " rows present as rows in the previous question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify funneled rows."
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.enter_question_title("Favorite Kanmusu?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Nagato")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Amatsukaze")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Shimakaze")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        driver.refresh()
        mySurvey.myLogic.verifyFunneledRowsText(["Nagato", "Amatsukaze", "Shimakaze"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Funneled Rows changed",
                                 "checks to make sure that the funneled questions updated with change in sender question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify funneled rows after sender question update."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
