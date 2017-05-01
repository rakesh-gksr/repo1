# This Python file uses the following encoding: utf-8

from smsdk.qafw.create.create_utils import reporting_wrapper, env_init
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
from dynamic_tests.dynamic_tests_config import recommendation_slides_data
import traceback
import pytest


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestVerifyAddLogoThemeFromRecommTipSection",  # report_relative_location
                               "test_verifyAddLogoThemeFromRecommTipSection",  # report_file_name_prefix
                               "Verify multiple choice and dropdown Q type Recommendation and Add Logo/ Theme "
                               "recommendations from TIP section of Survey Score modal",
                               # test_suite_title
                               "Test to verify multiple choice and dropdown Q type Recommendation and Add Logo/ "
                               "Theme recommendations from TIP section of Survey Score modal",
                               # test_suite_description
                               "utf-8",  # file_encoding
                               {SplunkDataAttributes.TYPE: SplunkTestCaseTypes.REGRESSION})  # selenium_driver
    env_init("basic")
    import datetime
    import os
    testcasename = os.path.basename(__file__).split('.')[0] + '--' + datetime.datetime.now().strftime("%I:%M%p %b %d, "
                                                                                                      "%Y")

    def fin():
        report.save_report()
    request.addfinalizer(fin)
    return report, testcasename

recommendation_slides_data = {
    "1": {

            'recommendation_title': u'A Multiple Choice question in your survey can be further optimized.',
            'recommendation_text': u'To make your survey easier to navigate, switch all questions with more than '
                                   u'15 answer choices to Dropdown question types.',
            'recommendation_q_nums': u'Applies to question 1'

        },
    "2": {

            'recommendation_title': u'A Dropdown question in your survey can be further optimized.',
            'recommendation_text': u'To make your survey faster to complete, switch all questions with fewer '
                                   u'than 6 answer choices to Multiple Choice question types.',
            'recommendation_q_nums': u'Applies to question 2'

        }
}


@pytest.mark.survey_score
@pytest.mark.IB
@pytest.mark.C48268729
def test_verify_add_logo_theme_from_recomm_tip_section(create_survey):
    driver, mySurvey, report = create_survey

    report.add_report_record(ReportMessageTypes.TEST_CASE,
                             "Verify multiple choice and dropdown Q type Recommendation and Add Logo/ Theme "
                             "recommendations from TIP section of Survey Score modal")
    try:

        mySurvey.myBuilder.click_MultipleChoiceAddButton()
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(10))
        for i in range(1, 17):
            mySurvey.myQuestion.enter_multipleChoice_answerText(i, mySurvey.myLogic.RNG(5))

        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 1)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Multiple Choice question with 16 rows Add to "
                                                               "Live Preview",
                                 "Verifies that Multiple Choice question with 16 rows added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Multiple Choice question with 16 rows added to live preview."

        mySurvey.myBuilder.click_DropdownAddButton()
        answerRows = []
        mySurvey.myQuestion.enter_question_title(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        answerRows.append(mySurvey.myLogic.RNG(10))
        mySurvey.myQuestion.enter_multipleChoice_answerText(1, answerRows[0])
        mySurvey.myQuestion.enter_multipleChoice_answerText(2, answerRows[1])
        mySurvey.myQuestion.enter_multipleChoice_answerText(3, answerRows[2])
        mySurvey.myQuestion.enter_multipleChoice_answerText(4, answerRows[3])
        mySurvey.myQuestion.click_question_save_from_edit_tab()
        ex = mySurvey.myQuestion.verify_main_survey_questions_count(1, 2)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Multiple Choice question with 4 rows Add to "
                                                               "Live Preview",
                                 "Verifies that Multiple Choice question with 4 rows added to live preview.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Multiple Choice question with 4 rows added to live preview."
        ex = mySurvey.myCreate.click_survey_score()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Check Rate My Survey CTA",
                                 "verifies Rate My Survey CTA present",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that create Rate My Survey present"

        ex = mySurvey.myCreate.verify_survey_score_modal()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Rate My Survey Modal",
                                 "verifies Rate My Survey modal box appears on screen",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Rate My Survey modal box appears on screen"

        for slide, messages in recommendation_slides_data.iteritems():
            temp = int(slide) - 1
            ex = mySurvey.myCreate.survey_score_next_recommendation(str(temp))
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Click Down Arrow : " + str(slide),
                                     "Click and verifies down arrow for slide: " + str(slide),
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify click on slide: " + str(slide)
            ex = mySurvey.myCreate.verify_recommendation(recommendation_title=messages["recommendation_title"],
                                                         recommendation_text=messages["recommendation_text"],
                                                         recommendation_q_nums=messages["recommendation_q_nums"])
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Recommendation for Slide : " + str(slide),
                                     "Verifies recommendation message for slide:  " + str(slide),
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify recommendation message for slide:  " + str(slide)
        mySurvey.myCreate.click_tip_section_cta("UploadLogo")
        ex = mySurvey.myDesign.click_upload_logo()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Upload Test Logo",
                                 "Uploads a test logo from Upload Logo link in tip section.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to upload Logo from Upload Logo link in tip section."

        mySurvey.myCreate.click_survey_score()
        ex = mySurvey.myCreate.verify_survey_score_modal()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Rate My Survey Modal Reopened",
                                 "verifies Rate My Survey modal box appears on screen",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify that Rate My Survey modal box reopened on screen"

        mySurvey.myCreate.click_tip_section_cta("CustomizeTheme")
        ex = mySurvey.myTheme.is_custom_theme_tab_active()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Custom Theme Tab",
                                 "Verifies that Custom theme tab is active.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify Custom theme tab"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()



