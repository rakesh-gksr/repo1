from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicQuestionSkipPageBreak/",  # report_relative_location
                               "test_logic_questionSkip_pageBreak",  # report_file_name_prefix
                               "verify question logic with page break",  # test_suite_title
                               ("This test adds 1 page with multiple questions. Test adds question skip logic  "
                                " and verifies that question skip logic works with auto page break."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def _setup_questions(mySurvey):
    mySurvey.myBuilder.unfold_BuilderRegion()
    mySurvey.myBuilder.click_MultipleChoiceAddButton()
    mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
    mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Kongou")
    mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Hiei")
    mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Kirishima")
    mySurvey.myQuestion.click_question_save_from_edit_tab()
    mySurvey.myBuilder.click_DropdownAddButton()
    mySurvey.myQuestion.enter_question_title("Best Vocaloid?")
    mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Miku")
    mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Luka")
    mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Rin")
    mySurvey.myQuestion.click_question_save_from_edit_tab()
    mySurvey.myBuilder.click_MultipleChoiceAddButton()
    mySurvey.myQuestion.enter_question_title("Favorite League ADC Champion?")
    mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Ashe")
    mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Caitlyn")
    mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Corki")
    mySurvey.myQuestion.click_question_save_from_edit_tab()
    mySurvey.myBuilder.click_DropdownAddButton()
    mySurvey.myQuestion.enter_question_title("This wormhole leads to...")
    mySurvey.myQuestion.enter_multipleChoice_answerText(1, "A room with a moose")
    mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Fluffy Pillows")
    mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Pixels")
    mySurvey.myQuestion.click_question_save_from_edit_tab()
    mySurvey.myBuilder.click_MultipleChoiceAddButton()
    mySurvey.myQuestion.enter_question_title("Favorite Destroyer?")
    mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Shimakaze")
    mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Yuudachi")
    mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Amatsukaze")
    mySurvey.myQuestion.click_question_save_from_edit_tab()


def test_logic_questionSkip_pageBreak(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify question logic with page break.")
    try:
        _setup_questions(mySurvey)
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.click_question_logic_tab()
        mySurvey.myLogic.setQuestionSkipLogic(1, "End of survey", True)
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.click_question_logic_tab()
        mySurvey.myLogic.setQuestionSkipLogic(2, 1, False, 4)
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.click_question_logic_tab()
        mySurvey.myLogic.toggle_pageBreak_circularLogic()
        ex = mySurvey.myDesign.click_preview_button()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Open a new survey and click the preview button",
                                 "Opens a new Survey and clicks the preview button.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        ex = mySurvey.myDesign.switch_to_preview_window()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Switching Focus to new window opened",
                                 "Switches Focus to what should be the preview and test window.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        mySurvey.myDesign.click_off_preview_warning()
        mySurvey.myDesign.switch_to_preview_iframe()
        # begin verification using rpage lib
        mySurvey.myDesign.previewNext()
        ex = mySurvey.myLogic.process_rPage_question_title("1", "2. Best Vocaloid?")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify page break question 2",
                                 "Verifies that auto page break splits question 2 onto page 2.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify page break question 2."
        ex = mySurvey.myLogic.process_rPageMCQuestion("2", "3. Favorite League ADC Champion?", "Caitlyn")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify page break question 3",
                                 "Verifies that auto page break splits question 3 onto page 2.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify page break question 3."
        ex = mySurvey.myLogic.process_rPage_question_title("3", "4. This wormhole leads to...")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify page break question 4",
                                 "Verifies that auto page break splits question 4 onto page 2.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify page break question 4."
        ex = mySurvey.myLogic.process_rPageMCQuestion("4", "5. Favorite Destroyer?", "Yuudachi")  # poi
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify page break question 5",
                                 "Verifies that auto page break splits question 5 onto page 2.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify page break question 5."
        mySurvey.myDesign.previewBack()
        ex = mySurvey.myLogic.process_rPageMCQuestion("1", "1. Best Kongou Class Ship?", "Hiei")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question skip logic",
                                 "Verifies that question skip logic applied to row3 in preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question skip logic row2 in preview."
        mySurvey.myDesign.previewNext()
        # weird number incrementing going on here not sure if bug
        ex = mySurvey.myLogic.process_rPage_question_title("1", "2. This wormhole leads to...")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question skip logic question 2",
                                 "Verifies that question skip logic skipped to correct question in page 2.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question skip logic skipped to correct question on page 2."
        ex = mySurvey.myLogic.process_rPageMCQuestion("2", "3. Favorite Destroyer?", "Yuudachi")  # poi
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question skip logic question 3",
                                 "Verifies that question skip logic skipped to correct question in page 2.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question skip logic skipped to correct question on page 2."
        mySurvey.myDesign.previewBack()
        ex = mySurvey.myLogic.process_rPageMCQuestion("1", "1. Best Kongou Class Ship?", "Kongou")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question skip logic skip",
                                 "Verifies that question skip logic applied to row1 in preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question skip logic row1 in preview."
        ex = mySurvey.myDesign.previewNext(True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question skip logic skip to end",
                                 "Verifies that question skip logic skips to end of survey.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question skip logic skipped to end of survey."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
