from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicPageSkipPageCopy/",  # report_relative_location
                               "test_logic_pageSkip_pageCopy",  # report_file_name_prefix
                               "verify copy page which has skip logic added",  # test_suite_title
                               ("This test adds 2 pages with 1 question each. Test adds page skip logic from P1 -> EOS "
                                " and then copies page 1 to page 3 and veifies no page skip logic on page 3."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_logic_pageSkip_pageCopy(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test copied page skip logic page.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Kongou")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Hiei")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Kirishima")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myBuilder.click_MatrixRatingScaleAddButton()
        mySurvey.myQuestion.enter_question_title("Please classify the following Ships")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Haruna")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Yuudachi")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Naka")
        mySurvey.myQuestion.enter_matrix_answerText(1, "Destroyer(DD)")
        mySurvey.myQuestion.enter_matrix_answerText(2, "Light Cruiser(CL)")
        mySurvey.myQuestion.enter_matrix_answerText(3, "Battleship(BB)")
        mySurvey.myQuestion.enter_matrix_answerText(4, "Aircraft Carrier(CV)")
        mySurvey.myQuestion.enter_matrix_answerText(5, "Submarine(SS)")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        # time.sleep(3)
        mySurvey.myLogic.unfold_LogicRegion()
        mySurvey.myLogic.click_PageSkipLogicButton()
        mySurvey.myLogic.select_PageSkipSelectPage("P1")
        mySurvey.myLogic.click_PageSkipSelectNextButton()
        mySurvey.myLogic.select_PageSkipTypeDropdown("End of Survey")
        mySurvey.myLogic.click_PageSkipLogicTargetApplyButton()
        ex = mySurvey.myLogic.verify_page_skip_logic_applied(0, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add page skip logic to P1",
                                 "Adds page skip logic to P1 to skip to EOS.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add page skip logic from P1 to EOS"
        # time.sleep(10)
        mySurvey.myDesign.scroll_to_top()
        mySurvey.myLogic.copy_existing_page(1, 2)
        ex = mySurvey.myLogic.verify_page_skip_logic_applied(2, 3)
        ex = not ex
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify no Page skip logic present on copied page",
                                 "verifies no page skip logic on page 3.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify no page skip logic applied on copied page"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
