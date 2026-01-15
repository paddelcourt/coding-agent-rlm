# coding-agent-rlm
Coding agent based on RLM implementation

To run the project, you can run main.py. Make sure to set up your environment variables first.

```
uv pip install .
```

For environment variables, create a .env file in the root directory with the following content:

```
GEMINI_API_KEY="your_gemini_api_key"
GEMINI_MODEL="gemini-2.5-pro"
GEMINI_SUB_RLM_MODEL="gemini-2.5-flash-lite"
```

To run the coding agent, use:

```uv python main.py```


To test it against a benchmark, you can run:

benchmark.py (benchmark is based on Alex Zhang's RLM minimal implementation)

```uv python benchmark.py
```



Here are some resources that were used for the project:

https://github.com/alexzhang13/rlm-minimal
https://huggingface.co/datasets/oolongbench/oolong-real
