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

def main():
    # Define our debaters
    agents = [ap.joseph, ap.steven, ap.benjamin, ap.christopher, ap.elijah]

    print("--- Multi-Agent Debate System ---")

    prompt = "Available files:\n"
    # append all files names in mad/news/ to prompt with numerations
    for i, file in enumerate(os.listdir("mad/news")):
        prompt += f"{i + 1}. {file}\n"
    prompt += "\nSelect file: "
    news_file_number = input(prompt)
    news_file = os.listdir("mad/news")[int(news_file_number) - 1]
    print('File selected: ', news_file)
    news_file_path = f"mad/news/{news_file}"
    prompt = "\nEnter number of turns: "
    num_turns = int(input(prompt))

    # Load and format the JSON as the debate topic
    with open(news_file_path, "r") as f:
        data = json.load(f)
    title = data["post_title"]
    source_score = data["source_score"]
    missing_source_rate = data["missing_source_rate"]
    num_articles = data["num_articles"]
    num_unrated = data["num_unrated"]
    gat_score = 0.5 # TODO: get the actual score from Justice's comment scoring system

    related_articles = data["related_articles"]
    formatted_related_articles = json.dumps(related_articles)

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

    final_transcript = orderly_mad(
        discussion,
        agents,
        num_turns,
        order="shuffle"
    )

    print("\n--- Debate Concluded ---")
    
    # Summarize the debate
    summary = ap.summarizer.respond(final_transcript)

    print("\n--- Summary ---")
    # print(summary.content)

    # Judge the debate
    verdict = ap.judge.respond(final_transcript + [summary])

    print("\n--- Verdict ---")
    # print(verdict.content)

    # Extract the verdict
    extracted_verdict = ap.extractor.respond([verdict])

    print("\n--- Extracted Verdict ---\n", extracted_verdict.content)
    

if __name__ == "__main__":
    main()