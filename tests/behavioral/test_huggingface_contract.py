from __future__ import annotations

import unittest

from reasoning_role.behavioral.backends.huggingface import HuggingFaceBackend
from reasoning_role.behavioral.schema import InferenceRequest


class FakeParameter:
    def __init__(self) -> None:
        self.requires_grad = True

    def requires_grad_(self, value: bool) -> None:
        self.requires_grad = value


class FakeScalar:
    def __init__(self, value: int) -> None:
        self.value = value

    def item(self) -> int:
        return self.value


class FakeAttention(list[int]):
    def sum(self) -> FakeScalar:
        return FakeScalar(sum(self))


class FakeMatrix(list[list[int]]):
    @property
    def shape(self) -> tuple[int, int]:
        return (len(self), len(self[0]))


class FakeEncoded(dict[str, object]):
    def to(self, device: str) -> "FakeEncoded":
        self["moved_to"] = device
        return self


class FakeInferenceMode:
    def __init__(self, torch: "FakeTorch") -> None:
        self.torch = torch

    def __enter__(self) -> None:
        self.torch.inference_active = True

    def __exit__(self, *args: object) -> None:
        self.torch.inference_active = False


class FakeTorch:
    float16 = "float16"
    bfloat16 = "bfloat16"
    float32 = "float32"

    def __init__(self) -> None:
        self.inference_active = False

    def inference_mode(self) -> FakeInferenceMode:
        return FakeInferenceMode(self)


class FakeTokenizer:
    pad_token_id = 0
    eos_token_id = 2
    eos_token = "</s>"
    chat_template = "{{ messages }}"

    def apply_chat_template(self, messages: object, **kwargs: object) -> str:
        return f"CHAT:{messages}"

    def __call__(self, texts: list[str], **kwargs: object) -> FakeEncoded:
        return FakeEncoded(
            input_ids=FakeMatrix([[10, 11] for _ in texts]),
            attention_mask=[FakeAttention([1, 1]) for _ in texts],
        )

    def decode(self, token_ids: list[int], **kwargs: object) -> str:
        return "A" if token_ids == [3] else "unexpected"


class FakeModel:
    device = "cpu"

    def __init__(self, torch: FakeTorch) -> None:
        self.torch = torch
        self.eval_called = False
        self.parameters_list = [FakeParameter(), FakeParameter()]

    def eval(self) -> None:
        self.eval_called = True

    def parameters(self) -> list[FakeParameter]:
        return self.parameters_list

    def generate(self, **kwargs: object) -> FakeMatrix:
        if not self.torch.inference_active:
            raise AssertionError("generation did not use inference_mode")
        if any(parameter.requires_grad for parameter in self.parameters_list):
            raise AssertionError("parameters were not frozen")
        inputs = kwargs["input_ids"]
        return FakeMatrix([list(row) + [3] for row in inputs])


class Loader:
    def __init__(self, value: object) -> None:
        self.value = value
        self.calls: list[tuple[str, dict[str, object]]] = []

    def from_pretrained(self, identifier: str, **kwargs: object) -> object:
        self.calls.append((identifier, dict(kwargs)))
        return self.value


class HuggingFaceContractTest(unittest.TestCase):
    def test_prepare_freezes_and_generate_disables_gradients(self) -> None:
        torch = FakeTorch()
        tokenizer = FakeTokenizer()
        model = FakeModel(torch)
        model_loader = Loader(model)
        tokenizer_loader = Loader(tokenizer)
        backend = HuggingFaceBackend(
            {
                "model_id": "model",
                "model_revision": "model-rev",
                "tokenizer_id": "tokenizer",
                "tokenizer_revision": "tokenizer-rev",
                "prompt_mode": "plain",
                "local_files_only": True,
                "trust_remote_code": False,
                "dtype": "float32",
                "do_sample": False,
                "max_new_tokens": 4,
            },
            torch_module=torch,
            model_loader=model_loader,
            tokenizer_loader=tokenizer_loader,
        )
        metadata = backend.prepare()
        self.assertTrue(model.eval_called)
        self.assertTrue(all(not item.requires_grad for item in model.parameters()))
        self.assertTrue(metadata["parameters_frozen"])
        self.assertFalse(metadata["gradients_enabled"])
        self.assertEqual(metadata["padding_side"], "left")
        self.assertEqual(model_loader.calls[0][1]["revision"], "model-rev")
        self.assertEqual(tokenizer_loader.calls[0][1]["revision"], "tokenizer-rev")

        item = InferenceRequest(
            request_id="request:1",
            instance_id="instance:1",
            prompt="Prompt",
            expected_answer="A",
            family="function_composition",
            answer_encoding="symbol",
            nuisance_factors={},
        )
        result = backend.generate([item])[0]
        self.assertEqual(result.completion, "A")
        self.assertEqual(result.prompt_tokens, 2)
        self.assertEqual(result.completion_tokens, 1)

    def test_chat_template_is_explicit(self) -> None:
        torch = FakeTorch()
        tokenizer = FakeTokenizer()
        backend = HuggingFaceBackend(
            {
                "model_id": "model",
                "model_revision": "rev",
                "prompt_mode": "chat_template",
                "dtype": "auto",
            },
            torch_module=torch,
            model_loader=Loader(FakeModel(torch)),
            tokenizer_loader=Loader(tokenizer),
        )
        metadata = backend.prepare()
        self.assertTrue(backend.format_input("Prompt").startswith("CHAT:"))
        self.assertEqual(metadata["chat_template"], tokenizer.chat_template)
        self.assertIsNotNone(metadata["chat_template_sha256"])

    def test_sampling_is_rejected(self) -> None:
        backend = HuggingFaceBackend(
            {"model_id": "model", "model_revision": "rev", "do_sample": True}
        )
        with self.assertRaisesRegex(ValueError, "greedy"):
            backend.prepare()


if __name__ == "__main__":
    unittest.main()
