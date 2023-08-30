# -*- coding:utf-8 -*-
import json
import logging
from typing import Generator, Union
import time
import uuid

from flask import Response, stream_with_context
from flask_restful import reqparse
from werkzeug.exceptions import InternalServerError, NotFound

from libs.text import detect

import services
from controllers.web import api
from controllers.web.error import AppUnavailableError, ConversationCompletedError, \
    ProviderNotInitializeError, NotChatAppError, NotCompletionAppError, CompletionRequestError, \
    ProviderQuotaExceededError, ProviderModelCurrentlyNotSupportError
from controllers.web.wraps import WebApiResource
from core.conversation_message_task import PubHandler
from core.model_providers.error import LLMBadRequestError, LLMAPIUnavailableError, LLMAuthorizationError, LLMAPIConnectionError, \
    LLMRateLimitError, ProviderTokenNotInitError, QuotaExceededError, ModelCurrentlyNotSupportError
from libs.helper import uuid_value
from services.completion_service import CompletionService
from extensions.ext_database import db
from models.model import Message


# define completion api for user
class CompletionApi(WebApiResource):

    def post(self, app_model, end_user):
        if app_model.mode != 'completion':
            raise NotCompletionAppError()

        parser = reqparse.RequestParser()
        parser.add_argument('inputs', type=dict, required=True, location='json')
        parser.add_argument('query', type=str, location='json')
        parser.add_argument('response_mode', type=str, choices=['blocking', 'streaming'], location='json')
        args = parser.parse_args()

        streaming = args['response_mode'] == 'streaming'

        try:
            response = CompletionService.completion(
                app_model=app_model,
                user=end_user,
                args=args,
                from_source='api',
                streaming=streaming
            )

            return compact_response(response)
        except services.errors.conversation.ConversationNotExistsError:
            raise NotFound("Conversation Not Exists.")
        except services.errors.conversation.ConversationCompletedError:
            raise ConversationCompletedError()
        except services.errors.app_model_config.AppModelConfigBrokenError:
            logging.exception("App model config broken.")
            raise AppUnavailableError()
        except ProviderTokenNotInitError as ex:
            raise ProviderNotInitializeError(ex.description)
        except QuotaExceededError:
            raise ProviderQuotaExceededError()
        except ModelCurrentlyNotSupportError:
            raise ProviderModelCurrentlyNotSupportError()
        except (LLMBadRequestError, LLMAPIConnectionError, LLMAPIUnavailableError,
                LLMRateLimitError, LLMAuthorizationError) as e:
            raise CompletionRequestError(str(e))
        except ValueError as e:
            raise e
        except Exception as e:
            logging.exception("internal server error.")
            raise InternalServerError()


class CompletionStopApi(WebApiResource):
    def post(self, app_model, end_user, task_id):
        if app_model.mode != 'completion':
            raise NotCompletionAppError()

        PubHandler.stop(end_user, task_id)

        return {'result': 'success'}, 200


class ChatApi(WebApiResource):
    def post(self, app_model, end_user):
        if app_model.mode != 'chat':
            raise NotChatAppError()

        parser = reqparse.RequestParser()
        parser.add_argument('inputs', type=dict, required=True, location='json')
        parser.add_argument('query', type=str, required=True, location='json')
        parser.add_argument('response_mode', type=str, choices=['blocking', 'streaming'], location='json')
        parser.add_argument('conversation_id', type=uuid_value, location='json')
        args = parser.parse_args()

        streaming = args['response_mode'] == 'streaming'

        if not detect(args['query']):
            return Response(response="error: question-sensitive", status=200, mimetype='application/json')

        try:
            response = CompletionService.completion(
                app_model=app_model,
                user=end_user,
                args=args,
                from_source='api',
                streaming=streaming
            )

            return compact_response(response, args['conversation_id'])
        except services.errors.conversation.ConversationNotExistsError:
            raise NotFound("Conversation Not Exists.")
        except services.errors.conversation.ConversationCompletedError:
            raise ConversationCompletedError()
        except services.errors.app_model_config.AppModelConfigBrokenError:
            logging.exception("App model config broken.")
            raise AppUnavailableError()
        except ProviderTokenNotInitError as ex:
            raise ProviderNotInitializeError(ex.description)
        except QuotaExceededError:
            raise ProviderQuotaExceededError()
        except ModelCurrentlyNotSupportError:
            raise ProviderModelCurrentlyNotSupportError()
        except (LLMBadRequestError, LLMAPIConnectionError, LLMAPIUnavailableError,
                LLMRateLimitError, LLMAuthorizationError) as e:
            raise CompletionRequestError(str(e))
        except ValueError as e:
            raise e
        except Exception as e:
            logging.exception("internal server error.")
            raise InternalServerError()


class ChatStopApi(WebApiResource):
    def post(self, app_model, end_user, task_id):
        if app_model.mode != 'chat':
            raise NotChatAppError()

        PubHandler.stop(end_user, task_id)

        return {'result': 'success'}, 200


def compact_response(response: Union[dict | Generator], conversation_id: str | None = None) -> Response:
    if isinstance(response, dict):
        return Response(response=json.dumps(response), status=200, mimetype='application/json')
    else:
        def generate() -> Generator:
            try:
                for chunk in response:
                    yield chunk
                if conversation_id:
                    message = db.session.query(Message).filter(
                           Message.conversation_id == conversation_id
                           ).order_by(Message.created_at.desc()).first()
                    if not detect(message.answer):
                        message.answer = "敏感信息"
                        db.session.commit()
                        yield "error: answer-sensitive"
            except services.errors.conversation.ConversationNotExistsError:
                yield "data: " + json.dumps(api.handle_error(NotFound("Conversation Not Exists.")).get_json()) + "\n\n"
            except services.errors.conversation.ConversationCompletedError:
                yield "data: " + json.dumps(api.handle_error(ConversationCompletedError()).get_json()) + "\n\n"
            except services.errors.app_model_config.AppModelConfigBrokenError:
                logging.exception("App model config broken.")
                yield "data: " + json.dumps(api.handle_error(AppUnavailableError()).get_json()) + "\n\n"
            except ProviderTokenNotInitError as ex:
                yield "data: " + json.dumps(api.handle_error(ProviderNotInitializeError(ex.description)).get_json()) + "\n\n"
            except QuotaExceededError:
                yield "data: " + json.dumps(api.handle_error(ProviderQuotaExceededError()).get_json()) + "\n\n"
            except ModelCurrentlyNotSupportError:
                yield "data: " + json.dumps(api.handle_error(ProviderModelCurrentlyNotSupportError()).get_json()) + "\n\n"
            except (LLMBadRequestError, LLMAPIConnectionError, LLMAPIUnavailableError,
                    LLMRateLimitError, LLMAuthorizationError) as e:
                yield "data: " + json.dumps(api.handle_error(CompletionRequestError(str(e))).get_json()) + "\n\n"
            except ValueError as e:
                yield "data: " + json.dumps(api.handle_error(e).get_json()) + "\n\n"
            except Exception:
                logging.exception("internal server error.")
                yield "data: " + json.dumps(api.handle_error(InternalServerError()).get_json()) + "\n\n"

        return Response(stream_with_context(generate()), status=200,
                        mimetype='text/event-stream')


api.add_resource(CompletionApi, '/completion-messages')
api.add_resource(CompletionStopApi, '/completion-messages/<string:task_id>/stop')
api.add_resource(ChatApi, '/chat-messages')
api.add_resource(ChatStopApi, '/chat-messages/<string:task_id>/stop')
