from tests.python.lib.create.create_utils import get_testrail_info
from smlib.qautils.reporting.report_message_types import ReportMessageTypes
import traceback
import pytest





@pytest.mark.DESIGN
@pytest.mark.BVT
@pytest.mark.C63626616
@pytest.mark.small_regression
def test_design_auto_scroll(request, create_survey):
    driver, mySurvey, report = create_survey
    testcasename = request.node.nodeid
    logging_dict = get_testrail_info(testcasename)
    # then start the normal test
    try:
        mySurvey.myOptions.unfold_OptionsRegion()
        ex = mySurvey.myOptions.verify_auto_scroll_state(target="on")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Auto Scroll Button activated",
                                 "checks for Auto Scroll Button to appear",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify auto scroll button"

        ex = mySurvey.myOptions.toggle_one_question_at_time()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Auto Scroll button is deactivated",
                                 "checks for  Auto Scroll Button to deactivated",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify exit link button"
        ex = mySurvey.myOptions.verify_auto_scroll_state(target="off")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Auto Scroll Button disabled",
                                 "checks for Auto Scroll Button to be removed",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Auto Scroll button disabled"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()