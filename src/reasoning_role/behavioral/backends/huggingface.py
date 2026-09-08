"""Lazy-loading frozen Hugging Face causal language model backend."""

from __future__ import annotations

import hashlib
import time
from typing import Any, Mapping, Sequence

from ..schema import BackendResult, InferenceRequest


class HuggingFaceBackend:
    def __init__(
        self,
        config: Mapping[str, Any],
        *,
        torch_module: Any = None,
        model_loader: Any = None,
        tokenizer_loader: Any = None,
    ) -> None:
        self.config = dict(config)
        self._torch = torch_module
        self._model_loader = model_loader
        self._tokenizer_loader = tokenizer_loader
        self.model: Any = None
        self.tokenizer: Any = None
        self.metadata: dict[str, Any] = {}

    def prepare(self) -> Mapping[str, Any]:
        self._validate_config()
        if self._torch is None or self._model_loader is None or self._tokenizer_loader is None:
            try:
                import torch
                from transformers import AutoModelForCausalLM, AutoTokenizer
            except ImportError as error:
                raise RuntimeError(
                    "Hugging Face backend requires the 'model' optional dependencies"
                ) from error
            self._torch = torch
            self._model_loader = AutoModelForCausalLM
            self._tokenizer_loader = AutoTokenizer

        model_id = str(self.config["model_id"])
        model_revision = str(self.config["model_revision"])
        tokenizer_id = str(self.config.get("tokenizer_id", model_id))
        tokenizer_revision = str(
            self.config.get("tokenizer_revision", model_revision)
        )
        common = {
            "local_files_only": bool(self.config.get("local_files_only", True)),
            "trust_remote_code": bool(self.config.get("trust_remote_code", False)),
        }
        self.tokenizer = self._tokenizer_loader.from_pretrained(
            tokenizer_id, revision=tokenizer_revision, **common
        )
        padding_side = str(self.config.get("padding_side", "left"))
        if padding_side not in {"left", "right"}:
            raise ValueError("padding_side must be left or right")
        self.tokenizer.padding_side = padding_side
        pad_token_was_eos = False
        if self.tokenizer.pad_token_id is None:
            if self.tokenizer.eos_token_id is None:
                raise ValueError("tokenizer needs either a pad token or an EOS token")
            self.tokenizer.pad_token = self.tokenizer.eos_token
            pad_token_was_eos = True
        model_kwargs = {
            **common,
            "revision": model_revision,
            "torch_dtype": self._resolve_dtype(str(self.config.get("dtype", "auto"))),
        }
        if "device_map" in self.config:
            model_kwargs["device_map"] = self.config["device_map"]
        self.model = self._model_loader.from_pretrained(model_id, **model_kwargs)
        self._freeze_model(self.model)
        chat_template = getattr(self.tokenizer, "chat_template", None)
        self.metadata = {
            "backend": "huggingface",
            "model_id": model_id,
            "model_revision": model_revision,
            "tokenizer_id": tokenizer_id,
            "tokenizer_revision": tokenizer_revision,
            "prompt_mode": str(self.config.get("prompt_mode", "plain")),
            "chat_template_sha256": (
                hashlib.sha256(str(chat_template).encode("utf-8")).hexdigest()
                if chat_template is not None
                else None
            ),
            "chat_template": chat_template,
            "pad_token_id": self.tokenizer.pad_token_id,
            "eos_token_id": self.tokenizer.eos_token_id,
            "padding_side": self.tokenizer.padding_side,
            "pad_token_was_eos": pad_token_was_eos,
            "local_files_only": common["local_files_only"],
            "trust_remote_code": common["trust_remote_code"],
            "dtype": str(self.config.get("dtype", "auto")),
            "device_map": self.config.get("device_map"),
            "parameters_frozen": True,
            "gradients_enabled": False,
        }
        return self.metadata

    def _validate_config(self) -> None:
        for field in ("model_id", "model_revision"):
            if not self.config.get(field):
                raise ValueError(f"Hugging Face backend requires {field}")
        if self.config.get("do_sample", False):
            raise ValueError("behavioral calibration v1 requires greedy decoding")
        if str(self.config.get("prompt_mode", "plain")) not in {
            "plain",
            "chat_template",
        }:
            raise ValueError("prompt_mode must be plain or chat_template")

    def _resolve_dtype(self, name: str) -> Any:
        if name == "auto":
            return "auto"
        supported = {
            "float16": "float16",
            "bfloat16": "bfloat16",
            "float32": "float32",
        }
        if name not in supported:
            raise ValueError(f"unsupported dtype {name!r}")
        return getattr(self._torch, supported[name])

    @staticmethod
    def _freeze_model(model: Any) -> None:
        model.eval()
        for parameter in model.parameters():
            parameter.requires_grad_(False)
        if any(bool(parameter.requires_grad) for parameter in model.parameters()):
            raise RuntimeError("failed to freeze all model parameters")

    def format_input(self, prompt: str) -> str:
        if self.tokenizer is None:
            raise RuntimeError("backend must be prepared before formatting")
        if str(self.config.get("prompt_mode", "plain")) == "plain":
            return prompt
        return str(
            self.tokenizer.apply_chat_template(
                [{"role": "user", "content": prompt}],
                tokenize=False,
                add_generation_prompt=True,
            )
        )

    def generate(
        self, requests: Sequence[InferenceRequest]
    ) -> Sequence[BackendResult]:
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("backend must be prepared before generation")
        inputs = [self.format_input(request.prompt) for request in requests]
        started = time.perf_counter()
        try:
            encoded = self.tokenizer(inputs, return_tensors="pt", padding=True)
            if hasattr(encoded, "to"):
                encoded = encoded.to(self.model.device)
            width = int(encoded["input_ids"].shape[1])
            with self._torch.inference_mode():
                sequences = self.model.generate(
                    **encoded,
                    do_sample=False,
                    max_new_tokens=int(self.config.get("max_new_tokens", 32)),
                    pad_token_id=self.tokenizer.pad_token_id,
                    eos_token_id=self.tokenizer.eos_token_id,
                )
            elapsed_ms = (time.perf_counter() - started) * 1000
            results: list[BackendResult] = []
            for request, input_text, sequence, attention in zip(
                requests, inputs, sequences, encoded["attention_mask"]
            ):
                completion_ids = sequence[width:]
                completion = self.tokenizer.decode(
                    completion_ids, skip_special_tokens=True
                )
                results.append(
                    BackendResult(
                        request_id=request.request_id,
                        input_text=input_text,
                        completion=completion,
                        prompt_tokens=int(attention.sum().item()),
                        completion_tokens=len(completion_ids),
                        latency_ms=elapsed_ms / max(len(requests), 1),
                    )
                )
            return results
        except Exception as error:
            return [
                BackendResult(
                    request_id=request.request_id,
                    input_text=input_text,
                    completion=None,
                    prompt_tokens=None,
                    completion_tokens=None,
                    latency_ms=None,
                    error_code="inference_exception",
                    error_message=f"{type(error).__name__}: {error}",
                )
                for request, input_text in zip(requests, inputs)
            ]

    def close(self) -> None:
        self.model = None
        self.tokenizer = None
