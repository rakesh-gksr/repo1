from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from funkload.Lipsum import Lipsum
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestMaxSurveyTitle/",  # report_relative_location
                               "test_max_surveyTitle",  # report_file_name_prefix
                               "verify adding max characters on survey title field",  # test_suite_title
                               ("This test adds both max and one character over max to custom theme name"
                                " and then checks to make sure the maximum limit was not breached."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_max_surveyTitle(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "verify adding max characters for survey title.")
    try:
        title = Lipsum().getUniqWord(250, 251)
        title = title.replace(title[0:5], "test_")
        mySurvey.myDesign.modifySurveyTitle(title)
        ex = mySurvey.myDesign.verify_Previewtitle_equalto_surveytile(title)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Create survey title max length (250 characters)",
                                 "change survey title to max length",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify max length survey title"
        mySurvey.myDesign.modifySurveyTitleRTE(title, "Turquoise")
        ex = True if len(mySurvey.myDesign.getSurveyTitle()) == 250 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Create survey title max length (250 characters)",
                                 "change survey title to max length with RTE formatting",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify max length survey title with RTE formatting"
        title = title + mySurvey.myLogic.RNG(1)
        mySurvey.myDesign.modifySurveyTitle(title)
        ex = mySurvey.myDesign.verify_Previewtitle_equalto_surveytile(title[:-1])  # maxlength attribute prevents 251 chars
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Create survey title over max length (251 characters)",
                                 "change survey title to over max length, 251st char should be cut off",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify max length survey title"
        mySurvey.myDesign.modifySurveyTitleRTE(title, "Turquoise")
        ex = True if len(mySurvey.myDesign.getSurveyTitle()) == 250 else False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Create survey title over max length (251 characters)",
                                 "change survey title to over max length, 251st char should be cut off. with RTE formatting",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify over max length survey title with RTE formatting"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
