from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):

    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSQTSwitchingToMenuMatrix/",  # report_relative_location
                               "test_sliderQType_switchingToMenuMatrix",  # report_file_name_prefix
                               "Verify switching from slider to matrix dropdown menu question type, saving them and "
                               "back to slider can be saved without an error showing default settings",
                               # test_suite_title
                               ("Test to verify switching from slider to matrix dropdown menu question type, saving "
                                "them and back to slider can be saved without an error showing default settings."),
                               # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, "
                                                                                                      "%Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.IB
@pytest.mark.slider_question
@pytest.mark.BVT
@pytest.mark.C410833
def test_sliderQType_switchingToMenuMatrix(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test to verify switching from slider to matrix dropdown "
                                                           "menu question type, saving them and back to slider can "
                                                           "be saved without an error showing default settings.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        # code to add slider question to survey
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title('Rate SurveyMonkey services')
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question Add to Live Preview",
                                 "Verifies that question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question added to live preview."
        mySurvey.myQuestion.click_on_question_to_edit()
        # code to change slider question type to MenuMatrix textbox
        mySurvey.myQuestion.changeQType("MenuMatrix")
        ex = mySurvey.myQuestion.verify_question_in_edit_mode('question-menu-matrix')
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify change question type from Slider to MenuMatrix",
                                 "verifies that changed question type from Slider to MenuMatrix",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MenuMatrix"

        ex = mySurvey.myQuestion.verifySwitchQuestionTypeWarningMsg()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify error message",
                                 "verifies that warning message display while changing the question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify warning message"
        answerRows = []
        matrixRows = []
        menuRows = []
        title = mySurvey.myLogic.RNG(30)
        mySurvey.myQuestion.enter_question_title(title)
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[0])
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[1])
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, answerRows[2])
        matrixRows.append(mySurvey.myLogic.RNG(10))
        matrixRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_matrix_answerText(1, matrixRows[0])
        mySurvey.myQuestion.enter_matrix_answerText(2, matrixRows[1])
        menuRows.append(mySurvey.myLogic.RNG(10))
        menuRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_answer_choices_matrix_menu(1, menuRows[0])
        mySurvey.myQuestion.enter_answer_choices_matrix_menu(2, menuRows[1])
        # code to save MenuMatrix text box question type
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify Save MenuMatrix question type",
                                 "verifies that MenuMatrix question type saved",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify MenuMatrix question type saved"
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question Add to Live Preview",
                                 "Verifies that question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question added to live preview."
        # code to edit MenuMatrix text box question type
        mySurvey.myQuestion.click_on_question_to_edit()
        # code to change MenuMatrix textbox question type to slider
        mySurvey.myQuestion.changeQType("Slider")
        ex = mySurvey.myQuestion.verify_question_in_edit_mode('question-open-ended-single', 'slider')
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify change question type from MenuMatrix to Slider",
                                 "verifies that changed question type from MenuMatrix to Slider",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to MenuMatrix"
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify Save Slider question type",
                                 "verifies that Slider question type saved",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Slider question type saved"
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question Add to Live Preview",
                                 "Verifies that question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question added to live preview."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

