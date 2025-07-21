from app.model.llm import query_llm
from app.utils.parsing import make_prompt, parse_response


def test_query_llm():
    resume_text = "name: sample name"
    question = "what is his name?"

    prompt = make_prompt(resume_text, question)

    result = query_llm(prompt)
    processed_result = parse_response(result, prompt)

    ## prompt type check
    assert isinstance(prompt, str)

    ## LLM result type check
    assert isinstance(result, str)
