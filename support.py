"""
Support functions for Feed Me.

@author: Andrew Eilertson
"""
import re
import references


def get_recipe_source(url):
    """Determine if URL is from known source. Returns source or 'unkown'"""

    # Get base url
    base_url = url.split('/')[2]

    # Get known sources
    known_sources = references.get_known_sources()

    # Check if base url in known sources
    if base_url in known_sources.keys():
        source = known_sources[base_url]
    else:
        source = 'unknown'

    return(source)


def set_instructions(instr):
    # Set blank list for instruction entries
    inst_list = []
    # Cycle through each entry in web instruction
    for entry in instr:
        # Add text value to instruction list
        inst_list.append(entry['text'])
    # Return list of instructions
    formatted_instructions = format_instructions(inst_list)
    return formatted_instructions


def strip_html_tags(text):
    tag_regex = re.compile('<.*?>')
    stripped_text = re.sub(tag_regex, '', text)
    return stripped_text


def strip_html_nbsp(text):
    stripped_text = text.replace("&nbsp;", " ")
    return stripped_text


def strip_html(text):
    text = strip_html_tags(text)
    text = strip_html_nbsp(text)
    return(text)


def get_search_terms(terms=[]):
    term = input("Enter ingridient: ")
    if term.lower() in ['', 'q', 'quit', 'e', 'exit']:
        return terms
    else:
        terms.append(term)
        get_search_terms(terms)
        return terms


def format_instructions(instructions):
    # Blank string to build from
    formatted_text = ''
    # Iterate through steps to build instructions
    for idx, step in enumerate(instructions, start=1):
        # Remove any remaining html from text
        clean_step = strip_html(step)
        # Format the step and add spacing
        formatted_text += f"Step {idx}\n{clean_step.strip()}\n\n"
    # Remove trailing whitespace from last step
    formatted_text = formatted_text.strip()

    return formatted_text
