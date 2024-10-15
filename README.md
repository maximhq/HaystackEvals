## How to stand up the stack

`docker build --platform linux/amd64 -t haystach-eval .`
`docker run -p 8080:8080 -t haystach-eval:latest`

## API Endpoints:

`api/document/evaluator/recall`

`api/document/evaluator/mrr`

`api/document/evaluator/mape`

## Payload:

For comparing Context IDs
```
{
	"ground_truth_documents": "1,2",
	"retrieved_documents": "1,2,3",
	"mode": "MULTI_HIT",
    "split_char": ","
}
```

For comparing Context Values. Each sentence is considered as a ground truth doc
```
{
	"ground_truth_documents": "France is in Europe. Paris is the capital of France.",
	"retrieved_documents": "France is in Europe.",
	"mode": "MULTI_HIT",
    "split_char": "."
}
```


