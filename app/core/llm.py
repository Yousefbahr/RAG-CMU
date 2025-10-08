from app.core.prompts import *
from app.core.retriever import *
from transformers import AutoTokenizer, AutoModelForCausalLM
from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TRAIN_Q_DIR = os.path.join(BASE_DIR, "data", "train", "questions.txt")
TRAIN_ANS_DIR = os.path.join(BASE_DIR, "data", "train", "reference_answers.txt")



LLM = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen2-0.5B-Instruct",
        torch_dtype="auto",
        device_map="auto"
    )

LLM_TOKENIZER = AutoTokenizer.from_pretrained("Qwen/Qwen2-0.5B-Instruct")
NUM_FEW_SHOT_EXAMPLES = 5


def get_examples():
    """
    Make a list of example questions and answers and their retrieved documents

    and return as  'SemanticSimilarityExampleSelector' to be used for few shot prompting
    """
    # 5 few shot examples will be chosen (from a pool of examples in training text file) based on similarity from query
    # fetch all examples from training set, documents will be retrived from the retriever
    examples = []
    with open(TRAIN_Q_DIR) as f:
      training_questions = f.readlines()

    with open(TRAIN_ANS_DIR) as f:
      training_answers = f.readlines()

    for i in range(len(training_questions)):
      ex = {}

      if training_questions[i].strip() == "":
        continue

      docs = get_context(training_questions[i])

      ex.update({
          "doc1": docs[0],
          "doc2": docs[1],
          "doc3": docs[2],

          "question": training_questions[i],
          "ans": training_answers[i]
      })

      # dont forget to add the documents for each example
      examples.append(ex)

    example_selector = SemanticSimilarityExampleSelector.from_examples(
        # This is the list of examples available to select from.
        examples,
        # This is the embedding class used to produce embeddings which are used to measure semantic similarity.
        EMBEDDING_MODEL,
        # This is the VectorStore class that is used to store the embeddings and do a similarity search over.
        Chroma,
        # This is the number of examples to produce.
        k=NUM_FEW_SHOT_EXAMPLES,
    )
    return example_selector


def get_total_prompt_template():
    examples = get_examples()

    prompt = FewShotPromptTemplate(
        example_selector=examples,
        example_prompt=PromptTemplate.from_template(EXAMPLE_PROMPT_TEMPLATE),
        suffix = QUERY_PROMPT_TEMPLATE,
        input_variables = ["doc1", "doc2", "doc3", "question"]
        )
    return prompt

def get_response(user_query):

    # retrieve relevant documents
    docs = get_context(user_query)

    # get prompt template
    prompt_template = get_total_prompt_template()

    prompt = prompt_template.invoke({"doc1": docs[0],
                       "doc2": docs[1],
                       "doc3": docs[2],
                       "question": user_query}).to_string()

    device = "cpu"

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]

    text = LLM_TOKENIZER.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    model_inputs = LLM_TOKENIZER([text], return_tensors="pt").to(device)

    generated_ids = LLM.generate(
        model_inputs.input_ids,
        max_new_tokens=512
    )

    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = LLM_TOKENIZER.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return response
