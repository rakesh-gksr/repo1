from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestLogicQuestionSkipPageDestDelete/",  # report_relative_location
                               "test_logic_questionSkip_pageDestDelete",  # report_file_name_prefix
                               "verify deleting page having question skip logic destination question",  # test_suite_title
                               ("This test adds 2 pages with 1 question each. Test adds question skip logic  "
                                " and verifies that deleting page causes warning to appear ."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_logic_questionSkip_clear(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify deleting page having question skip logic destination question.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title("Best Kongou Class Ship?")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "Kongou")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Hiei")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Kirishima")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myBuilder.click_NewPageAddButton()
        mySurvey.myBuilder.click_DropdownAddButton()
        mySurvey.myQuestion.enter_question_title("This wormhole leads to...")
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, "A room with a moose")
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, "Fluffy Pillows")
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, "Pixels")
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.click_question_logic_tab()
        mySurvey.myLogic.setQuestionSkipLogic(1, 2, False, 2)
        mySurvey.myQuestion.click_on_question_to_edit(1)
        mySurvey.myQuestion.click_question_logic_tab()
        ex = mySurvey.myLogic.verify_questionSkipLogic(1, 2, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question skip logic destination",
                                 "Verifies that question skip logic has the correct destination set.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question skip logic for row 1."
        mySurvey.myCreate.nuke_page(2)
        ex = mySurvey.myLogic.verifyPageDeleteWarningLogic()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify warning present",
                                 "Verifies that question skip logic warning appears before deletion.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify logic warning appeared."
        ex = mySurvey.myCreate.num_pages_present(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify page deletion",
                                 "Verifies that warning is not looping and only 1 page remains.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify page deletion."
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
