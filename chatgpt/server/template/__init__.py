#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Simple introduction

    :Author: Su Deli 16646
    :Time: 2023/3/3 15:20
    :Modifier: Su Deli 16646
    :UpdateTime: 2023/3/3 15:20
"""
from common.constant import ActionsConstant, ConfigurationConstant
from template.advise import ADVISE_PROMPT
from template.add_comment import INITIAL_PROMPT as ADD_COMMENT_INITIAL_PROMPT
from template.add_debug_code import INITIAL_PROMPT as ADD_DEBUG_CODE_INITIAL_PROMPT
from template.add_stronger_code import INITIAL_PROMPT as ADD_STRONGER_CODE_INITIAL_PROMPT
from template.explain_code import INITIAL_PROMPT as EXPLAIN_INITIAL_PROMPT
from template.find_bugs import INITIAL_PROMPT as FIND_BUGS_INITIAL_PROMPT
from template.generate_unit_test import INITIAL_PROMPT as ADD_TEST_INITIAL_PROMPT
from template.review import INITIAL_PROMPT as REVIEW_INITIAL_PROMPT
from template.improve_readability import INITIAL_PROMPT as OPTIMIZE_INITIAL_PROMPT
from template.pick_common_func import INITIAL_PROMPT as PICK_COMMON_FUNC_INITIAL_PROMPT
from template.simplify_code import INITIAL_PROMPT as SIMPLIFY_CODE_INITIAL_PROMPT
from template.continue_content import INITIAL_PROMPT as CONTINUE_CONTENT_INITIAL_PROMPT
from template.generate_api_test import INITIAL_API_TEST_POINT_PROMPT, INITIAL_API_TEST_SET_PROMPT


"""
prompt default template
"""
DEFAULT_TEMPLATE_MAP = {
    ActionsConstant.FIND_BUGS: FIND_BUGS_INITIAL_PROMPT,
    ActionsConstant.ADD_TEST: ADD_TEST_INITIAL_PROMPT,
    ActionsConstant.OPTIMIZE: OPTIMIZE_INITIAL_PROMPT,
    ActionsConstant.EXPLAIN: EXPLAIN_INITIAL_PROMPT,
    ActionsConstant.ADVISE: ADVISE_PROMPT,
    # ActionsConstant.GENERATE_CODE_BY_ASK: GENERATE_CODE_BY_ASK_INITIAL_PROMPT,
    ActionsConstant.REVIEW: REVIEW_INITIAL_PROMPT,
    ActionsConstant.ADD_DEBUG_CODE: ADD_DEBUG_CODE_INITIAL_PROMPT,
    ActionsConstant.ADD_STRONGER_CODE: ADD_STRONGER_CODE_INITIAL_PROMPT,
    ActionsConstant.ADD_COMMENT: ADD_COMMENT_INITIAL_PROMPT,
    ActionsConstant.PICK_COMMON_FUNC: PICK_COMMON_FUNC_INITIAL_PROMPT,
    ActionsConstant.SIMPLIFY_CODE: SIMPLIFY_CODE_INITIAL_PROMPT,
    # Continue writing content
    ConfigurationConstant.CONTINUE_PROMPT: CONTINUE_CONTENT_INITIAL_PROMPT,
}
