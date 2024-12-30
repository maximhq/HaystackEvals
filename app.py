from haystack import Document
from haystack.components.evaluators import (
    DocumentMAPEvaluator,
    DocumentMRREvaluator,
    DocumentRecallEvaluator,
)
import flask
from flask import jsonify, request, Response
import re
import ast
import json

from haystack.components.evaluators.document_recall import RecallMode

app = flask.Flask(__name__)


def process_regex(input_string):
    # input_string = "1,4,(5,7,8),2,(9,11)"
    var = ast.literal_eval(input_string)
    if type(var) == tuple:
        var = var

    output = []
    for item in var:
        if type(item) == tuple:
            output.append([str(x) for x in item])
        else:
            output.append(str(item))
    return output


@app.post("/api/document/evaluator/mape")
def mape():

    payload = request.json
    print("\n=== MAPE Evaluation Start ===")
    print("Received payload:", json.dumps(payload, indent=2))
    split_char = payload.get("split_char", ",")
    print(f"\nUsing split character: '{split_char}'")
    ground_truth_documents = payload["ground_truth_documents"].split(split_char)
    retrieved_documents = payload["retrieved_documents"].split(split_char)
    print(f"\nInitial document counts:")
    print(f"- Ground truth documents: {len(ground_truth_documents)}")
    print(f"- Retrieved documents: {len(retrieved_documents)}")

    evaluator = DocumentMAPEvaluator()

    ground_truth_documents = [
        Document(content=doc.strip())
        for doc in ground_truth_documents
        if len(doc.strip()) > 0
    ]
    retrieved_documents = [
        Document(content=doc.strip())
        for doc in retrieved_documents
        if len(doc.strip()) > 0
    ]
    print(f"\nAfter filtering:")
    print(f"- Ground truth docs: {len(ground_truth_documents)}")
    print(f"- Retrieved docs: {len(retrieved_documents)}")
    
    print("\nGround Truth Documents Content:")
    for i, doc in enumerate(ground_truth_documents):
        print(f"{i+1}. {doc.content[:100]}{'...' if len(doc.content) > 100 else ''}")
    
    print("\nRetrieved Documents Content:")
    for i, doc in enumerate(retrieved_documents):
        print(f"{i+1}. {doc.content[:100]}{'...' if len(doc.content) > 100 else ''}")

    result = evaluator.run(
        ground_truth_documents=[ground_truth_documents],
        retrieved_documents=[retrieved_documents],
    )
    print("\nEvaluation result:")
    print(json.dumps(result, indent=2))
    print("=== MAPE Evaluation End ===\n")

    response = {"mape": result["individual_scores"], "score": result["score"]}
    result = json.dumps(response)
    return Response(response=result, status=200, mimetype="application/json")


@app.post("/api/document/evaluator/mrr")
def mrr():

    payload = request.json
    print("\n=== MRR Evaluation Start ===")
    print("Received payload:", json.dumps(payload, indent=2))
    split_char = payload.get("split_char", ",")
    print(f"\nUsing split character: '{split_char}'")
    ground_truth_documents = payload["ground_truth_documents"].split(split_char)
    retrieved_documents = payload["retrieved_documents"].split(split_char)
    print(f"\nInitial document counts:")
    print(f"- Ground truth documents: {len(ground_truth_documents)}")
    print(f"- Retrieved documents: {len(retrieved_documents)}")

    evaluator = DocumentMRREvaluator()

    ground_truth_documents = [
        Document(content=doc.strip())
        for doc in ground_truth_documents
        if len(doc.strip()) > 0
    ]
    retrieved_documents = [
        Document(content=doc.strip())
        for doc in retrieved_documents
        if len(doc.strip()) > 0
    ]
    print(f"\nAfter filtering:")
    print(f"- Ground truth docs: {len(ground_truth_documents)}")
    print(f"- Retrieved docs: {len(retrieved_documents)}")
    
    print("\nGround Truth Documents Content:")
    for i, doc in enumerate(ground_truth_documents):
        print(f"{i+1}. {doc.content[:100]}{'...' if len(doc.content) > 100 else ''}")
    
    print("\nRetrieved Documents Content:")
    for i, doc in enumerate(retrieved_documents):
        print(f"{i+1}. {doc.content[:100]}{'...' if len(doc.content) > 100 else ''}")

    result = evaluator.run(
        ground_truth_documents=[ground_truth_documents],
        retrieved_documents=[retrieved_documents],
    )
    print("\nEvaluation result:")
    print(json.dumps(result, indent=2))
    print("=== MRR Evaluation End ===\n")

    response = {"mrr": result["individual_scores"], "score": result["score"]}
    result = json.dumps(response)
    return Response(response=result, status=200, mimetype="application/json")


@app.post("/api/document/evaluator/recall")
def recall():
    payload = request.json
    print("\n=== Recall Evaluation Start ===")
    print("Received payload:", json.dumps(payload, indent=2))
    mode = RecallMode.SINGLE_HIT
    split_char = payload.get("split_char", ",")
    print(f"\nUsing split character: '{split_char}'")
    ground_truth_documents = payload["ground_truth_documents"].split(split_char)
    retrieved_documents = payload["retrieved_documents"].split(split_char)
    print(f"\nInitial document counts:")
    print(f"- Ground truth documents: {len(ground_truth_documents)}")
    print(f"- Retrieved documents: {len(retrieved_documents)}")

    evaluator = DocumentRecallEvaluator(mode=RecallMode.SINGLE_HIT)
    if "mode" in payload:
        mode = payload["mode"]
        if mode == "SINGLE_HIT":
            evaluator = DocumentRecallEvaluator(mode=RecallMode.SINGLE_HIT)
        else:
            evaluator = DocumentRecallEvaluator(mode=RecallMode.MULTI_HIT)
    print(f"Recall Mode: {mode}")

    ground_truth_documents = [
        Document(content=doc.strip())
        for doc in ground_truth_documents
        if len(doc.strip()) > 0
    ]
    retrieved_documents = [
        Document(content=doc.strip())
        for doc in retrieved_documents
        if len(doc.strip()) > 0
    ]
    print(f"\nAfter filtering:")
    print(f"- Ground truth docs: {len(ground_truth_documents)}")
    print(f"- Retrieved docs: {len(retrieved_documents)}")
    
    print("\nGround Truth Documents Content:")
    for i, doc in enumerate(ground_truth_documents):
        print(f"{i+1}. {doc.content[:100]}{'...' if len(doc.content) > 100 else ''}")
    
    print("\nRetrieved Documents Content:")
    for i, doc in enumerate(retrieved_documents):
        print(f"{i+1}. {doc.content[:100]}{'...' if len(doc.content) > 100 else ''}")

    result = evaluator.run(
        ground_truth_documents=[ground_truth_documents],
        retrieved_documents=[retrieved_documents],
    )
    print("\nEvaluation result:")
    print(json.dumps(result, indent=2))
    print("=== Recall Evaluation End ===\n")

    response = {"recall": result["individual_scores"], "score": result["score"]}
    result = json.dumps(response)
    return Response(response=result, status=200, mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True)
