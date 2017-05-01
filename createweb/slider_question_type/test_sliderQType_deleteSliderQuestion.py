from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestSliderQTypeDeleteAndRestoreSliderQuestion/",  # report_relative_location
                               "test_sliderQType_deleteAndRestoreSliderQuestion",  # report_file_name_prefix
                               "Delete slider question and restore back to live preview",  # test_suite_title
                               "This test deletes the slider question and then restore back to live preview",
                               # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d,"
                                                                                                      " %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.slider_question
@pytest.mark.BVT
@pytest.mark.IB
@pytest.mark.C284134
@pytest.mark.C284135
def test_sliderQType_deleteAndRestoreSliderQuestion(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Delete slider question and restore back to live preview.")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_SliderAddButton()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(30))
        ex = mySurvey.myQuestion.click_question_save_from_edit_tab()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Slider question type to survey ",
                                 "Verified that slider question type added to survey",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify add slider question to survey."
        ex = mySurvey.myQuestion.hover_on_question_to_delete_it(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Delete Slider Question",
                                 "verifies that slider question is deleted.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify slider question deleted"

        ex = mySurvey.myCreate.verify_deleted_question(1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Deleted Question Appears In Restore Question",
                                 "verifies that deleted question appears in restore question.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify deleted question appears in restore question"

        mySurvey.myCreate.restoreDeletedQuestion(1)
        ex = True if mySurvey.myCreate.num_questions_in_survey() == 1 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify slider question restore",
                                 "Verifies that slider question restored in live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify slider question restored in live preview"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()

