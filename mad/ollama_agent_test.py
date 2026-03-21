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
    news_file = input("Enter news file path: ")
    news_file_path = f"mad/{news_file}"
    rounds = int(input("Enter number of turns: "))

    # Load and format the JSON as the debate topic
    with open(news_file_path, "r") as f:
        data = json.load(f)
    post = data["post"]
    comments = data["comments"]
    formatted_comments = json.dumps(format_comments(comments))

    discussion = (
        f"[DEBATE RULES]\n"
        f"1. You are participating in a debate about the fakeness of the following news article.\n"
        f"2. Give a verdict and then a brief, one-paragraph explanation the article is fake or not in response to previous responses too.\n"
        
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
        rounds,
        order="random"
    )

    print("--- Debate Concluded ---")
    
    # Summarize the debate
    summary = ap.summarizer.respond(final_transcript)

    print("\n--- Summary ---\n", summary.content)
    

if __name__ == "__main__":
    # print('Role options: ', ', '.join(role_titles))
    # while True:
    #     role = input("Enter the role: ")
    #     # role = "journalist"
    #     if role in role_titles:
    #         break
    #     print("Invalid role. Please try again.")
    main()