import textwrap

import dspy
from dspy import ChainOfThoughtWithHint
from dspy.utils import DummyLM


def test_cot_with_no_hint():
    lm = DummyLM(["[[ ## rationale ## ]]\nfind the number after 1\n\n[[ ## answer ## ]]\n2"])
    dspy.settings.configure(lm=lm)
    predict = ChainOfThoughtWithHint("question -> answer")
    # Check output fields have the right order
    assert list(predict.extended_signature2.output_fields.keys()) == [
        "rationale",
        "hint",
        "answer",
    ]
    assert predict(question="What is 1+1?").answer == "2"

    for message in lm.get_convo(-1)[0]:
        print("----")
        print(message["content"])
        print("----")
    assert lm.get_convo(-1)[0] == [
        {
            "role": "system",
            "content": textwrap.dedent(
                """\
            """
            ),
        },
        {
            "role": "user",
            "content": textwrap.dedent(
                """\
                """
            ),
        },
    ]


def test_cot_with_hint():
    lm = DummyLM(["[[ ## rationale ## ]]\nfind the number after 1\n\n[[ ## answer ## ]]\n2"])
    dspy.settings.configure(lm=lm)
    predict = ChainOfThoughtWithHint("question -> answer")
    assert list(predict.extended_signature2.output_fields.keys()) == [
        "rationale",
        "hint",
        "answer",
    ]
    assert predict(question="What is 1+1?", hint="think small").answer == "2"

    for message in lm.get_convo(-1)[0]:
        print("----")
        print(message["content"])
        print("----")
    assert lm.get_convo(-1)[0] == [
        {
            "role": "system",
            "content": textwrap.dedent(
                """\
            """
            ),
        },
        {
            "role": "user",
            "content": textwrap.dedent(
                """\
                """
            ),
        },
    ]
