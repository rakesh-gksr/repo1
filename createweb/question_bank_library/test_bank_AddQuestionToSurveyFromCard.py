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
                               "TestBankVerifyAddedQuestionToSurvey",  # report_relative_location
                               "test_bank_verifyAddQuestionToSurveyFromCard",  # report_file_name_prefix
                               "Verify added question from card to survey",  # test_suite_title
                               "Testing of question add to survey from card / modal box / QB",
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
@pytest.mark.TC_BVT
@pytest.mark.C410842
def test_bank_add_question_to_survey_from_card(create_survey):
    driver, mySurvey, report = create_survey
    ex = mySurvey.mySvc_holder.svysvc_create.get_already_added_bankedquestions(mySurvey.survey_id)

    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify Added Question from card to main survey")
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

        ul_item = 1
        preview_question_ids= []
        total_questions_to_add = 4
        for li_item in range(1, total_questions_to_add+1):
            # prepare list of question ids that need to match afer add operation
            q_id = mySurvey.myQBank.get_modal_question_ids(ul_item, li_item)
            if q_id is not False:
                preview_question_ids.append(q_id)

            # add questions
            ex = mySurvey.myQBank.add_question_from_question_box_by_plus_icon_click(ul_item, li_item)
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Add Modal Question From List",
                                     "Verify question added on click of card or question box.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to add question"

            # check question plus icon change to check icon or not after question add
            ex = mySurvey.myQBank.check_modal_question_icon_visible(ul_item, li_item)
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Added or Not",
                                     "Verify Question added or not based on the plus / check mark icon.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify checked icon after question add"

            # check question added into preview box or not
            ex = mySurvey.myQBank.check_modal_question_added_in_preview_box(li_item)
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question in Preview Box",
                                     "Verify Added Question is added into preview box or not.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to add  question in preview box"

            #  check card / li box color after question add. It should be grey after question add
            ex = mySurvey.myQBank.check_modal_question_card_box_color(ul_item, li_item, '#eaeae8')
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Check Modal Box Color",
                                     "Verify Modal Box Color of added question.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to change question card color to grey"

            ex = mySurvey.myQBank.check_modal_question_box_hover_color(ul_item, li_item)
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Check hover effect of card",
                                     "Verify hover effect of question card.",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to verify hover color"

            ex = mySurvey.myQBank.check_preview_question_box_color(li_item)
            report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Box Color in Preview Window",
                                     "Verify question box color is grey after adding into preview window",
                                     ex,
                                     True,
                                     not ex,
                                     driver)
            assert ex, "Failed to validate question box color in preview window"

        # add preview modal questions into main survey
        ex = mySurvey.myQBank.add_preview_question_from_modal_box()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Add Into Main Survey",
                                 "Verify that preview question gets added into main survey or not by clicking on "
                                 "Add button present at preview window",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add question from preview window to main survey by clicking on add button"

        # get question Ids that are already or recently added into survey
        survey_questions = mySurvey.mySvc_holder.svysvc_create.get_already_added_bankedquestions(mySurvey.survey_id)
        total_added_questions = len(survey_questions)

        ex1 = False
        if total_added_questions == 4:
            ex1 = True

        ex2 = False
        # Compare Preview Question with Added Questions
        ex2 = mySurvey.myQBank.verify_main_survey_questions_ids(survey_questions, preview_question_ids)

        # Verify Preview Question Count with Added Questions Count from preview section
        ex3 = mySurvey.myQuestion.verify_main_survey_questions_count(1, total_questions_to_add)

        if ex1 is True and ex2 is True and ex3 is True:
            ex = True

        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Preview and Main survey questions",
                                 "Verify Preview and Main survey Questions.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify preview and main survey questions"

    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occurred during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()