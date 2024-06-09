import requests
import time
import json
import os
from process_data import process

url = "https://leetcode.com/graphql/"

def list_all_questions(skip=0):
    total = None
    
    all_questions = {}
    
    while total is None or skip  < total:
        print("Skip:", skip)
        payload = {
            "query": """
            query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
                problemsetQuestionList: questionList(
                    categorySlug: $categorySlug
                    limit: $limit
                    skip: $skip
                    filters: $filters
                ) {
                    total: totalNum
                    questions: data {
                        acRate
                        difficulty
                        freqBar
                        frontendQuestionId: questionFrontendId
                        isFavor
                        paidOnly: isPaidOnly
                        status
                        title
                        titleSlug
                        topicTags {
                            name
                            id
                            slug
                        }
                        hasSolution
                        hasVideoSolution
                    }
                }
            }
            """,
            "variables": {
                "categorySlug": "all-code-essentials",
                "skip": skip,
                "limit": 100,
                "filters": {}
            },
            "operationName": "problemsetQuestionList"
        }
    
        response = requests.post(url, json=payload)

        #print(response.status_code)
        #print(response.json())
        data = response.json()['data']
        problemsetQuestionList = data["problemsetQuestionList"]
        
        questions = problemsetQuestionList["questions"]
        for question in questions:
            frontend_id = question["frontendQuestionId"]
            #all_questions[id] = question
            
            tags = question["topicTags"]
            titleSlug = question["titleSlug"]
            description = list_question(titleSlug)
            time.sleep(1)
            all_questions[frontend_id] = {
                "tags" : str(tags),
                "description" : str(description)
            }
            
        
        total = problemsetQuestionList["total"]
        skip += 100
        time.sleep(10)
        
        print(all_questions)
        with open(os.path.join("data", f"output-{skip}"), "w") as f:
            json.dump(all_questions, f, default=str)
        
    return all_questions

def list_question(question_slug):
    """
    Lists a specific question id
    """
    print("Looking up", question_slug)
    payload = {"query":"\n    query questionContent($titleSlug: String!) {\n  question(titleSlug: $titleSlug) {\n    content\n    mysqlSchemas\n    dataSchemas\n  }\n}\n    ","variables":{"titleSlug":question_slug},"operationName":"questionContent"}
    
    response = requests.post(url, json=payload)
    #print(response.status_code)
    #print(response.json())
    try:
        data = response.json()["data"]
        question = data["question"]
        print("Question:", question)
        content = question["content"]
        
        return content.lower().split("example")[0]
    except Exception:
        print("ERROR!!! Exception")
        return ""
    
if __name__ == "__main__":
    
    x = list_all_questions()
    
    # x = process(raw)
    
    with open("output.json", "w") as f:
        json.dump(x, f, default=str)
    
    print("Done writing stage 1")
    