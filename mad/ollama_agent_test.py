import agents.ollama_agent as ag
from openai import OpenAI
from roles import role_titles, roles
from orderly_mad import orderly_mad
import presets as ap
import json

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
    news_file = input("Enter news file name: ")
    news_file_path = f"mad/news/{news_file}"
    num_turns = int(input("Enter number of turns: "))

    # Load and format the JSON as the debate topic
    with open(news_file_path, "r") as f:
        data = json.load(f)
    post = data["post"]
    comments = data["comments"]
    formatted_comments = json.dumps(format_comments(comments))

    discussion = (
        f"[DEBATE RULES]\n"
        f"1. You are participating in a debate about the fakeness of the following news article.\n"
        f"2. Give a clear verdict (fake or not) and then a brief, one-paragraph explanation of this and in response to any previous responses as well.\n"
        
        f"[NEWS ARTICLE FOR DEBATE]\n"
        f"Headline: {post['title']}\n"
        f"Source domain: {post['domain']}\n"
        f"Body: {post['body']}\n"
        f"[COMMENTS FOR DEBATE]\n"
        f"{formatted_comments}\n"
    )

    final_transcript = orderly_mad(
        discussion,
        agents,
        num_turns,
        order="random"
    )

    print("--- Debate Concluded ---")
    
    # Summarize the debate
    summary = ap.summarizer.respond(final_transcript)

    print("\n--- Summary ---\n", summary.content)
    

if __name__ == "__main__":
    main()