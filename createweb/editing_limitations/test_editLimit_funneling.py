from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestEditLimitOtherOption/",  # report_relative_location
                               "test_editLimit_otherOption",  # report_file_name_prefix
                               "Dropdown:verify add other answer options",  # test_suite_title
                               ("This test adds 2 dropdowns, 1 with other answer enabled. Answers are collected "
                                " and verifies that limited editability is enabled."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_editLimit_otherOption(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Dropdown:verify add other answer options.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        # time.sleep(3)
        mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Kongou")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Hiei")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Kirishima")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        # time.sleep(1)
        mySurvey.myBuilder.click_NewPageAddButton()
        # time.sleep(1)
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
                                 "checks to make sure that there are the same number of funneled rows"
                                 " present as rows in the previous question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify funneled rows."
        # begin verification using rpage lib
        mySurvey.myLogic.process_surveyCollection(mySurvey.myCreate.get_survey_title(),
                                                  [{1: {'choices_list': ['Kongou']}},
                                                   {1: {'choices_list': ['Kongou Battleship(BB)']}}])
        mySurvey.myQuestion.click_on_question_to_edit(2)
        ex = mySurvey.myQuestion.verify_responsesCollected()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify questions collected succesfully",
                                 "checks for limited editability notice",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify limited editability."
        mySurvey.myLogic.toggleQuestionFunneling()
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myLogic.verifyNumFunneledRows(3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Funneled Rows",
                                 "checks to make sure that there are the same number of funneled rows"
                                 " present as rows in the previous question",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify funneled rows."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
