from smsdk.qafw.create.create_utils import reporting_wrapper
from smsdk.qafw.reporting.report_message_types import ReportMessageTypes
from smsdk.qafw.reporting.splunk_data_attributes import SplunkDataAttributes
from smsdk.qafw.reporting.splunk_test_case_types import SplunkTestCaseTypes
import traceback
from smsdk.qafw.create import create_utils
import pytest

open_category = "AllCategories"
keyword = "School"


@pytest.fixture(scope="module")
def get_report(request):
    report = reporting_wrapper("Create",  # report_feature_name
                               "TestBankVerifyPreviewQuestionReorderInPages",  # report_relative_location
                               "test_bank_verifyPreviewQuestionReorderInPages",  # report_file_name_prefix
                               "Verify Preview Box Question Reorder In Pages",  # test_suite_title
                               "Testing reordering features in preview box question between multiple pages",
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
@pytest.mark.C280937
def test_bank_verify_preview_question_reorder_in_pages(create_survey):
    driver, mySurvey, report = create_survey
    report.add_report_record(ReportMessageTypes.TEST_CASE, "Verify Preview Question Reordering In Pages")
    try:
        mySurvey.myBuilder.unfold_BuilderRegion()
        mySurvey.myBuilder.click_NewPageAddButton()
        pagecountList = create_utils.get_page_ID_list(mySurvey.survey_id)
        if len(pagecountList) == 2:
            ex = True
        else:
            ex = False
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify new page is added or not",
                                 "check to make sure that new page is added in Live preview",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to add new page"

        mySurvey.myBank.unfold_QuestionBankRegion()
        ex = mySurvey.myQBank.openCategory(open_category)
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify open " +
                                 open_category + " Category",
                                 "Clicks on " + open_category + " and makes sure that "
                                 "it opens with " + open_category + " as hero button",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, open_category + "Category closing the modal failed"

        li_item = 1
        question_cnt = 0
        preview_question_ids = []
        flag = 0

        # Add 3 questions in page 2 by drag and drop from question bank
        while question_cnt < 3:
            # toggle ul item : if Flag == 0 then ul is 1 otherwise ul is 2
            if not flag:
                ul_item = 1
                flag = 1
            else:
                ul_item = 2
                li_item -= 1
                flag = 0

            if not mySurvey.myQBank.\
                    verifyQuestionHasQuesModifierDropdownButton(ul_item,
                                                                li_item):
                mySurvey.myQBank.\
                    add_question_from_question_box_by_plus_icon_click(ul_item,
                                                                      li_item)

                # prepare list of question ids that need to match after
                # add operation
                q_id = mySurvey.myQBank.get_modal_question_ids(ul_item,
                                                               li_item)
                if q_id is not False:
                    preview_question_ids.append(q_id)
                question_cnt += 1
            li_item += 1

        # Verify page 1 and page 2 question count
        ex1 = mySurvey.myQBank.verify_preview_page_question_count(1, 0)
        ex2 = mySurvey.myQBank.verify_preview_page_question_count(2, 3)

        if ex1 is True and ex2 is True:
            ex = True
        else:
            ex = False

        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Page Question Count Before Reordering ",
                                 "Verify Page Question Count Before Reordering between page 1 and 2.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to match question count in pages before reordering"

        # Move 2 question from page2 to page1 to check the reordering
        from_page = 2
        to_page = 1
        for i in range(1, 3):
            mySurvey.myQBank.move_question_via_drag_and_drop(i,
                                                             from_page, to_page)

        # Verify page 1 and page 2 question count after reordere
        ex1 = mySurvey.myQBank.verify_preview_page_question_count(1, 2)
        ex2 = mySurvey.myQBank.verify_preview_page_question_count(2, 1)

        if ex1 is True and ex2 is True:
            ex = True
        else:
            ex = False

        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Page Question Count After Reordering ",
                                 "Verify Page Question Count After Reordering between page 1 and 2.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to match question count in pages After reordering"

        # add preview modal questions into main survey
        ex = mySurvey.myQBank.add_preview_question_from_modal_box()
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Question Added Into Main Survey",
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
        if total_added_questions == 3:
            ex1 = True

        ex2 = False
        # Compare Preview Question with Added Questions
        ex2 = mySurvey.myQBank.verify_main_survey_questions_ids(survey_questions, preview_question_ids)

        # Verify Preview Question Count with Added Questions Count from preview section
        ex3 = mySurvey.myQuestion.verify_main_survey_questions_count(1, 2)
        ex4 = mySurvey.myQuestion.verify_main_survey_questions_count(2, 1)

        if ex1 is True and ex2 is True and ex3 is True and ex4 is True:
            ex = True

        report.add_report_record(ReportMessageTypes.TEST_STEP, "Verify Preview and Main survey questions",
                                 "Verify Preview and Main survey Questions.",
                                 ex,
                                 True,
                                 not ex,
                                 driver)
        assert ex, "Failed to verify preview and main survey questions"
    except:
        report.add_report_record(ReportMessageTypes.TEST_STEP, "Exception occured during test setup",
                                 traceback.format_exc(),
                                 False,
                                 False,
                                 True,
                                 driver)
        assert False, traceback.format_exc()
