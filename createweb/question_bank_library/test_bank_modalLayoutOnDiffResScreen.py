# py.test -v -s automation/question_bank_library/test_bank_verifyNormalResScreen.py

from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest

open_category = "AllCategories"
test_data = {
    (800, 600): 1,
    (1290, 700): 2,
}


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestBankVerifyModalLayout",  # report_relative_location
                               "test_bank_modalLayoutOnDiffResScreen",  # report_file_name_prefix
                               "Verify Modal Layout on different screen resolution",  # test_suite_title
                               "Testing of add question modal dialog layout on various screen resolution",  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})

    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename

@pytest.mark.MT1
@pytest.mark.QBL
@pytest.mark.IB
@pytest.mark.BVT
@pytest.mark.C280956
@pytest.mark.C284062
def test_bank_modalLayoutOnDiffResScreen(create_survey):
    driver, mySurvey, report = create_survey

    driver.get_window_size()
    driver.set_window_position(0, 0)
    driver.set_window_size(800,600)
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify Add Question Modal Layout")
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
        assert ex, open_category + " Category open modal failed"

        for resolution in test_data.keys():
            w, h = resolution
            driver.set_window_size(w, h)
            expected_col = test_data[resolution]
            print w, h, expected_col
            ex = mySurvey.myQBank.checkQuestionBankCardColumn(expected_col)
            assert ex, "Check number of columns failed for: %d, %d" % (w, h)

            ex = mySurvey.myQBank.verifySearchBar()
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify search bar and question count",
                                     "Check to make sure that hero button on the left side with category name "
                                     "and place to enter search term on the right and question count is shown",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify search bar or question count"
            ex = mySurvey.myQBank.checkTopBarRecommendedTemplates()
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify that top-bar with recommended templates",
                                     "check to make sure that top-bar with recommended templates",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify top-bar with recommended templates"
            if w < 1290:
                ex = mySurvey.myQBank.verifyTwoColumnModal()
                ex = not ex
                report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify one column modal result",
                                         "Check to make sure that modal result is in one column",
                                         ex,
                                         True,
                                         not ex,
                                         driver)
                assert ex, "Failed to verify one column modal result"
            else:
                ex = mySurvey.myQBank.verifyTwoColumnModal()
                report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify two column modal result",
                                         "Check to make sure that modal result is in two column",
                                         ex,
                                         True,
                                         not ex,
                                         driver)
                assert ex, "Failed to verify two column modal result"

            ex = mySurvey.myQBank.verifyPreviewButton()
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify preview button is present",
                                     "check to make sure that preview button is present",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify presence of preview button"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()