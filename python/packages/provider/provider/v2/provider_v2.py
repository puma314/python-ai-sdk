from __future__ import annotations

"""Provider for language, text embedding, and image generation models.

Translated from: packages/provider/src/provider/v2/provider-v2.ts
"""

from typing import Protocol, runtime_checkable

from ...embedding_model.v2.embedding_model_v2 import EmbeddingModelV2
from ...image_model.v2.image_model_v2 import ImageModelV2
from ...language_model.v2.language_model_v2 import LanguageModelV2
from ...speech_model.v2.speech_model_v2 import SpeechModelV2
from ...transcription_model.v2.transcription_model_v2 import TranscriptionModelV2


@runtime_checkable
class ProviderV2(Protocol):
    """Provider for language, text embedding, and image generation models."""

    def language_model(self, model_id: str) -> LanguageModelV2:
        """Returns the language model with the given id.

        The model id is then passed to the provider function to get the model.

        Args:
            model_id: The id of the model to return.

        Returns:
            The language model associated with the id.

        Raises:
            NoSuchModelError: If no such model exists.
        """
        ...

    def text_embedding_model(self, model_id: str) -> EmbeddingModelV2[str]:
        """Returns the text embedding model with the given id.

        The model id is then passed to the provider function to get the model.

        Args:
            model_id: The id of the model to return.

        Returns:
            The language model associated with the id.

        Raises:
            NoSuchModelError: If no such model exists.
        """
        ...

    def image_model(self, model_id: str) -> ImageModelV2:
        """Returns the image model with the given id.

        The model id is then passed to the provider function to get the model.

        Args:
            model_id: The id of the model to return.

        Returns:
            The image model associated with the id.
        """
        ...

    def transcription_model(self, model_id: str) -> TranscriptionModelV2:
        """Returns the transcription model with the given id.

        The model id is then passed to the provider function to get the model.

        Args:
            model_id: The id of the model to return.

        Returns:
            The transcription model associated with the id.
        """
        raise NotImplementedError

    def speech_model(self, model_id: str) -> SpeechModelV2:
        """Returns the speech model with the given id.

        The model id is then passed to the provider function to get the model.

        Args:
            model_id: The id of the model to return.

        Returns:
            The speech model associated with the id.
        """
        raise NotImplementedError
