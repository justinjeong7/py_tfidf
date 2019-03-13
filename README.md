# TFIDF package for Python

### Why?
1. For my side project, I need to be able to search for relevant terms (i.e. when searching for `apple juice`, I need `fresh apple`, `apple`, `golden apple`, etc.).

2. I wanted to take the chance to practice SOLID and TDD development practice.


### How it works:
1. I am working under the assumption that documents to search through are always being added or if you want, reset.
2. Since each document is summarized with term frequency (TF), I think the performance issue can be mitigated.
3. You can save/load the document summary from JSON file
4. Store query results.  In my use case, document sizes are small but there are a lot of them.  As the runtime is 2NQ where N is the number of documents and Q is the size of the query, I want to retain search history to avoid repeated compute resource

### Getting started:
Coming soon as a package

### Usage:
Coming soon. You can get started by looking at the test cases though :)
