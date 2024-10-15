from haystack import Document
from haystack.components.evaluators import DocumentMAPEvaluator, DocumentMRREvaluator, DocumentRecallEvaluator
from haystack.components.evaluators.document_recall import RecallMode
evaluator = DocumentRecallEvaluator(mode=RecallMode.SINGLE_HIT)
result = evaluator.run(ground_truth_documents=[[Document(content="1"),Document(content="2"),Document(content="3")]], 
                       retrieved_documents=[[Document(content="1"),Document(content="2")]])

print(result)