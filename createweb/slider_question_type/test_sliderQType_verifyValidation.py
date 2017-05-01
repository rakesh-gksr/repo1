from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSliderQTypeVerifyValidation/",  # report_relative_location
                               "test_sliderQType_verifyValidation",  # report_file_name_prefix
                               "Verify question validation without entering all the required fields on edit tab",  # test_suite_title
                               "This test verify question validation without entering all the required fields on "
                               "edit tab",
                               # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d,"
                                                                                                      " %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.slider_question
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C284105
def test_sliderQType_verifyValidation(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "This test verify question validation without entering all "
                                                           "the required fields on edit tab")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SliderAddButton()
        # code to clear slider question error message
        mySurvey.myQuestion.clearSliderQtnInputFields()
        # code to click on save question button
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        # code to verify required field error message
        ex = mySurvey.myQuestion.verifySliderQtnErrorMessages()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Required Field Error Message",
                                 "Verified that slider question is showing required field error message",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add slider question is showing required field error message."

        mySurvey.myQuestion.click_question_options_tab()
        # Code to turning on required answer checkbox
        mySurvey.myQuestion.turn_on_answer_required()
        # Code to clear required message text box
        mySurvey.myQuestion.clearRequiredMessage()
        mySurvey.myQuestion.click_question_edit_tab()
        # code to click on save question button
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        # Code to verify that general error message is appearing on edit page
        ex = mySurvey.myQuestion.verifyGeneralErrorMessage()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Error Message",
                                 "Verified that slider question is showing error message",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add slider question is showing error message."
        # Code to enter question title
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        # Code to fill slider question input texts such as left, middle and right scale values
        mySurvey.myQuestion.fillSliderQtnInputFields()
        # code to click on save question button
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        # Code to verify that general error message is appearing on edit page
        ex = mySurvey.myQuestion.verifyGeneralErrorMessage()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Error Message",
                                 "Verified that slider question is showing error message",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add slider question is showing error message."
        mySurvey.myQuestion.click_question_options_tab()
        # Code to fill required error message
        mySurvey.myQuestion.enter_errmsg_when_not_answered("This question requires an answer.")
        mySurvey.myQuestion.click_question_edit_tab()
        # code to click on save question button
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Slider question type to survey ",
                                 "Verified that slider question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add slider question to survey."
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

