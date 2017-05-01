from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import datetime
import pytest
from smsdk.qafw.create.create_start_existing import EditExistingSurvey
from smsdk.qafw.create.create_start import click_step_1_radio_button


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestStep1CopyAllLogic/",  # report_relative_location
                               "test_step1_copy_allLogic",  # report_file_name_prefix
                               "verify editing existing survey maintains all logics",  # test_suite_title
                               ("This test adds edits and existing survey and tests if the previously existing logic"
                                " was copied and still functions."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    env_init('platinum_advanced_branching')
    import datetime
    import os
    testcasename = datetime.datetime.now().strftime("%I:%M%p %b %d, %Y") + '--' + os.path.basename(__file__).split('.')[
        0]

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_step1_copy_allLogic(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify editing existing survey maintains advanced branching with basic logic sent to another user")
    try:
        survey_title = datetime.datetime.now().strftime("%I:%M%p %b %d, %Y") + '--' + "test_step1_copy_allLogic"

        new_survey_id = mySurvey.myCreate.copy_exiting_survey_via_svysvc("130333866", "58275163", survey_title)
        mySurvey.myCreate.click_new_survey()
        step1 = EditExistingSurvey(driver)
        click_step_1_radio_button(driver, 2)
        ex = mySurvey.myCreate.choose_first_existing_survey(survey_title)

        report.add_report_record(ReportMessageTypes.TEST_STEP, "Survey Loaded or recreated",
                                 "The survey has either been copied or recreated and is ready for the test",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        ex = mySurvey.myLogic.checkQuotaIcon(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that page quota icon appears",
                                 "checks to make sure that the page quota icon appears.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify presence of page quota icon"
        mySurvey.myDesign.clickNextButton()
        mySurvey.myDesign.select_collector_type("weblink")
        ex = mySurvey.myLogic.verifyCustomVarsUrl(customName="myvariable", customLabel="myvariable_value")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "collector page url verification",
                                 "Verifies that custom variables appear in the collector page url",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify collector page url"
        mySurvey.myDesign.returnToDesignPage()
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
        ex = mySurvey.myDesign.verify_preview_question_title_randomized(["Favorite Akizuki Class", "Favorite Shiratsuyu Class"])
        if not ex:
            ex = mySurvey.myDesign.verify_preview_question_title_randomized(["Favorite Myoukou Class", "Favorite Sendai Class"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Checking Logics",
                                 "Check to make sure copied logics continue to work.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Logic on Page 1"
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.switch_to_preview_iframe()
        ex = mySurvey.myDesign.verify_preview_question_title_randomized(["Favorite Akizuki Class", "Favorite Shiratsuyu Class"])
        if not ex:
            ex = mySurvey.myDesign.verify_preview_question_title_randomized(["Favorite Myoukou Class", "Favorite Sendai Class"])
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Checking Logics",
                                 "Check to make sure copied logics continue to work.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Logic on Page 2"
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.switch_to_preview_iframe()
        ex = mySurvey.myDesign.verify_preview_question_title("Best Kongou Class", 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Checking Logics",
                                 "Check to make sure copied logics continue to work.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Logic on Page 3"
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.switch_to_preview_iframe()
        ex = mySurvey.myDesign.verify_preview_question_title("Best Mogami Class", 1)
        if not ex:
            ex = mySurvey.myDesign.verify_preview_question_title("Favorite Akatsuki Class", 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Checking Logics",
                                 "Check to make sure copied logics continue to work.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Logic on Page 4"
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.switch_to_preview_iframe()
        ex = mySurvey.myDesign.verify_preview_question_title("Best Mogami Class", 1)
        if not ex:
            ex = mySurvey.myDesign.verify_preview_question_title("Favorite Akatsuki Class", 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Checking Logics",
                                 "Check to make sure copied logics continue to work.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Logic on Page 5"
        mySurvey.myDesign.click_preview_done_button()
        # mySurvey.myDesign.return_from_frame()
        myTitle = mySurvey.myDesign.getPreviewEndTitle()
        myBool = False
        if myTitle == "That's the end of the preview!":
            myBool = True
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check for ending survey page",
                                 "Check ending survey page.",
                                 myBool,
                                 True,
                                 not myBool,
                                 driver)
        assert myBool, "Failed to verify EOS page and advanced branching rules"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
