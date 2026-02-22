"""
Auto-translated Python mirror for `src/index.ts`.
"""

from __future__ import annotations

from typing import Any, TypeAlias

try:
  from .openai_provider import createOpenAI, openai
except Exception:
  createOpenAI: Any = None
  openai: Any = None

try:
  from .openai_provider import OpenAIProvider, OpenAIProviderSettings
except Exception:
  OpenAIProvider: Any = None
  OpenAIProviderSettings: Any = None

try:
  from .responses.openai_responses_options import OpenAILanguageModelResponsesOptions, OpenAIResponsesProviderOptions
except Exception:
  OpenAILanguageModelResponsesOptions: Any = None
  OpenAIResponsesProviderOptions: Any = None

try:
  from .chat.openai_chat_options import OpenAILanguageModelChatOptions, OpenAIChatLanguageModelOptions
except Exception:
  OpenAILanguageModelChatOptions: Any = None
  OpenAIChatLanguageModelOptions: Any = None

try:
  from .completion.openai_completion_options import OpenAILanguageModelCompletionOptions
except Exception:
  OpenAILanguageModelCompletionOptions: Any = None

try:
  from .embedding.openai_embedding_options import OpenAIEmbeddingModelOptions
except Exception:
  OpenAIEmbeddingModelOptions: Any = None

try:
  from .speech.openai_speech_options import OpenAISpeechModelOptions
except Exception:
  OpenAISpeechModelOptions: Any = None

try:
  from .transcription.openai_transcription_options import OpenAITranscriptionModelOptions
except Exception:
  OpenAITranscriptionModelOptions: Any = None

try:
  from .responses.openai_responses_provider_metadata import OpenaiResponsesProviderMetadata, OpenaiResponsesReasoningProviderMetadata, OpenaiResponsesTextProviderMetadata, OpenaiResponsesSourceDocumentProviderMetadata
except Exception:
  OpenaiResponsesProviderMetadata: Any = None
  OpenaiResponsesReasoningProviderMetadata: Any = None
  OpenaiResponsesTextProviderMetadata: Any = None
  OpenaiResponsesSourceDocumentProviderMetadata: Any = None

try:
  from .version import VERSION
except Exception:
  VERSION: Any = None

