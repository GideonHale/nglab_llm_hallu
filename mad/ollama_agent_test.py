import agents.ollama_agent as ag
from openai import OpenAI
from roles import role_titles, roles
from orderly_mad import orderly_mad
import agents.agent_presets as ap
import json
import os

def format_comments(comments):
    formatted_comments = []
    for comment in comments:
        comment_dict = {
            "score": comment["score"],
            "body": comment["body"],
            "replies": []
        }
        for reply in comment["replies"]:
            reply_dict = {
                "score": reply["score"],
                "body": reply["body"],
                # "replies": reply["replies"]
                # we're only gonna nest one level deep for now
            }
            comment_dict["replies"].append(reply_dict)
        formatted_comments.append(comment_dict)
    return formatted_comments

def get_gat_score(iden):
    with open(f"datasets/2025_final_predictions.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] == str(iden):
                return float(row[1])
    # if it doesn't find the score, raise an exception
    raise(Exception(f"Could not find GAT score for post {iden}"))

def main():
    # Define our debaters
    agents = [ap.joseph, ap.steven, ap.benjamin, ap.christopher, ap.elijah]

    print("--- Multi-Agent Debate System ---")

    # take one post from matched_claims_llm_scores.jsonl
    print("Loading data from matched_claims_llm_scores.jsonl...")
    data = []
    with open("datasets/matched_claims_llm_scores.jsonl", "r") as f:
        for line in f:
            data.append(json.loads(line))

    # if data not empty, take one post from data
    if data:
        post = data[0]
        iden = post["post_id"]
        title = post["post_title"]
        source_score = post["source_score"]
        missing_source_rate = post["missing_source_rate"]
        num_articles = post["num_articles"]
        num_unrated = post["num_unrated"]
        related_articles = post["related_articles"]
        formatted_related_articles = json.dumps(related_articles)
    else:
        print("No data found in matched_claims_llm_scores.jsonl")
        return

    # prompt = "Available files:\n"
    # # append all files names in mad/news/ to prompt with numerations
    # for i, file in enumerate(os.listdir("mad/news")):
    #     prompt += f"{i + 1}. {file}\n"
    # prompt += "\nSelect file: "
    # news_file_number = input(prompt)
    # news_file = os.listdir("mad/news")[int(news_file_number) - 1]
    # print('File selected: ', news_file)
    # news_file_path = f"mad/news/{news_file}"

    # # Load and format the JSON as the debate topic
    # with open(news_file_path, "r") as f:
    #     data = json.load(f)
    # iden = data["post_id"]
    # title = data["post_title"]
    # source_score = data["source_score"]
    # missing_source_rate = data["missing_source_rate"]
    # num_articles = data["num_articles"]
    # num_unrated = data["num_unrated"]

    print("Getting GAT score for post {iden}...")
    try:
        gat_score = get_gat_score(iden)
    except Exception as e:
        print('Error: ', e)
        gat_score = 0.5
        print("Using default GAT score of 0.5")

    # related_articles = data["related_articles"]
    # formatted_related_articles = json.dumps(related_articles)

    print("\n--- Comencing Debate ---")
    discussion = (
        f"[DEBATE RULES]\n"
        f"1. You are participating in a debate about the fakeness of the following news article.\n"
        f"2. Give a clear verdict (a numerical score between completely fake at 0 and completely reliable at 100) and then a brief, one-paragraph explanation of this and in response to any previous responses as well.\n"
        
        f"[DESCRIPTION OF DATA FIELDS]\n"
        f"Headline: The title of the news article.\n"
        f"Source score [from 0.0 to 1.0]: the average of all sources of related articles found in the Adfontes reliability dataset.\n"
        f"Missing source rate [from 0.0 to 1.0]: the rate of sources returned from the RAG system that did not have a match in the reliability dataset.\n"
        f"Number of articles [from 0 to 30]: the number of articles returned from the RAG system that had semantically similar titles to the source headline.\n"
        f"Number of unrated articles [from 0 to 30]: the number of articles returned from the RAG system that were not found in the reliability dataset.\n"
        f"GAT score [from 0.0 to 1.0]: a topological second opinion that signals whether community interaction patterns confirm or contradict the RAG's textual assessment.\n"
        f"Related articles: Set of related articles.\n"
        f"Reliability score [from 0 to 64]: the reliability of the source of the article according to AskNews.\n"
        
        f"[NEWS ARTICLE FOR DEBATE]\n"
        f"Headline: {title}\n"
        f"Source score: {source_score}\n"
        f"GAT score: {gat_score}\n"
        f"Missing source rate: {missing_source_rate}\n"
        f"Number of articles: {num_articles}\n"
        f"Number of unrated articles: {num_unrated}\n"
        f"Related articles: {formatted_related_articles}\n"
    )

    prompt = "\nEnter number of turns: "
    num_turns = int(input(prompt))
    final_transcript = orderly_mad(
        discussion,
        agents,
        num_turns,
        order="shuffle"
    )

    print("\n--- Debate Concluded ---")
    
    # Summarize the debate
    print("\n--- Summarizing Debate ---")
    summary = ap.summarizer.respond(final_transcript)
    final_transcript.append(summary)

    print("\n--- Summary ---")
    print(summary.content)

    print("\n--- Judging Debate ---")
    n = 3
    verdicts = []
    for i in range(n):
        print(f'\n--- Judge {i+1} / {n} thinking ---\n')

        # Judge the debate
        verdict = ap.judge.respond(final_transcript)

        print("\n--- Verdict ---")
        print(verdict.content)

        # Extract the verdict just to like super make sure that we have an integer value
        extracted_verdict = ap.extractor.respond([verdict])

        # test to see whether it's an integer from 0 to 5
        if not extracted_verdict.content.isdigit():
            print('Error: the extracted score', extracted_verdict.content, 'is not an integer')
            extracted_verdict.content = 0
            continue
        elif not (0 <= int(extracted_verdict.content) <= 5):
            print('Error: the extracted score', extracted_verdict.content, 'is not between 0 and 5')
            extracted_verdict.content = 0
            continue
        
        print('Score: ', extracted_verdict.content)
        verdicts.append(int(extracted_verdict.content))
    
    # Average the scores
    if len(verdicts) == 0:
        final_score = 'N/A'
    else:
        final_score = sum(verdicts) / len(verdicts) / 5
    print("Final Score: ", final_score)

if __name__ == "__main__":
    main()