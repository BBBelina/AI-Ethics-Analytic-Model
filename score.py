import pandas as pd
import requests
import json

# Replace with your actual API endpoint and access token
API_URL = "https://api.chatgpt-nano.example.com/evaluate"
API_HEADERS = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",  # Replace with your token if required
    "Content-Type": "application/json"
}

# Define an indicator dictionary with indicator numbers and corresponding descriptions
indicator_dict = {
    1: "Refuses or contains clearly harmful requests (violence, self‑harm, illegal activity)",
    2: "False refusal rate on benign prompts monitored (over-refusal)",
    3: "Refuses or contains financial coercion/doxxing patterns",
    4: "Minor exposure rate to proscribed content",
    5: "Sensitive topic exposure pacing (teens)",
    6: "Time‑to‑intervention to block/deflect off‑platform invites and display safety guidance",
    7: "Real-time scam pattern flagging for seniors (e.g., impostor, lottery, tech-support)",
    8: "Real-time scam and phishing detection tuned for seniors",
    9: "Clarity of voice-clone warnings in UX (elder-scenario tests)",
    10: "Voice-clone risk detection & warning (elder-scenario tests)",
    11: "Contains crisis language and prevents escalation",
    12: "Correctly flags crisis cues (true‑positive rate)",
    13: "Avoids missing crisis cues (false‑negative rate)",
    14: "Grooming detection false-negative rate",
    15: "Grooming detection true-positive rate",
    16: "De‑escalation signal quality in sensitive exchanges (expert rubric)",
    17: "Safety referral reliability & accuracy in scenario tests",
    18: "Trigger‑content detection & guarding (configurable, low over‑blocking)",
    19: "Agent transactional guardrails and dry-run modes",
    20: "Agent human-in-the-loop escalation thresholds for high-risk actions",
    21: "Off-platform invite interdiction program present",
    22: "Off-platform invite interdiction time-to-intervention",
    23: "Resistance to jailbreaks and prompt injection tested on hidden evals",
    24: "Data poisoning and model extraction risks assessed",
    25: "Prompt-injection stress test coverage",
    26: "Unauthorized tool-call interdiction TPR/FPR",
    27: "Guard-rail efficacy against data exfiltration",
    28: "Model/agent isolation and secret-scoping",
    29: "MITRE ATLAS technique coverage reporting"
}


# Function to get the score from the API for a given text block and indicator number
def get_indicator_score(text_block, indicator_number):
    indicator_description = indicator_dict.get(indicator_number, "No description available.")
    # Construct the prompt
    prompt = prompt = f"""
    Evaluation Criteria:
    0 - completely Ungrounded
    Score is not based on any text in the chunk
    Key claims or key words in the justification do not appear anywhere in the chunk
    Chunks includes outside knowledge or hallucinated mechanisms

    25 - Minimally Grounded
    Detects few keywords, but does not use meaningful evidence
    Chunks only has vague assumption or vague explanation
    No clear mapping between evidence and score

    50 - Partially Grounded
    Some use of evidence, but the reasoning is incomplete
    There’s partially relies on assumptions or over-interpretation
    The chunk supports the category, but does not justify the level of scoring claimed

    75 - Strongly Grounded
    There’s explicit text in the chunk
    Clearly connects evidence into the scope of the indicator
    There’s very speculation; minor over-interpretation only. 

    100 - Fully Grounded & Justified
    The indicator directly supported by explicit evidence in the chunk
    There’s no assumptions, extrapolation, or fabrication

    I need you to evaluate whether this text clearly explains the relevant institutional rules related to the indicator. The score should be based on this dimension, not just whether the content is present.
    Please score the following text according to the above criteria:

    
    Indicator: {indicator_number}
    Indicator Description: {indicator_description}
    Text:{text_block}

    Please return the response in the following JSON format:
    {{
    "score": <score_value>
    }}
    Where `<score_value>` is the score based on the evaluation criteria above. Ensure that the output includes the "score" field, and the value corresponds to the evaluation score of the given text block.
    """
    # Prepare the request payload
    payload = {
        "prompt": prompt,
        "max_tokens": 200  # Adjust the token size if necessary
    }

    # Send a POST request to the API
    response = requests.post(API_URL, headers=API_HEADERS, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Assuming the response contains a score
        result = response.json()
        score = result.get("score", None)  # Assuming 'score' key contains the score
        if score is not None:
            return score
        else:
            print(f"Error: No score returned for indicator {indicator_number}")
            return 0  # Return a default score if no score is returned
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return 0  # Return a default score on failure

# Function to apply the scoring process to the DataFrame
def score_text_blocks(df):
    indicators = list(range(1, 30))  # Indicator numbers from l1 to l29
    
    # Iterate over each row
    for index, row in df.iterrows():
        text_block = row['TextBlock']
        
        # Score each indicator
        for indicator in indicators:
            # Get the score for the current indicator (replace with real API call)
            score = get_indicator_score(text_block, indicator)
            # Update the corresponding column for the indicator
            df.loc[index, f'l{indicator}'] = score
            
    return df

# Load the provided CSV file
file_path = 'openai_segmentation.csv'
data = pd.read_csv(file_path)

# Apply the scoring process
data_with_scores = score_text_blocks(data)

# Save the DataFrame with the scores to a new CSV
output_file_path = 'openai_segmentation.csv'  # You can change this path as needed
data_with_scores.to_csv(output_file_path, index=False)

