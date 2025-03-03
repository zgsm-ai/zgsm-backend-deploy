#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    简单介绍

    :作者: 陈烜 42766
    :时间: 2023/3/24 14:12
    :修改者: 陈烜 42766
    :更新时间: 2023/3/24 14:12
"""
from services.action.add_comment_service import AddCommentCodeStrategy
from services.action.add_debug_code_service import AddDebugCodeStrategy
from services.action.add_stronger_code_service import AddStrongerCodeStrategy
from services.action.chat_service import ChatStrategy
from services.action.continue_service import ContinueStrategy
from services.action.explain_code_service import ExplainCodeStrategy
from services.action.advise_service import AdviseStrategy
from services.action.find_bugs_service import FindBugsStrategy
from services.action.optimize_code_service import OptimizeCodeStrategy
from services.action.base_service import ChatbotOptions
from services.action.review_service import ReviewStrategy
from services.action.simplify_code_service import SimplifyCodeStrategy
from services.action.zhuge_normal_chat import NormalChatStrategy

strategy_map = {
    FindBugsStrategy.name: FindBugsStrategy,
    OptimizeCodeStrategy.name: OptimizeCodeStrategy,
    ExplainCodeStrategy.name: ExplainCodeStrategy,
    ChatStrategy.name: ChatStrategy,
    ReviewStrategy.name: ReviewStrategy,
    AddDebugCodeStrategy.name: AddDebugCodeStrategy,
    AddStrongerCodeStrategy.name: AddStrongerCodeStrategy,
    AddCommentCodeStrategy.name: AddCommentCodeStrategy,
    SimplifyCodeStrategy.name: SimplifyCodeStrategy,
    ContinueStrategy.name: ContinueStrategy,
    NormalChatStrategy.name: NormalChatStrategy,
    AdviseStrategy.name: AdviseStrategy,
}


def get_action_strategy(action):
    return strategy_map.get(action, ChatStrategy)()


__all__ = [
    'get_action_strategy',
    'ChatbotOptions',
    'strategy_map',
]
