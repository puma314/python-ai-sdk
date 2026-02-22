from __future__ import annotations

"""Provider for language, text embedding, and image generation models.

Translated from: packages/provider/src/provider/v3/provider-v3.ts
"""

from typing import Literal, Protocol, runtime_checkable

from ...embedding_model.v3.embedding_model_v3 import EmbeddingModelV3
from ...image_model.v3.image_model_v3 import ImageModelV3
from ...language_model.v3.language_model_v3 import LanguageModelV3
from ...reranking_model.v3.reranking_model_v3 import RerankingModelV3
from ...speech_model.v3.speech_model_v3 import SpeechModelV3
from ...transcription_model.v3.transcription_model_v3 import TranscriptionModelV3


@runtime_checkable
class ProviderV3(Protocol):
    """Provider for language, text embedding, and image generation models."""

    @property
    def specification_version(self) -> Literal['v3']:
        """The specification version of this provider."""
        ...

    def language_model(self, model_id: str) -> LanguageModelV3:
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

    def embedding_model(self, model_id: str) -> EmbeddingModelV3:
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

    def text_embedding_model(self, model_id: str) -> EmbeddingModelV3:
        """Returns the text embedding model with the given id.

        The model id is then passed to the provider function to get the model.

        Args:
            model_id: The id of the model to return.

        Returns:
            The embedding model associated with the id.

        Raises:
            NoSuchModelError: If no such model exists.

        .. deprecated::
            Use ``embedding_model`` instead.
        """
        ...

    def image_model(self, model_id: str) -> ImageModelV3:
        """Returns the image model with the given id.

        The model id is then passed to the provider function to get the model.

        Args:
            model_id: The id of the model to return.

        Returns:
            The image model associated with the id.
        """
        ...

    def transcription_model(self, model_id: str) -> TranscriptionModelV3:
        """Returns the transcription model with the given id.

        The model id is then passed to the provider function to get the model.

        Args:
            model_id: The id of the model to return.

        Returns:
            The transcription model associated with the id.
        """
        ...

    def speech_model(self, model_id: str) -> SpeechModelV3:
        """Returns the speech model with the given id.

        The model id is then passed to the provider function to get the model.

        Args:
            model_id: The id of the model to return.

        Returns:
            The speech model associated with the id.
        """
        ...

    def reranking_model(self, model_id: str) -> RerankingModelV3:
        """Returns the reranking model with the given id.

        The model id is then passed to the provider function to get the model.

        Args:
            model_id: The id of the model to return.

        Returns:
            The reranking model associated with the id.

        Raises:
            NoSuchModelError: If no such model exists.
        """
        ...
