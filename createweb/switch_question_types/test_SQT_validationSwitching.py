from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):

    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSQTValidationSwitching/",  # report_relative_location
                               "test_SQT_validation_switching",  # report_file_name_prefix
                               "verify validation does not follow question type switching ",  # test_suite_title
                               ("This test suite adds questions with options and changes question type"
                                " Test verifies question verification from original question not present."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_SQT_validationSwitching_dateTime(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify validation for datetime")
    try:
        mySurvey.myDesign.click_addPageTitle("Page 1", "This is test page 1")
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_DateTimeAddButton()
        title = mySurvey.myLogic.RNG(30)
        mySurvey.myQuestion.enter_question_title(title)
        mySurvey.myQuestion.changeQType("SingleTextbox")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        for x in xrange(1):
            mySurvey.myCreate.newPage_viaSvysvc(mySurvey.survey_id, x + 2, "Page " + str(x + 2))
        driver.refresh()
        # We can re use advanced branching verification to test in the preview page
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
        # https://monkeys.jira.com/browse/CREATE-5075 fixed now, changing from Page 1 to Page 2
        ex = mySurvey.myLogic.verify_advanced_branching("text", 1, ["monkey"], "page_skip", "Page 2")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that error does not appear",
                                 "verifies validation error does not appear.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        ex = mySurvey.myLogic.verify_preview_error("The comment you entered is in an invalid format.")
        mySurvey.myDesign.return_from_preview_window()
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
        import datetime
        day_after_tomorrow = datetime.date.today() + datetime.timedelta(days=2)
        ex = mySurvey.myLogic.verify_advanced_branching("text", 1, [day_after_tomorrow.strftime("%m/%d/%Y")], "page_skip", "Page 2")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Matches error to expected fail condition",
                                 "verifies error in event it appears.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to validate the date format"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()


def test_SQT_validationSwitching_multipleChoice(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify validation for MultiChoice")
    try:
        mySurvey.myDesign.click_addPageTitle("Page 1", "This is test page 1")
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        title = mySurvey.myLogic.RNG(30)
        mySurvey.myQuestion.enter_question_title(title)
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, mySurvey.myLogic.RNG(30))
        mySurvey.myQuestion.turn_on_multiple_answers()
        mySurvey.myQuestion.click_question_options_tab()
        mySurvey.myQuestion.turn_on_answer_required()
        mySurvey.myQuestion.select_required_answer_type("exactly")
        mySurvey.myQuestion.enter_required_amount_answers(2)
        mySurvey.myQuestion.click_question_edit_tab()
        mySurvey.myQuestion.changeQType("SingleTextbox")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        for x in xrange(1):
            mySurvey.myCreate.newPage_viaSvysvc(mySurvey.survey_id, x + 2, "Page " + str(x + 2))
        driver.refresh()
        # We can re use advanced branching verification to test in the preview page
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
        ex = mySurvey.myLogic.verify_advanced_branching("text", 1, ["monkey"], "page_skip", "Page 2")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that error does not appear",
                                 "verifies validation error does not appear.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to go to next page"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
