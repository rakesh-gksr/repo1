from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):

    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSQTSwitchingToDateTime/",  # report_relative_location
                               "test_sliderQType_switchingToDateTime",  # report_file_name_prefix
                               "Verify switching from slider to Date / Time question type, saving them and back to "
                               "slider can be saved without an error showing default settings.",  # test_suite_title
                               ("Test to verify switching from slider to Date / Time question type, saving them and "
                                "back to slider can be saved without an error showing default settings."),
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
@pytest.mark.C410840
def test_sliderQType_switchingToDateTime(create_survey):
    driver, mySurvey, report = create_survey
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test to verify switching from slider to Date / Time "
                                                           "question type, saving them and back to slider can be "
                                                           "saved without an error showing default settings.")
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
        # code to change slider question type to Date / Time textbox
        mySurvey.myQuestion.changeQType("DateTime")
        ex = mySurvey.myQuestion.verify_question_in_edit_mode('question-datetime')
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify change question type from Slider to Date / Time",
                                 "verifies that changed question type from Slider to Date / Time",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Date / Time"

        ex = mySurvey.myQuestion.verifySwitchQuestionTypeWarningMsg()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify error message",
                                 "verifies that warning message display while changing the question type",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify warning message"

        title = mySurvey.myLogic.RNG(30)
        mySurvey.myQuestion.enter_question_title(title)
        # code to save Date / Time text box question type
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify Save Date / Time question type",
                                 "verifies that Date / Time question type saved",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Date / Time question type saved"
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question Add to Live Preview",
                                 "Verifies that question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question added to live preview."
        # code to edit Date / Time text box question type
        mySurvey.myQuestion.click_on_question_to_edit()
        # code to change Date / Time textbox question type to slider
        mySurvey.myQuestion.changeQType("Slider")
        ex = mySurvey.myQuestion.verify_question_in_edit_mode('question-open-ended-single', 'slider')
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify change question type from Date / Time to Slider",
                                 "verifies that changed question type from Date / Time to Slider",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Date / Time"
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
