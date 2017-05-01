from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestBankCustomizeModifierOnQuestionCard/",  # report_relative_location
                               "test_bank_customizeModifierOnQuestionCard",  # report_file_name_prefix
                               "Verify Customize Modifier on Question Card",  # test_suite_title
                               ("Test to verify Customize Modifier "
                                "on Question Card and it updated on live preview"),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})

    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename

@pytest.mark.C280925
@pytest.mark.IB
@pytest.mark.QBL
def test_bank_customizeModifierOnQuestionCard(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify Customize Modifier on Question Card")

    open_category = "HumanResources"
    search_question = "How likely is it that you would recommend <this company> to a friend or colleague?"
    modifier = "surveymonkey"

    try:
        mySurvey.myBank.unfold_QuestionBankRegion()
        ex = mySurvey.myQBank.openCategory(open_category)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify open "+ open_category + " Category",
                             "Clicks on " + open_category + " and makes sure that "
                             "it opens with " + open_category + " as hero button",
                             ex,
                             True,
                             not ex,
                             driver)
        assert ex, open_category + " Category closing the modal failed"

        ex = mySurvey.myQBank.typePartialQuestion(search_question)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify text entry",
                                 "check to make sure that entered question to get an autocomplete list",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Verify Text Entry verification failure"
        ex = mySurvey.myQBank.customizeModifier(modifier)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify question save with modifier",
                                 "check to mke sure that question save with modifier",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify question save with modifier"

        mySurvey.myQBank.addModalSearchQuestionToPreview(1, 1)
        ex = mySurvey.myQBank.check_modal_question_added_in_preview_box()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question in Preview Box",
                                 "Verify Added Question is added into preview box or not.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add question in preview box"
        mySurvey.myQBank.clickAddQuestionOnPreview()
        ex = mySurvey.myDesign.verify_preview_question_in_title(modifier, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify live preview have the modifier updated",
                                 "check to make sure that live preview have the modifier updated",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify modifier updated in live preview"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
