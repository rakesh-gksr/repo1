from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest

transfer_survey_id = "130000129"
original_user_id = "58014660"

@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAdvBranchTransferExistingWithLogic/",  # report_relative_location
                               "test_advBranch_transferExistingWithLogic",  # report_file_name_prefix
                               "verify transferring existing survey maintains advanced branching with basic logic",  # test_suite_title
                               ("This test transfers an existing survey and tests if the previously existing advanced branching and basic page skip logic"
                                " was copied and still functions."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    env_init("platinum_advanced_branching")
    import datetime
    import os
    testcasename = os.path.basename(__file__).split(".")[0] + "--" + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename

@pytest.mark.MT1
def test_advBranch_transferExistingWithLogic(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify transferring existing survey maintains advanced branching with basic logic")
    try:
        ex = mySurvey.myCreate.transfer_survey(transfer_survey_id, original_user_id, "to")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify survey transferred",
                                 "Check the survey transferred correctly",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to transfer survey "
        url = mySurvey.myCreate.open_copied_survey(transfer_survey_id)
        driver.get(url)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Survey Loaded or recreated",
                                 "The survey has either been copied or recreated and is ready for the test",
                                 True,
                                 True,
                                 False,
                                 driver)
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
        mySurvey.myDesign.click_preview_next_button()
        ex = mySurvey.myDesign.verify_preview_question_title("This survey has become silly!", 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check for advanced branching rule",
                                 "Check to make sure we followed advanced branching rules and skipped to page 3.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify page 3 and advanced branching rules"
        mySurvey.myDesign.click_preview_done_button()
        ex = mySurvey.myDesign.verify_preview_question_title("Best Kanmusu", 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check for page skip logic",
                                 "Check to make sure we followed standard page skip logic rules and skipped to page 2.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify page 2 and standard page skip logic"
        mySurvey.myDesign.return_from_frame()
        mySurvey.myDesign.click_preview_next_button()
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
    finally:
        #blocked by SVYSVC-831
        mySurvey.myCreate.transfer_survey(transfer_survey_id, original_user_id, "from")

