import json
import os
import pandas as pd
import openai

dict_criteriaprompts_v1 = {"duplicate names of intentional elements": "In the XML enclosed using triple back ticks, do "
                                                                      "you see duplicate values for"
                                                                      "'name' attribute? Answer using yes or no only. Do not include any explanation.",

                           "duplicate identifiers of intentional elements": "In the XML enclosed using triple back ticks,"
                                                                            " do you see duplicate "
                                                                            "values for"
                                                                            "'id' attribute? Answer using yes or no only. Do not include any explanation.",

                           "empty intentional element": "In the XML enclosed using triple back ticks, "
                                                        "do you see empty string as a value for "
                                                        "'name' attribute? Answer using yes or no only. Do not include any explanation.",

                           "compare model modified and created dates": "In the XML enclosed using triple back ticks, "
                                                                       "if you see the attributes 'modified' and "
                                                                       "'created', convert the values of both the"
                                                                       "attributes to Date and compare them. Is value of "
                                                                       "'modified' attribute greater than the value of "
                                                                       "'created' attribute?  Answer Yes, or No if the "
                                                                       "attributes 'modified' and 'created' are present. "
                                                                       "Otherwise answer Not Applicable. Do not include any explanation.",

                           "empty goal model": "In the XML enclosed using triple back ticks, do you see that the element "
                                               "named 'grl-catalog' is empty? Answer yes or no only. Do not include any explanation.",

                           "intentional elements contained outside grlspec": "In the XML enclosed using triple back "
                                                                             "ticks, do you see any content outside of "
                                                                             "the section named 'grl-catalog'? Answer yes or no only. Do not include any explanation.",

                           "intentional element has name, id, and type": "In the XML enclosed using triple back ticks, "
                                                                         "do you find an element with name "
                                                                         "'intentional-element' with missing the"
                                                                         "following attributes missed- name, id, type? Answer yes or no only. Do not include any explanation.",

                           "actors section found in the model": "Does the XML have a section with title 'actor-def'?Yes or No?",

                           "actors used in links": "In the given XML, each actor element has an 'id' attribute, do you see the value of 'id' "
                                                   "attribute of an actor element used as the value for 'srcid' or 'destid' attributes "
                                                   "within the section named 'link-def'?Answer yes or no only. Do not include any explanation.",

                           "section for linked actors and intentional elements found in the model": "Does the XML have a section with title "
                                                                                                    "'actor-IE-link-def'? Answer using yes or no only? Do not include any explanation.",

                           "multiple actors for one intentional element": "In the XML enclosed using triple back ticks, within the section with name "
                                                                          "'actor-IE-link-def', do you see any element with same value for 'ie' attribute, "
                                                                          "but different value for 'actor' attribute? Answer Yes or No? Do not include any explanation.",

                           "intentional element category": "In the XML enclosed using triple back ticks, for an element "
                                                           "with name 'intentional-element', is the value for 'type' "
                                                           "attribute of the tag one of the following values - Task, Goal, Softgoal, Resource, Belief? Answer yes or no only. Do not include any explanation.",

                           "intentional element default decomposition type": "In the XML enclosed using triple back "
                                                                             "ticks, for an element with name "
                                                                             "'intentional-element', is the value of "
                                                                             "attribute 'decompositiontype' of the tag one of the following "
                                                                             "values - AND, OR, XOR? Answer yes or no only. Do not include any explanation.",

                           "contribution type category": "In the XML enclosed using triple back ticks, if you see an "
                                                         "element with name 'contribution', is the value for the attribute "
                                                         "'contributiontype'"
                                                         " of the tag one of the following values- Make, Help, Break, Hurt?  Answer Yes, "
                                                         "or No if element with name 'contribution' is present. Otherwise answer Not Applicable. Do not include any explanation.",

                           "contribution link validation": "In the XML enclosed using triple back ticks,, if you see an "
                                                           "element with name 'contribution', are the values for srcid "
                                                           "and destid"
                                                           "attributes in each tag different? Answer Yes, or No if element with name "
                                                           "'contribution' is present. Otherwise answer Not Applicable. Do not include any explanation.",

                           "contribution link without source": "In the XML enclosed using triple back ticks, if you see "
                                                               "an element with name 'contribution', is the "
                                                               "value for srcid empty string, or is element with name "
                                                               "'contribution' missing attribute 'srcid'? Answer yes or no only. Do not include any explanation.",

                           "contribution link without destination": "In the XML enclosed using triple back ticks, if you "
                                                                    "see a element with name 'contribution',"
                                                                    "is the value for destid empty string, or is element "
                                                                    "with name 'contribution' missing attribute 'destid? "
                                                                    "Answer yes or no only. Do not include any explanation.",

                           "decomposition link without source": "In the XML enclosed using triple back ticks, if you see "
                                                                "an element with name 'decomposition', is the "
                                                                "value for srcid empty string, or is element with name "
                                                                "'decomposition' missing attribute 'srcid'? Answer yes or no only. Do not include any explanation.",

                           "decomposition link without destination": "In the XML enclosed using triple back ticks, "
                                                                     "if you see an element with name 'decomposition',"
                                                                     "is the value for destid empty string, "
                                                                     "or is element with name 'contribution' missing "
                                                                     "attribute 'destid? Answer yes or no only. Do not include any explanation.",

                           "decomposition link validation": "In the XML enclosed using triple back ticks, if you see an "
                                                            "element with name 'decomposition', are the values for srcid "
                                                            "and destid"
                                                            "attributes for the tag different? Answer Yes, or No if element with name "
                                                            "'decomposition' if present. Otherwise answer Not Applicable. Do not include any explanation."
                           }

dict_criteriaprompts_v2 = {
    "duplicate names of intentional elements": "In the output enclosed using triple back ticks, do "
                                               "you see duplicate values in sections-"
                                               "'Actors', 'Soft Goals', 'Goals', 'Tasks for Goals', and 'Tasks for Soft Goals'? "
                                               "Answer using yes or no only. Do not include any explanation.",

    "empty intentional element": "In the output enclosed using triple back ticks, "
                                 "do you see empty string as a value in sections-"
                                 "'Actors', 'Soft Goals', 'Goals', 'Tasks for Goals', and 'Tasks for Soft Goals'? "
                                 "Answer using yes or no only. Do not include any explanation.",

    "empty goal model": "Is the output enclosed using triple back ticks empty? Answer yes or no only. Do not include any explanation.",

    "actors section found in the model": "Does the output have a section with title 'actors'? Yes or No?",

    "actors used in links": "In the output enclosed using triple back ticks, do you see an actor "
                            "mentioned in the section 'actors' used as a source or destination "
                            "within the section named 'Decompositions Links' or 'Contributions Links'? Answer yes or no only. Do not include any explanation.",

    "section for linked actors and intentional elements found in the model": "Does the output enclosed using triple back ticks, have the following sections with titles- "
                                                                             "'IE Links for Goals', 'IE Links for Tasks of Soft Goals', " 
                                                                             "'IE Links for Tasks of Goals', 'IE Links for Tasks of Soft Goals'? "
                                                                             "Answer using yes or no only? Do not include any explanation.",

    "intentional elements associated with actors_goals": "In the output enclosed using triple back ticks, is every element "
                                                   "in the section-'Goals' present in the section name "
                                                   "'IE Links for Goals'? "
                                                   "Answer Yes or No? Do not include any explanation.",

    "intentional elements associated with actors_softgoals": "In the output enclosed using triple back ticks, is every element "
                                                       "in the section-'Soft Goals' present in the section name "
                                                       "'IE Links for Tasks of Soft Goals'? "
                                                       "Answer Yes or No? Do not include any explanation.",

    "intentional elements associated with actors_taskgoals": "In the output enclosed using triple back ticks, is every element "
                                                       "in the section-'Tasks of Goals' present in the section name "
                                                       "'IE Links for Tasks of Goals'? "
                                                       "Answer Yes or No? Do not include any explanation.",

    "intentional elements associated with actors_tasksoftgoals": "In the output enclosed using triple back ticks, is every element "
                                                             "in the section-'Tasks of Soft Goals' present in the section name "
                                                             "'IE Links for Tasks of Soft Goals'? "
                                                             "Answer Yes or No? Do not include any explanation.",

"multiple actors for one intentional element": "In the output enclosed using triple back ticks, is there atleast one entry in the following sections-"
                                               "following sections with titles- "
                                             "'IE Links for Goals', 'IE Links for Tasks of Soft Goals', " 
                                             "'IE Links for Tasks of Goals', 'IE Links for Tasks of Soft Goals' that "
                                           "is associated with multiple actors? Answer Yes or No? Do not include any explanation.",

    "intentional element category": "In the output enclosed using triple back ticks, "
                                    "do you see any section other than the following- 'Tasks for Goals', 'Tasks for Soft Goals', 'Goals', 'Soft Goals', 'Actors', "
                                    "'Contribution Links', 'Decomposition Links',"
                                     "'IE Links for Goals', 'IE Links for Tasks of Soft Goals', " 
                                     "'IE Links for Tasks of Goals', and 'IE Links for Tasks of Soft Goals'?"
                                    " Answer yes or no only. Do not include any explanation.",

    "contribution link validation": "In the output enclosed using triple back ticks, if you see a section with name 'Contribution Links', are the values for "
                                    "source and destination, different? Answer Yes, or No if section "
                                    "'Contribution Links' is present. Otherwise answer Not Applicable. Do not include any explanation.",

    "contribution link without source": "In the output enclosed using triple back ticks, if you see a section with name 'Contribution Links', is the "
                                        "source empty string? Answer yes or no only. Do not include any explanation.",

    "contribution link without destination": "In the output enclosed using triple back ticks, if you see a element with name 'Contribution Links', is the value for "
                                             "destination empty string? Answer yes or no only. Do not include any explanation.",

    "contribution type category": "In the output enclosed using triple back ticks, under the section 'Contribution Links', is the contribution type"
                                  " one of the following values- Make, Help, Break, Hurt? Answer "
                                  "Yes, or No if element with name 'contribution' is present. Otherwise answer Not "
                                  "Applicable. Do not include any explanation.",

    "intentional element default decomposition type": "In the output enclosed using triple back ticks, under the section 'Decomposition Links' do you see any decomposition "
                                                      "type' other than other than the following values - AND, OR, XOR? Answer yes or no only. "
                                                      "Do not include any explanation.",

    "decomposition link validation": "In the output enclosed using triple back ticks, if you see a section with name 'Decomposition Links', are the values for "
                                     "source and destination different? Answer Yes, or No if element with name "
                                     "'decomposition' if present. Otherwise answer Not Applicable. Do not include any "
                                     "explanation.",

    "decomposition link without source": "In the output enclosed using triple back ticks, if you see a section with name 'Decomposition Links', is the value for "
                                         "source empty string, or is the 'source' missing? Answer yes or no only. Do "
                                         "not include any explanation.",

    "decomposition link without destination": "In the output enclosed using triple back ticks, if you see an element with name 'Decomposition Links', is the value for "
                                              "destination empty string, or is the destination' missing? Answer yes or no "
                                              "only. Do not include any explanation."
}


def load_config(config_file: str) -> dict:
    """
    Loads the JSON configuration and sets the OpenAI API key.
    @param config_file:  Path to the JSON configuration file.
    @returns config: dictionary of the parsed configuration
    """
    with open(config_file) as json_file:
        config = json.load(json_file)
    # sets the OpenAI key
    openai.api_key = config["OPEN_AI_KEY"]
    return config


def load_userstories(input_dir: str) -> list:
    stories = []

    # iterate over files in
    # that directory
    for filename in os.listdir(input_dir):
        stories_file = os.path.join(input_dir, filename)

        # checking if it is a file
        if os.path.isfile(stories_file):

            # Opening file
            file1 = open(stories_file, 'r')
            file_content = ''

            for line in file1:
                file_content = file_content + line

            # Closing files
            file1.close()

        stories.append(file_content)
    return stories


def save_generated_model(output_dir: str, output_filename: str, contents: str) -> None:
    with open(os.path.join(output_dir,
                           output_filename), 'w') as generated_goalmodel:
        generated_goalmodel.write(contents)


def save_execution_results(output_dir: str, output_filename: str, results_lst: list) -> None:
    # Calling DataFrame constructor on the zipped lists, with columns specified
    results_df = pd.DataFrame(results_lst,
                              columns=['Stories', 'Status'])
    # save the contents as a csv
    results_df.to_csv(os.path.join(output_dir, output_filename))


def load_prompt_text(file_dir: str, textfile: str) -> str:
    # checking if it is a file
    # Opening file
    file1 = open(os.path.abspath(os.path.join(file_dir,
                                              textfile)))
    prompt_content = ''

    for line in file1:
        prompt_content = prompt_content + line

    # Closing files
    file1.close()

    return prompt_content


def getCriteria_v1() -> list:
    return ["Actors section found in the model",
            "Actors used in links",
            "Compare model modified and created dates",
            "Contribution link validation",
            "Contribution link without source",
            "Contribution link without destination",
            "Contribution type category",
            "Decomposition link validation",
            "Decomposition link without source",
            "Decomposition link without destination",
            "Duplicate Identifiers of intentional elements",
            "Duplicate names of intentional elements",
            "Empty goal model",
            "Empty intentional element",
            "Intentional elements contained outside GRLspec",
            "Intentional element has name, id, and type",
            "Intentional element category",
            "Intentional element default decomposition type",
            "Multiple actors for one intentional element",
            "Section for linked actors and intentional elements found in the model"]

def getCriteria_v2() -> list:
    return [
    "duplicate names of intentional elements",
    "empty intentional element",
    "empty goal model",
    "actors section found in the model",
    "actors used in links",
    "section for linked actors and intentional elements found in the model",
    "intentional elements associated with actors_goals",
    "intentional elements associated with actors_softgoals",
    "intentional elements associated with actors_taskgoals",
    "intentional elements associated with actors_tasksoftgoals",
    "multiple actors for one intentional element",
    "intentional element category",
    "contribution link validation",
    "contribution link without source",
    "contribution link without destination",
    "contribution type category",
    "intentional element default decomposition type",
    "decomposition link validation",
    "decomposition link without source",
    "decomposition link without destination"]


def getPrompt_text(query_prompt: str) -> str:
    # print(query_prompt.lower())
    try:
        return dict_criteriaprompts_v2[query_prompt.lower().strip()]
    except:
        print(query_prompt)
        print("no text")
        return ""
