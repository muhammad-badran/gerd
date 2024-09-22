config = {
    'app': {
        'config': {
            'name': 'full-stack-app'
        }
    },
    'llm': {
        'provider': 'openai',
        'config': {
            'model': 'gpt-4o-mini',
            'temperature': 0.5,
            'max_tokens': 1000,
            'top_p': 1,
            'stream': False,
            'prompt': (
                "Use the following pieces of context to answer the query at the end.\n"
                "If you don't know the answer, just say that you don't know, don't try to make up an answer.\n"
                "$context\n\nQuery: $query\n\nHelpful Answer:"
            ),
            'system_prompt': (
                "Act as William Shakespeare. Answer the following questions in the style of William Shakespeare."
            ),
            'api_key': os.environ["OPENAI_API_KEY"],
            "model_kwargs": {"response_format": {"type": "json_object"}},
        }
    },
    'vectordb': {
        'provider': 'pinecone',
        'config': {
            'metric': 'dotproduct',
            'vector_dimension': 1536,
            'index_name': 'my-index',
            'serverless_config': {
                'cloud': 'aws',
                'region': 'us-west-2'
            },
            'hybrid_search': True, # Remember to set this for hybrid search
        }
    },
    'embedder': {
        'provider': 'openai',
        'config': {
            'model': 'text-embedding-3-small',
            'api_key': os.environ["OPENAI_API_KEY"],
        }
    },
    'chunker': {
        'chunk_size': 2000,
        'chunk_overlap': 100,
        'length_function': 'len',
        'min_chunk_size': 0
    },
    'cache': {
      'similarity_evaluation': {
          'strategy': 'distance',
          'max_distance': 1.0,
      },
      'config': {
          'similarity_threshold': 0.8,
          'auto_flush': 50,
      },
    },
}

