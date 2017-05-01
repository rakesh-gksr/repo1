from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
import pytest

transfer_survey_id = "130159753"
original_user_id = "58199745"

def build_survey_questions(mySurvey, driver, report, assetLib=False):
    if assetLib:
        page_num = mySurvey.myDesign.getPageID(1)
        mySurvey.myQuestion.generate_multichoice_question(mySurvey.survey_id, page_num, "Best Vocaloid?", 1,
                                                          ["Miku", "Luka", "Rin"], True)
        mySurvey.myQuestion.generate_matrix_scale_question(mySurvey.survey_id, page_num,
                                                           "Please classify the following Ships", 2,
                                                           ["Haruna", "Yuudachi", "Naka"],
                                                           ["Destroyer(DD)", "Light Cruiser(CL)", "Battleship(BB)",
                                                            "Aircraft Carrier(CV)", "Submarine(SS)"])
        mySurvey.myDesign.click_add_logo()
        if not assetLib:
            mySurvey.myDesign.click_upload_logo()
        else:
            mySurvey.myDesign.click_upload_logo_fromLib(1)
        mySurvey.myDesign.click_addPageTitle("Page 1", "This is test page 1")
        mySurvey.myOptions.unfold_OptionsRegion()
        mySurvey.myOptions.toggle_progressBar()
    else:
        survey_title = mySurvey.myCreate.get_survey_title()
        new_survey_id = mySurvey.myCreate.copy_exiting_survey_via_svysvc(transfer_survey_id, original_user_id, survey_title + " Copied via svysvc")
        url = mySurvey.myCreate.open_copied_survey(new_survey_id['survey_id'])
        driver.get(url)
    report.add_report_record(ReportMessageTypes.TEST_STEP, "Survey Loaded or recreated",
                             "The survey has either been copied or recreated and is ready for the test",
                             True,
                             True,
                             False,
                             driver)

pytestmark = pytest.mark.MT1


@pytest.fixture(scope="module")
def get_report(request):

    report = reporting_wrapper("Create",  # report_feature_name
                               "TestAssetsThemes/",  # report_relative_location
                               "test_assets_themes",  # report_file_name_prefix
                               "Test applying group themes to the survey",  # test_suite_title
                               ("Creates a custom theme and adds it to the asset library, "
                                " this theme is then applied "
                                " and theme application verified."),  # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    env_init('JianAdmin')
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, %Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename


def test_assets_theme(create_survey):
    driver, mySurvey, report = create_survey

    # then start the normal test
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Test applying group themes to the survey.")
    try:
        build_survey_questions(mySurvey, driver, report, True)
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
    try:
        mySurvey.myTheme.unfold_ThemeRegion()
        mySurvey.myTheme.setUpCustomTheme(1)
        ex = mySurvey.myTheme.clickCustomTheme("testCustomTheme1")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Apply testCustomTheme1",
                                 "Open the theme accordion and select the testCustomTheme1",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to apply testCustomTheme1 theme"
        mySurvey.myTheme.add_theme_to_library("testCustomTheme1")
        ex = mySurvey.myTheme.clickGroupTheme("testCustomTheme1")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Apply testCustomTheme1 from group",
                                 "Open the theme accordion and select the testCustomTheme1",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to apply testCustomTheme1 theme from group"
        ex = mySurvey.myTheme.verifyThemeApplied("testCustomGroupTheme1")
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify testCustomTheme1 Theme",
                                 "Compares current theme with values of what the theme should have",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify testCustomTheme1 theme " + str(ex)
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
    finally:
        mySurvey.myTheme.remove_theme_from_library('testCustomTheme1')
        mySurvey.myTheme.clickCustomTheme("testCustomTheme1")
        mySurvey.myTheme.cleanUpChangeTheme()


