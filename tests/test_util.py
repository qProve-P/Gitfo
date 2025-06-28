#################################
#       Tests for util.py       #
#################################

import pytest, typer, os, shutil, csv, json
from gitfo.util import prepareForCsv, printOutput, printOutputToFile, getHeaders

TEST_DATA = {
  "name": "Test",
  "description": "This is a test description",
  "array": ["item1", "item2"],
  "dictonary": {
    "key1": "value1",
    "key2": "value2"
  }
}

def testPrepareForCSV():
    expectedOutput = {
        "name": "Test",
        "description": "This is a test description",
        "array": "item1|item2",
        "dictonary": "key1:value1|key2:value2"
    }

    result = prepareForCsv(TEST_DATA)
    assert result == expectedOutput

def testPrintOutput(capsys):
    printOutput(TEST_DATA)

    captured = capsys.readouterr()
    plain = typer.unstyle(captured.out)

    assert "name: Test" in plain
    assert "description: This is a test description" in plain
    assert "array:" in plain
    assert "\titem1" in plain
    assert "\titem2" in plain
    assert "dictonary:" in plain
    assert "\tkey1: value1" in plain
    assert "\tkey2: value2" in plain

def testPrintToTxt():
    outputFile = "testTmp/output.txt"
    os.makedirs(os.path.dirname(outputFile), exist_ok=True)

    printOutputToFile(TEST_DATA, outputFile)

    with open(outputFile, "r") as f:
        content = f.read()

    assert "name: Test" in content
    assert "description: This is a test description" in content
    assert "array: ['item1', 'item2']" in content
    assert "dictonary: {'key1': 'value1', 'key2': 'value2'}" in content

    shutil.rmtree("testTmp")

def testPrintToCSV():
    outputFile = "testTmp/output.csv"
    os.makedirs(os.path.dirname(outputFile), exist_ok=True)

    printOutputToFile(TEST_DATA, outputFile)

    with open(outputFile, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 1
    row = rows[0]

    assert row["name"] == "Test"
    assert row["description"] == "This is a test description"
    assert row["array"] == "item1|item2"
    assert row["dictonary"] == "key1:value1|key2:value2"

    shutil.rmtree("testTmp")

def testPrintToJson():
    outputFile = "testTmp/output.json"
    os.makedirs(os.path.dirname(outputFile), exist_ok=True)

    printOutputToFile(TEST_DATA, outputFile)

    with open(outputFile, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["name"] == "Test"
    assert data["description"] == "This is a test description"
    assert data["array"] == ["item1", "item2"]
    assert data["dictonary"] == {
        "key1": "value1",
        "key2": "value2"
    }

    shutil.rmtree("testTmp")

def testGetHeadersNoAuth():
    headers = getHeaders(None)

    assert headers == {
        "Accept": "application/vnd.github.mercy-preview+json",
    }

def testGetHeadersWithAuth():
    headers = getHeaders("TestToken")

    assert headers == {
        "Accept": "application/vnd.github.mercy-preview+json",
        "Authorization": "token TestToken",
    }