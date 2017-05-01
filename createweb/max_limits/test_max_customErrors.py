from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestMaxCustomErrors/",  # report_relative_location
                               "test_max_customErrors",  # report_file_name_prefix
                               " text length of custom error messages (like on required questions)",  # test_suite_title
                               ("This test adds a multiple choice question "
                                " and adds a custom error message for required answer. Test then verifies custom error message max size."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_max_customErrors(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "  text length of custom error messages (like on required questions).")
    try:
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.click_question_options_tab()
        mySurvey.myQuestion.turn_on_answer_required()
        mySurvey.myQuestion.enter_errmsg_when_not_answered(mySurvey.myLogic.RNG(251))
        mySurvey.myQuestion.click_question_save_from_options_tab()
        ex = mySurvey.myQuestion.verify_question_required(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question required",
                                 "checks to make sure that question requires an answer",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify logo error exceeding max size."
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Click the preview button",
                                 "Clicks preview button, in order to verify theme in preview window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        mySurvey.myDesign.click_off_preview_warning()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.switch_to_preview_iframe()
        mySurvey.myDesign.click_preview_done_button()
        ex = True if mySurvey.myQuestion.verify_requiredAnswer_customErrorLength() == 250 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify length of error message is 250",
                                 "checks to make sure that custom error message is max size",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify max size custom error message."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
