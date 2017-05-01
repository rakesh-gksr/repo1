from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicQuestionSkipVerify/",  # report_relative_location
                               "test_logic_questionSkip_verify",  # report_file_name_prefix
                               # test_suite_title
                               "Verify question logic from logic tab (multiple choice, dropdown)  Multiple logic on single question",
                               ("This test adds 3 pages with questions . Test adds question skip logic  "
                                " and verifies that question skip logic works in preview."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def _seup_questions(mySurvey):
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
    mySurvey.myBuilder.click_NewPageAddButton()
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


def test_logic_questionSkip_verify(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(
        ReportMessageTypes.TEST_CASE,
        "Verify question logic from logic tab (multiple choice, dropdown)  Multiple logic on single question.")
    try:
        _seup_questions(mySurvey)
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.click_question_logic_tab()
        mySurvey.myLogic.setQuestionSkipLogic(1, 2, False, 5)
        mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title("Favorite League AP Mid Champion?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Annie")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Veigar")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Lux")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myBuilder.click_DropdownAddButton()
        mySurvey.myQuestion.enter_question_title("Is this survey becoming silly?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Oh yeah")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Nope, nothing to see here")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Maybe, I'm confused")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title("Favorite editor?(flamewar initiated)")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "vim")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "nano")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "emacs")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.click_question_logic_tab()
        mySurvey.myLogic.setQuestionSkipLogic(2, 3, False, 8)
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.click_question_logic_tab()
        mySurvey.myLogic.setQuestionSkipLogic(3, "Disqualification Page", True)
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.click_question_logic_tab()
        ex = mySurvey.myLogic.verify_questionSkipLogic(1, 2, 5)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question skip logic",
                                 "Verifies that question skip logic applied to row1.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question skip logic row1."
        ex = mySurvey.myLogic.verify_questionSkipLogic(2, 3, 8)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question skip logic",
                                 "Verifies that question skip logic applied to row2.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question skip logic row2."
        ex = mySurvey.myLogic.verify_questionSkipLogic(3, "Disqualification Page", "")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question skip logic",
                                 "Verifies that question skip logic applied to row3.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question skip logic row3."
        mySurvey.myQuestion.click_question_save_from_logic_tab()
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
        assert ex, "Failed to click Preview Button"
        mySurvey.myDesign.click_off_preview_warning()
        mySurvey.myDesign.switch_to_preview_iframe()
        # begin verification using rpage lib
        ex = mySurvey.myLogic.process_rPageMCQuestion("1", "1. Best Kongou Class Ship?", "Kongou")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question skip logic",
                                 "Verifies that question skip logic applied to row1 in preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question skip logic row1 in preview."
        mySurvey.myDesign.previewNext()
        mySurvey.myLogic.process_rPageMCQuestion("3", "3. Favorite Destroyer?", "Yuudachi")  # POI POI
        mySurvey.myDesign.previewBack()
        ex = mySurvey.myLogic.process_rPageMCQuestion("1", "1. Best Kongou Class Ship?", "Hiei")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Open a new survey and click the preview button",
                                 "Opens a new Survey and clicks the preview button.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to click Preview Button"
        mySurvey.myDesign.previewNext()
        mySurvey.myLogic.process_rPageMCQuestion("3", "3. Favorite editor?(flamewar initiated)", "vim")
        mySurvey.myDesign.previewBack()
        ex = mySurvey.myLogic.process_rPageMCQuestion("1", "1. Best Kongou Class Ship?", "Kirishima")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question skip logic",
                                 "Verifies that question skip logic applied to row3 in preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question skip logic row3 in preview."
        ex = mySurvey.myDesign.previewNext(True)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check for end of survey",
                                 "Presses next button and verifies end of survey.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify end of survey."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
