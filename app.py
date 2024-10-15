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
    split_char = payload.get("split_char", ",")
    ground_truth_documents = payload["ground_truth_documents"].strip().split(split_char)
    retrieved_documents = payload["retrieved_documents"].strip().split(split_char)

    evaluator = DocumentMAPEvaluator()

    ground_truth_documents = [Document(content=doc) for doc in ground_truth_documents]
    retrieved_documents = [Document(content=doc) for doc in retrieved_documents]

    result = evaluator.run(
        ground_truth_documents=[ground_truth_documents],
        retrieved_documents=[retrieved_documents],
    )
    response = {"mape": result["individual_scores"], "score": result["score"]}
    result = json.dumps(response)
    return Response(response=result, status=200, mimetype="application/json")


@app.post("/api/document/evaluator/mrr")
def mrr():

    payload = request.json
    split_char = payload.get("split_char", ",")
    ground_truth_documents = payload["ground_truth_documents"].strip().split(split_char)
    retrieved_documents = payload["retrieved_documents"].strip().split(split_char)

    evaluator = DocumentMRREvaluator()

    ground_truth_documents = [Document(content=doc) for doc in ground_truth_documents]
    retrieved_documents = [Document(content=doc) for doc in retrieved_documents]
    result = evaluator.run(
        ground_truth_documents=[ground_truth_documents],
        retrieved_documents=[retrieved_documents],
    )

    response = {"mrr": result["individual_scores"], "score": result["score"]}
    result = json.dumps(response)
    return Response(response=result, status=200, mimetype="application/json")


@app.post("/api/document/evaluator/recall")
def recall():
    payload = request.json

    split_char = payload.get("split_char", ",")
    ground_truth_documents = payload["ground_truth_documents"].strip().split(split_char)
    retrieved_documents = payload["retrieved_documents"].strip().split(split_char)

    evaluator = DocumentRecallEvaluator(mode=RecallMode.SINGLE_HIT)
    if "mode" in payload:
        mode = payload["mode"]
        if mode == "SINGLE_HIT":
            evaluator = DocumentRecallEvaluator(mode=RecallMode.SINGLE_HIT)
        else:
            evaluator = DocumentRecallEvaluator(mode=RecallMode.MULTI_HIT)
    ground_truth_documents = [Document(content=doc) for doc in ground_truth_documents]
    retrieved_documents = [Document(content=doc) for doc in retrieved_documents]

    result = evaluator.run(
        ground_truth_documents=[ground_truth_documents],
        retrieved_documents=[retrieved_documents],
    )

    response = {"recall": result["individual_scores"], "score": result["score"]}
    result = json.dumps(response)
    return Response(response=result, status=200, mimetype="application/json")


if __name__ == "__main__":
    app.run(debug=True)
