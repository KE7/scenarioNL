

from typing import Dict, List
import openai
import os

import yaml
from scenicNL.common import ModelInput, PromptFiles

class CompositionalScenic():

    def __init__(self):
        super().__init__()
        openai.api_base = "http://localhost:8080/v1"
        openai.api_key = "sk-no-key-required"


    @staticmethod
    def _query_and_parse_for_final_answer(
        messages: List[Dict],
        temperature: float,
        verbose: bool,
        question: str
    ) -> str:
        response =openai.ChatCompletion.create(
            model="LLama_CPP",
            messages=messages,
            temperature=temperature,
        )
        answer = response.choices[0].message.content
        if verbose:
            print(f"--- BEGIN: Question {question} Response ---")
            print(answer)
            print(f"--- END: Question {question} Response ---")

        # the answer is provided as 3 experts and 1 final where each of them
        # says JUSTIFICATION and FINAL_ANSWER
        # we just want the FINAL_ANSWER of the final
        answer = answer.split("FINAL_ANSWER: ")[-1]

        return answer


    def _step_one(
        self,
        model_input: ModelInput,
        temperature: float,
        system_message: dict,
        questions: dict,
        verbose: bool,
    ) -> str:
        question_num = "one"
        user_message = {
            "role": "user",
            "content": questions[question_num]["question"].format(description=model_input.nat_lang_scene_des),
        }
        messages = [system_message, user_message]
        answer = self._query_and_parse_for_final_answer(
            messages=messages,
            temperature=temperature,
            verbose=verbose,
            question=question_num,
        )

        return answer
    

    def _build_constants(
        self,
        model_input: ModelInput,
        temperature: float,
        system_message: dict,
        objects: str,
        questions: dict,
        verbose: bool,
    ) -> str:
        get_objs_q_num = "nine"
        user_message = {
            "role": "user",
            "content": questions[get_objs_q_num]["question"].format(objects_from_one=objects),
        }
        messages = [system_message, user_message]
        objects = self._query_and_parse_for_final_answer(
            messages=messages,
            temperature=temperature,
            verbose=verbose,
            question=get_objs_q_num,
        )

        user_message = {
            "role": "user",
            "content": questions["four"]["b"]["question"].format(
                description=model_input.nat_lang_scene_des, 
                objects_from_nine=objects,
            ),
        }
        messages = [system_message, user_message]
        missing_objects = self._query_and_parse_for_final_answer(
            messages=messages,
            temperature=temperature,
            verbose=verbose,
            question="four b",
        )

        generic_dists_q_num = "five"
        user_message = {
            "role": "user",
            "content": questions[generic_dists_q_num]["question"].format(
                description=model_input.nat_lang_scene_des, 
                missing_object_info=missing_objects,
            ),
        }
        messages = [system_message, user_message]
        generic_dists = self._query_and_parse_for_final_answer(
            messages=messages,
            temperature=temperature,
            verbose=verbose,
            question=generic_dists_q_num,
        )

        scenic_dists_q_num = "six"
        user_message = {
            "role": "user",
            "content": questions[scenic_dists_q_num]["question"].format(
                description=model_input.nat_lang_scene_des, 
                missing_info=missing_objects,
                distributions=generic_dists,
            ),
        }
        messages = [system_message, user_message]
        scenic_dists = self._query_and_parse_for_final_answer(
            messages=messages,
            temperature=temperature,
            verbose=verbose,
            question=scenic_dists_q_num,
        )

        # Finally, we are ready to construct the first part of a Scenic program
        # we will ask the LLM to take the objects and scenic distributions and
        # declare them as constants in a Scenic program
        # we can re-try up to compiler_error many times
        

        

    def compositionally_construct_scenic_program(
        self,
        model_input: ModelInput,
        temperature: float,
        max_tokens: int,
        verbose: bool,
    ) -> str:
        """
        Constructs a scenic program by parts
        """
        questions = None
        with os.open(PromptFiles.COMPOSITIONAL_GBNF.value) as f:
            prompt = f.read()
            questions = yaml.safe_load(prompt)

        system_message = {
            "role": "system",
            "content": questions["context"],
        }

        # Step 1: getting the objects
        objects = self._step_one(
            model_input=model_input,
            temperature=temperature,
            system_message=system_message,
            questions=questions,
            verbose=verbose,
        )

        # Step 2: write the constants and variables section of the scenic program
        constants = self._build_constants(
            model_input=model_input,
            temperature=temperature,
            system_message=system_message,
            objects=objects,
            questions=questions,
            verbose=verbose,
        )
        
    