#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dao.base_dao import BaseDao
from models.system.conversation import Conversation


class ConversationDao(BaseDao):
    model = Conversation
