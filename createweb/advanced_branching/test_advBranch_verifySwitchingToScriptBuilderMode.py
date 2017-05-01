from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAdvBranchVerifySwitchingToScriptBuilderMode/",  # report_relative_location
                               "test_advBranch_verifySwitchingToScriptBuilderMode",  # report_file_name_prefix
                               "Verify switching to script/builder mode",
                               # test_suite_title
                               ("This test verifies user switches to script mode showing applied logic in script"
                                " and switches"
                                "to builder mode without "
                                "throwing any error and without loosing existing logic."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    env_init("platinum_advanced_branching")
    import datetime
    import os
    testcasename = os.path.basename(__file__).split(".")[0] + "--" + datetime.datetime.now().strftime("%I:%M%p %b %d,"
                                                                                                      " %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.advBranch
@pytest.mark.IB
@pytest.mark.C225171
def test_advBranch_verifySwitchingToScriptBuilderMode(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify switching to script/builder mode.")
    try:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myDesign.click_addPageTitle("Page 1", "This is test page 1")
        mySurvey.myQuestion.generate_matrix_scale_question(mySurvey.survey_id, page_num,
                                                           "Please classify the following Ships", 1,
                                                           ["Haruna", "Yuudachi", "Naka"],
                                                           ["Destroyer(DD)", "Light Cruiser(CL)", "Battleship(BB)",
                                                            "Aircraft Carrier(CV)", "Submarine(SS)"])
        mySurvey.myQuestion.generate_dropdown_question(
            mySurvey.survey_id, page_num,
            "Best Vocaloid?", 2, ["Miku", "Luka", "Rin"])

        for x in xrange(1):
            mySurvey.myCreate.newPage_viaSvysvc(mySurvey.survey_id, x + 2, "Page " + str(x + 2))
        driver.refresh()
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1: Page 1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        ex = mySurvey.myLogic.addNewBranchingRule([
            ("matrix", [1, 1, 1], "equals", ["Destroyer(DD)"], "finish", "default", None)])

        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Advanced Logic",
                                 "Verifies advanced logic window closed and logic saved.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to save advanced logic"

        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.editPageSkipLogic(1)
        mySurvey.myLogic.click_EditPageSkipRule()
        ex = mySurvey.myLogic.verifySwitchToScriptMode()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify switched to script mode",
                                 "Verifies that user switched to script mode successfully ",
                                 ex,
                                 True,
                                 not ex,
                                 driver)

        assert ex, "Failed to verify stitched to script mode"

        ex = mySurvey.myLogic.verifySwitchToBuilderMode()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify switched to builder mode",
                                 "Verifies that user switched to builder mode successfully",
                                 ex,
                                 True,
                                 not ex,
                                 driver)

        assert ex, "Failed to verify stitched to builder mode"

        mySurvey.myLogic.verify_pageSkipOn()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Page Skip Logic is applied",
                                 "Verifies page skip logic is applied.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify page skip logic applied"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
