from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from utils import add_item_to_file
from prompts import Prompts
from brands import Brand
from files import Files
from logger import Logger
from llm import LLM, GenerationMode, GenerationItemType


class LinkedInGenerator:
    def __init__(self, brand: Brand, language: str, idea: str, prompt_expansion: str, generation_mode: GenerationMode):
        self.brand = brand
        self.language = language
        self.idea = idea
        self.prompt_expansion = prompt_expansion
        self.generation_mode = generation_mode

    def generate_post(self):
        prompt = f"Write a LinkedIn post in {self.language} with 5-8 paragraphs for their account that talks about '{self.idea}'{Prompts.get_avoids()}{Prompts.build_style_prompt(self.brand.style)}"
        if (self.prompt_expansion != ""):
            prompt = prompt + \
                f"\n\nTake this also into account: {self.prompt_expansion}"
        post = LLM.generate(
            [SystemMessage(content=self.brand.description), HumanMessage(
                content=prompt)], GenerationItemType.POST, self.generation_mode
        ).content.strip()
        Logger.log("Generated LinkedIn post", post)
        add_item_to_file(Files.linkedin_results, post)
        return post
