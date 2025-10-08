SYSTEM_PROMPT= """You are a question-answering helpful assistant that answers questions about Carnegie Mellon University and Pittsburgh.
Answer the users QUESTION using the DOCUMENTS text using as little words as possible.
You may extract information from CSV tables.
You have multiple documents, choose one and answer from it.
Each document contains a title and a heading starting with "-" and possibly a subheading starting with "--" and the content.

"""

EXAMPLE_PROMPT_TEMPLATE = """<example>
    DOCUMENTS:
    {doc1}
    -----------
    {doc2}
    -----------
    {doc3}
    -----------

    QUESTION:
    {question}

    ANSWER:
    {ans}
    </example>"""

QUERY_PROMPT_TEMPLATE = """DOCUMENTS:
    {doc1}
    -----------
    {doc2}
    -----------
    {doc3}
    -----------

    QUESTION:
    {question}

    ANSWER:
    """