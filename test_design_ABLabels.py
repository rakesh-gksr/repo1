from tests.python.lib.create.create_utils import get_testrail_info
from smlib.qautils.reporting.report_message_types import ReportMessageTypes
import traceback
import pytest





@pytest.mark.DESIGN
def test_design_questionTabbing_textAB(request, create_survey):
    driver, mySurvey, report = create_survey
    testcasename = request.node.nodeid
    logging_dict = get_testrail_info(testcasename)
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify placeholder text states for text AB choice question type.",
                             logging_dict=logging_dict)
    try:
        mySurvey.myBuilder.click_TextABTestAddButton()
        mySurvey.myQuestion.enter_textAB_textbox(1, mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.enter_variable_label(1, "Row 1 Variable Label")
        ex = mySurvey.myQuestion.verify_variableLabel_popup(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify variable label popup",
                                 "Verifies that hovering over the question mark opens the variable label popup.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify label popup"
        mySurvey.myQuestion.enter_textAB_textbox(2, mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.enter_variable_label(2, "Row 2 Variable Label")
        ex = mySurvey.myQuestion.verify_variableLabel_popup(2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify variable label popup",
                                 "Verifies that hovering over the question mark opens the variable label popup.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify label popup"
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myQuestion.click_on_question_to_edit()
        ex = mySurvey.myQuestion.verify_variable_label(1, "Row 1 Variable Label")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify previously entered variable label saved",
                                 "Verifies that previously entered variable label saved.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify variable label"
        ex = mySurvey.myQuestion.verify_variable_label(2, "Row 2 Variable Label")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify previously entered variable label saved",
                                 "Verifies that previously entered variable label saved.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify variable label"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


@pytest.mark.DESIGN
def test_design_questionTabbing_imageAB(request, create_survey):
    driver, mySurvey, report = create_survey
    testcasename = request.node.nodeid
    logging_dict = get_testrail_info(testcasename)
    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify placeholder text states for image AB question type.",
                             logging_dict=logging_dict)
    try:
        mySurvey.myBuilder.click_ImageABTestAddButton()
        mySurvey.myQuestion.enter_imageAB_url(1,
                                              "http://images5.fanpop.com/image/photos/31100000/"
                                              "Keep-Calm-and-Continue-Testing-portal-2-31140076-453-700.jpg")
        mySurvey.myQuestion.enter_variable_label(1, "Row 1 Variable Label")
        ex = mySurvey.myQuestion.verify_variableLabel_popup(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify variable label popup",
                                 "Verifies that hovering over the question mark opens the variable label popup.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify label popup"
        mySurvey.myQuestion.enter_imageAB_url(2,
                                              "http://images4.fanpop.com/image/photos/21200000"
                                              "/TACOS-gir-21208550-838-953.jpg")
        mySurvey.myQuestion.enter_variable_label(2, "Row 2 Variable Label")
        ex = mySurvey.myQuestion.verify_variableLabel_popup(2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify variable label popup",
                                 "Verifies that hovering over the question mark opens the variable label popup.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify label popup"
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myQuestion.click_on_question_to_edit()
        ex = mySurvey.myQuestion.verify_variable_label(1, "Row 1 Variable Label")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify previously entered variable label saved",
                                 "Verifies that previously entered variable label saved.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify variable label"
        ex = mySurvey.myQuestion.verify_variable_label(2, "Row 2 Variable Label")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify previously entered variable label saved",
                                 "Verifies that previously entered variable label saved.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify variable label"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
