from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):

    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSQTSwitchingToCommentBox/",  # report_relative_location
                               "test_sliderQType_switchingToCommentBox",  # report_file_name_prefix
                               "Verify switching from slider to matrix/rating scale question type, saving them and "
                               "back to slider can be saved without an error showing default settings",
                               # test_suite_title
                               ("Test to verify switching from slider to Comment Box question type, saving "
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


@pytest.mark.slider_question
@pytest.mark.BVT
@pytest.mark.IB
@pytest.mark.C410838
def test_sliderQType_switchingToCommentBox(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test to verify switching from slider to CommentBox "
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
        # code to change slider question type to CommentBox textbox
        mySurvey.myQuestion.changeQType("CommentBox")
        ex = mySurvey.myQuestion.verify_question_in_edit_mode("question-essay")
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify change question type from Slider to Comment Box",
                                 "verifies that changed question type from Slider to Comment Box",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to CommentBox"

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
        # code to save CommentBox text box question type
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify Save Comment Box question type",
                                 "verifies that Comment Box question type saved",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Comment Box question type saved"
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question Add to Live Preview",
                                 "Verifies that question added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question added to live preview."
        # code to edit CommentBox text box question type
        mySurvey.myQuestion.click_on_question_to_edit()
        # code to change CommentBox textbox question type to slider
        mySurvey.myQuestion.changeQType("Slider")
        ex = mySurvey.myQuestion.verify_question_in_edit_mode('question-open-ended-single', 'slider')
        report.add_report_record(ReportMessageTypes.TEST_STEP,
                                 "Verify change question type from Comment Box to Slider",
                                 "verifies that changed question type from Comment Box to Slider",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question state to Comment Box"
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

