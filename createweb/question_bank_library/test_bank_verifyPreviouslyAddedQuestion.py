from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest

open_category = "Community"


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestBankVerifyPreviouslyAddedQuestion",  # report_relative_location
                               "test_bank_verifyPreviouslyAddedQuestion",  # report_file_name_prefix
                               "Verify Previously Added Question Functionality",  # test_suite_title
                               "Testing of verification of previously added question functionality from preview "
                               "window by adding question from modal list",  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})

    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


@pytest.mark.QBL
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C280933
def test_bank_verify_preivously_added_question(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify Previously Added Question Functionality")
    try:
        mySurvey.myBank.unfold_QuestionBankRegion()

        ex = mySurvey.myQBank.openCategory(open_category)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify open " + open_category + " Category",
                                 "Clicks on " + open_category + " and makes sure that "
                                                                "it opens with " + open_category + " as hero button",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, open_category + " Category closing the modal failed"

        initial_question_count = mySurvey.myQBank.totalCategoryQuestions()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify default question box",
                                 "Verify default question box loaded or not",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert initial_question_count > 0, "Failed to load question box"

        ex = mySurvey.myQBank.add_question_from_question_box_by_plus_icon_click(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add First Modal Question",
                                 "Verify First Question added or not by click on plus icon.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add first question"

        # check question added into preview box or not
        ex = mySurvey.myQBank.check_modal_question_added_in_preview_box()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify First Question in Preview Box",
                                 "Verify Added First Question is added into preview box or not.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add first question in preview box"

        ex = mySurvey.myQBank.add_question_from_question_box_by_plus_icon_click(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Second Modal Question",
                                 "Verify Second Question added or not by click on plus icon.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add second question"

        # check question added into preview box or not
        ex = mySurvey.myQBank.check_modal_question_added_in_preview_box(2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Second Question in Preview Box",
                                 "Verify Added Second Question is added into preview box or not.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add second question in preview box"

        ex = mySurvey.myQBank.check_preview_question_box_color()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify First Question Box Color in Preview Window",
                                 "Verify first question box color is grey after adding into preview window",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to validate first question box color in preview window"

        ex = mySurvey.myQBank.check_preview_question_box_color(2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Second Question Box Color in Preview Window",
                                 "Verify second  question box color is grey after adding into preview window",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to validate second question box color in preview window"

        ex = mySurvey.myQBank.add_preview_question_from_modal_box()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Preview Question Added Into Main Survey",
                                 "Verify preview questions added into main survey or not",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add preview questions into main survey"

        mySurvey.myBank.unfold_QuestionBankRegion()

        ex = mySurvey.myQBank.openCategory(open_category)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify open " + open_category + " Category",
                                 "Clicks on " + open_category + " and makes sure that "
                                 "it opens with " + open_category + " as hero button "
                                 "while click on second time",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, open_category + " Category closing the modal failed"

        initial_question_count = mySurvey.myQBank.totalCategoryQuestions()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify default question box loaded second time",
                                 "Verify default question box loaded second time properly or not",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert initial_question_count > 0, "Failed to load question box second time click on category"

        ex = mySurvey.myQBank.check_preview_question_box_color(1, '#cccccc')
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Already Added First Question Color",
                                 "Verify already added first question color is dark grey or not",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to validate already added first question box color in preview window"

        ex = mySurvey.myQBank.check_preview_question_box_color(2, '#cccccc')
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Already Added Second Question Color",
                                 "Verify already added second question color is dark grey or not",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to validate already added second question box color in preview window"

        ex = mySurvey.myQBank.add_question_from_question_box_by_plus_icon_click(2, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Third Modal Question",
                                 "Verify Third Question added or not by click on plus icon.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add Third question"

        # check question added into preview box or not
        ex = mySurvey.myQBank.check_modal_question_added_in_preview_box(3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Third Question in Preview Box",
                                 "Verify Third Question is added into preview box or not.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add third question in preview box"

        ex = mySurvey.myQBank.check_preview_question_box_color(3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Third Question Box Color in Preview Window",
                                 "Verify third question box color is grey after adding into preview window",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to validate third question box color in preview window"

        # check li/questionbox color of previously added question
        ex1 = mySurvey.myQBank.check_class_present_at_preview_question(1)
        ex2 = mySurvey.myQBank.check_class_present_at_preview_question(2)

        # if both 1st and 2nd existing question don't present return as true, means output is correct else False
        ex = True if ex1 is False and ex2 is False else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Already Added Question Functionality",
                                 "Verify already added 2 question functionality like drag/drop, remove, move etc. based"
                                 "on the class check",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to validate existing question functionality based on class check"

        ex = mySurvey.myQBank.check_class_present_at_preview_question(3)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Newly Added Question Functionality",
                                 "Verify newly added  question functionality like drag/drop, remove, move etc. based"
                                 "on the class check",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to validate newly added question functionality based on class check"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()